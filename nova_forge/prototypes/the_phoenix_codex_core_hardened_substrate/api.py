import asyncio
import hashlib
import json
import os
import subprocess
import tempfile
import time
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import ed25519
from fastapi import APIRouter, Header, HTTPException, Request, status, WebSocket, WebSocketDisconnect
from jsonschema import Draft202012Validator, ValidationError
from pydantic import BaseModel

from . import worker
from .config import (AUTHORIZED_PUBLIC_KEYS, MIN_FINALIZE_STAKE, PHOENIX_CODEX_SCHEMA,
                     PHOENIX_VOTE_SCHEMA, REPLAY_WINDOW_SECONDS, UIAC_PATTERN)
from .state import verify_merkle_proof

router = APIRouter()

class ProofVerificationRequest(BaseModel):
    leaf_hash_hex: str
    proof: list
    root_hash_hex: str

def verify_signature_and_freshness(node_id: str, sig_hex: str, raw_body: bytes) -> dict:
    if node_id not in AUTHORIZED_PUBLIC_KEYS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[node_id])
        sig = bytes.fromhex(sig_hex)
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, raw_body)
        payload = json.loads(raw_body.decode())
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch or malformed payload.")

    ts = payload.get("timestamp")
    if not isinstance(ts, int) or abs(time.time() - ts) > REPLAY_WINDOW_SECONDS:
        raise HTTPException(400, "[-] Timestamp outside freshness window.")
    return payload

@router.get("/api/v1/health")
def health_check():
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    with worker.substrate.lock:
        state = {
            "total_blocks_processed": worker.substrate.total_blocks_processed,
            "global_state_root": worker.substrate.global_state_root,
        }
        return {
            "status": "stasis" if worker.substrate.is_stasis_active() else "active", "version": "4.0.0",
            "total_blocks": state["total_blocks_processed"], "global_state_root": state["global_state_root"],
            "registered_namespaces": len(worker.substrate.node_registry),
            "active_proposals": sum(1 for p in worker.substrate.proposal_registry.values() if p["status"] == "VOTING"),
            "dlq_depth": len(worker.substrate.dead_letter_queue),
            "merkle_leaf_count": worker.substrate.merkle.leaf_count,
            "peers_connected": len(worker.active_sockets),
        }

@router.get("/api/v1/merkle/proof/{leaf_index}")
def get_merkle_proof(leaf_index: int):
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    with worker.substrate.lock:
        proof = worker.substrate.merkle.generate_merkle_proof(leaf_index)
        if not proof and leaf_index >= worker.substrate.merkle.leaf_count:
            raise HTTPException(404, f"[-] Leaf index {leaf_index} out of range.")
        return {
            "leaf_index": leaf_index, "proof": proof,
            "current_root": worker.substrate.global_state_root,
            "total_leaves": worker.substrate.merkle.leaf_count,
        }

@router.post("/api/v1/merkle/verify")
def verify_proof_endpoint(req: ProofVerificationRequest):
    result = verify_merkle_proof(req.leaf_hash_hex, req.proof, req.root_hash_hex)
    return {"valid": result, "leaf_hash": req.leaf_hash_hex, "root": req.root_hash_hex}

@router.websocket("/api/v1/network/sync")
async def websocket_p2p_sync(websocket: WebSocket, x_phoenix_node_id: str = Header(...)):
    if not worker.substrate or x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS or x_phoenix_node_id in worker.substrate.quarantined_peers:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    async with worker._sockets_lock: worker.active_sockets.add(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try: packet = json.loads(raw)
            except (json.JSONDecodeError, AttributeError, TypeError): continue
            if not (action_type := packet.get("action_type")) or not isinstance(payload := packet.get("payload", {}), dict): continue
            if x_phoenix_node_id in worker.substrate.quarantined_peers or payload.get("nonce") in worker.substrate.seen_nonces: continue
            try: worker.tx_queue.put_nowait({"action_type": action_type, "payload": payload, "node_id": x_phoenix_node_id})
            except asyncio.QueueFull: print(f"[-] Backpressure: dropped packet from {x_phoenix_node_id}")
    except WebSocketDisconnect: pass
    finally:
        async with worker._sockets_lock: worker.active_sockets.discard(websocket)

@router.get("/api/v1/codex/entry/{entry_namespace:path}")
def get_entry_history(entry_namespace: str):
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    with worker.substrate.lock:
        if entry_namespace not in worker.substrate.node_registry: raise HTTPException(404, "[-] Namespace not found.")
        return worker.substrate.node_registry[entry_namespace].to_dict()

@router.get("/api/v1/governance/proposals")
def list_proposals(status_filter: str | None = None):
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    with worker.substrate.lock:
        proposals = list(worker.substrate.proposal_registry.values())
        if status_filter: proposals = [p for p in proposals if p["status"] == status_filter.upper()]
        return proposals

@router.get("/api/v1/governance/proposals/{proposal_id}")
def get_proposal(proposal_id: int):
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    with worker.substrate.lock:
        if not (prop := worker.substrate.proposal_registry.get(proposal_id)): raise HTTPException(404, f"[-] Proposal {proposal_id} not found.")
        return prop

@router.post("/api/v1/governance/propose", status_code=status.HTTP_202_ACCEPTED)
async def submit_proposal(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if not worker.substrate: raise HTTPException(503, "Substrate not initialized.")
    if worker.substrate.is_stasis_active(): raise HTTPException(503, "[-] Substrate locked in Stasis Mode.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)

    if UIAC_PATTERN.search(payload.get("assertion", "")) or UIAC_PATTERN.search(payload.get("lineage", {}).get("justification", "")):
        raise HTTPException(422, "[-] UIAC-001 Violation.")

    errors = sorted(Draft202012Validator(PHOENIX_CODEX_SCHEMA).iter_errors(payload), key=lambda e: e.path)
    if errors:
        worker.substrate.append_dlq({"error_class": "SCHEMA_VALIDATION_FAILURE", "timestamp_captured": time.time(), "raw_payload": payload, "audit_meta": {"node_origin": x_phoenix_node_id, "reason": errors[0].message}})
        raise HTTPException(400, f"[-] Schema error: {errors[0].message}")

    with worker.substrate.lock:
        state = {"last_event_hash": worker.substrate.last_event_hash}
        entry_id = payload.get("entry_id", "")
        relevant_commits = []
        if entry_id in worker.substrate.node_registry:
            relevant_commits = [{"event_hash": h, "prev_hash": b.get("parent_hash")} for h, b in worker.substrate.node_registry[entry_id].commits.items()]

    opa_input = {"input": {"actor": {"id": x_phoenix_node_id}, "chronicle": {"latest_hash": state["last_event_hash"], "events": relevant_commits}, "event": {"payload": payload}}}
    allow = False
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            tmp_path = tf.name; json.dump(opa_input, tf)
        result = await asyncio.to_thread(subprocess.run, ["opa", "eval", "-d", "chronicle_integrity.rego", "-i", tmp_path, "data.phoenix.chronicle.integrity.allow"], capture_output=True, text=True, check=True)
        allow = json.loads(result.stdout)["result"][0]["expressions"][0]["value"]
    except Exception as exc: print(f"[!] OPA evaluation failed: {exc}")
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path): os.remove(tmp_path)

    if not allow:
        worker.substrate.append_dlq({"error_class": "OPA_POLICY_ADMISSION_DENIED", "timestamp_captured": time.time(), "raw_payload": payload, "audit_meta": {"node_origin": x_phoenix_node_id}})
        raise HTTPException(422, "[-] OPA policy denied.")

    try: worker.tx_queue.put_nowait({"action_type": "SUBMIT_PROPOSAL", "payload": payload, "node_id": x_phoenix_node_id})
    except asyncio.QueueFull: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "PROPOSAL_ACCEPTED"}

@router.post("/api/v1/governance/vote", status_code=status.HTTP_202_ACCEPTED)
async def cast_vote(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if not worker.substrate or worker.substrate.is_stasis_active(): raise HTTPException(503, "[-] Stasis active.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)
    try: Draft202012Validator(PHOENIX_VOTE_SCHEMA).validate(instance=payload)
    except ValidationError as err: raise HTTPException(400, f"[-] Vote schema error: {err.message}")
    try: worker.tx_queue.put_nowait({"action_type": "COMMIT_VOTE", "payload": payload, "node_id": x_phoenix_node_id})
    except asyncio.QueueFull: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "VOTE_ACCEPTED"}

@router.post("/api/v1/governance/finalize/{proposal_id}", status_code=status.HTTP_202_ACCEPTED)
async def finalize_proposal(proposal_id: int, request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if not worker.substrate or worker.substrate.is_stasis_active(): raise HTTPException(503, "[-] Stasis active.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)

    with worker.substrate.lock:
        prop = worker.substrate.proposal_registry.get(proposal_id)
        if not prop: raise HTTPException(404, f"[-] Proposal {proposal_id} does not exist.")
        if prop["status"] != "VOTING": raise HTTPException(409, f"[-] Proposal {proposal_id} is not in VOTING state.")
        if (prop["support_stake"] + prop["against_stake"]) < MIN_FINALIZE_STAKE:
            raise HTTPException(422, f"[-] Insufficient stake to finalize.")

    try: worker.tx_queue.put_nowait({"action_type": "FINALIZE_PROPOSAL", "payload": {"proposal_id": proposal_id, **payload}, "node_id": x_phoenix_node_id})
    except asyncio.QueueFull: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "RESOLUTION_QUEUED"}

@router.get("/api/v1/debug/dlq")
def get_dlq(x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...), limit: int = 100):
    if not worker.substrate or x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[x_phoenix_node_id])
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(bytes.fromhex(x_phoenix_signature), f"GET_DLQ_METADATA_BIND_{x_phoenix_node_id}".encode())
    except Exception: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch.")
    with worker.substrate.lock:
        return {"total": len(worker.substrate.dead_letter_queue), "entries": worker.substrate.dead_letter_queue[-limit:]}

@router.get("/api/v1/debug/ledger")
def get_ledger_tail(n: int = 20, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if not worker.substrate or x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[x_phoenix_node_id])
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(bytes.fromhex(x_phoenix_signature), f"GET_LEDGER_METADATA_BIND_{x_phoenix_node_id}".encode())
    except Exception: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch.")
    with worker.substrate.lock:
        tail = list(worker.substrate._ledger)[-min(n, 500):]
        return [e.to_dict() for e in tail]
