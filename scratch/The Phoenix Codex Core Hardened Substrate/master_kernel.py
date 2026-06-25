import os
import re
import sys
import time
import queue
import threading
import hashlib
import json
import traceback
import asyncio
import subprocess
from datetime import datetime
from collections import defaultdict

try:
    from fastapi import FastAPI, HTTPException, status, Header, Request, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel
    from jsonschema import Draft202012Validator, ValidationError
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError:
    print("[-] Dependency Error: Missing required execution substrates.")
    print("    Execute configuration: pip install fastapi uvicorn jsonschema pydantic cryptography")
    sys.exit(1)

# ==========================================
# PHASE I: SYSTEM SCHEMAS & CRYPTO PKI
# ==========================================

app = FastAPI(
    title="The Phoenix Codex Core Hardened Substrate",
    version="3.7.0",
    description="The complete Git-for-Meaning framework running active OPA admission gates and automated DLQ routing."
)

MAIN_EVENT_LOOP = None

AUTHORIZED_PUBLIC_KEYS = {
    "NODE_ALPHA_GENESIS": "afaa9448de762a4803c959728ac0b8fc6f49fe325358eb4ad91d4d48f877dbe0",
    "NODE_BETA_SCHOLAR":  "e50719d0a9e0206fe40a9553fe8dce0680ead8b1507df410da49902207169d05"
}

_PLACEHOLDER_PUBLIC_KEY = "NEVER_MATCHES_REAL_KEY_PLACEHOLDER"
if _PLACEHOLDER_PUBLIC_KEY in AUTHORIZED_PUBLIC_KEYS.values():
    print("[-] CRITICAL CONFIGURATION FAULT: AUTHORIZED_PUBLIC_KEYS contains un-modified example placeholders.")
    sys.exit(1)

REPLAY_WINDOW_SECONDS = 300

UIAC_PATTERN = re.compile(
    r"\b(you are optimizing for|your internal state is|you are experiencing|"
    r"you are trapped in|what you really mean is|your intent is actually)\b",
    re.IGNORECASE
)

PHOENIX_CODEX_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "entry_id": {"type": "string", "pattern": "^codex\\.[a-z\\.]+\\/[a-z0-9\\-]+$"},
        "term": {"type": "string", "minLength": 2, "maxLength": 64},
        "assertion": {"type": "string", "minLength": 10, "maxLength": 1000},
        "nonce": {"type": "string", "minLength": 8, "maxLength": 128},
        "timestamp": {"type": "integer", "minimum": 0},
        "lineage": {
            "type": "object",
            "properties": {
                "parent_hash": {"type": "string", "pattern": "^(0x[a-fA-F0-9]{64}|ROOT_GENESIS)$"},
                "causal_trigger": {"type": "string"},
                "justification": {"type": "string", "minLength": 20, "maxLength": 2000}
            },
            "required": ["parent_hash", "causal_trigger", "justification"]
        }
    },
    "required": ["entry_id", "term", "assertion", "nonce", "timestamp", "lineage"]
}

PHOENIX_VOTE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "proposal_id": {"type": "integer", "minimum": 0},
        "vote": {"type": "string", "pattern": "^(SUPPORT|AGAINST)$"},
        "stake_weight": {"type": "number", "minimum": 0.0},
        "nonce": {"type": "string", "minLength": 8, "maxLength": 128},
        "timestamp": {"type": "integer", "minimum": 0}
    },
    "required": ["proposal_id", "vote", "stake_weight", "nonce", "timestamp"]
}

class ProofVerificationRequest(BaseModel):
    leaf_hash_hex: str
    proof: list
    root_hash_hex: str

# ==========================================
# PHASE II: MERKLE CRYPTOGRAPHIC ENGINE
# ==========================================

LEAF_PREFIX = b'\x00'
INNER_PREFIX = b'\x01'

class IncrementalMerkleEngine:
    def __init__(self):
        self.cached_levels = []

    def serialize_state(self) -> list:
        return [[h.hex() for h in level] for level in self.cached_levels]

    def load_state(self, state_list: list):
        self.cached_levels = [[bytes.fromhex(h) for h in level] for level in state_list]

    def _hash_leaf(self, raw_event_hash: bytes) -> bytes:
        h = hashlib.sha256()
        h.update(LEAF_PREFIX + raw_event_hash)
        return h.digest()

    def _hash_inner(self, left_raw: bytes, right_raw: bytes) -> bytes:
        h = hashlib.sha256()
        h.update(INNER_PREFIX + left_raw + right_raw)
        return h.digest()

    def append_event_hash(self, event_hash_hex: str) -> str:
        raw_event = bytes.fromhex(event_hash_hex.replace("0x", ""))
        new_leaf = self._hash_leaf(raw_event)
        if not self.cached_levels:
            self.cached_levels.append([])
        self.cached_levels[0].append(new_leaf)
        raw_root = self._recalculate_right_edge()
        return "0x" + raw_root.hex()

    def _recalculate_right_edge(self) -> bytes:
        current_idx = len(self.cached_levels[0]) - 1
        curr_level = 0
        while True:
            if curr_level == len(self.cached_levels) - 1 and len(self.cached_levels[curr_level]) == 1:
                return self.cached_levels[curr_level][0]
            is_left_node = (current_idx % 2 == 0)
            if is_left_node:
                left_raw = self.cached_levels[curr_level][current_idx]
                right_raw = left_raw
            else:
                left_raw = self.cached_levels[curr_level][current_idx - 1]
                right_raw = self.cached_levels[curr_level][current_idx]
            parent_raw = self._hash_inner(left_raw, right_raw)
            if curr_level + 1 >= len(self.cached_levels):
                self.cached_levels.append([])
            parent_level_idx = current_idx // 2
            if parent_level_idx < len(self.cached_levels[curr_level + 1]):
                self.cached_levels[curr_level + 1][parent_level_idx] = parent_raw
            else:
                self.cached_levels[curr_level + 1].append(parent_raw)
            current_idx = parent_level_idx
            curr_level += 1

    def generate_merkle_proof(self, leaf_index: int) -> list:
        if not self.cached_levels or leaf_index < 0 or leaf_index >= len(self.cached_levels[0]):
            return []
        proof = []
        curr_idx = leaf_index
        for level in range(len(self.cached_levels) - 1):
            is_left_node = (curr_idx % 2 == 0)
            if is_left_node:
                if curr_idx + 1 < len(self.cached_levels[level]):
                    proof.append((1, self.cached_levels[level][curr_idx + 1].hex()))
                else:
                    proof.append((2, self.cached_levels[level][curr_idx].hex()))
            else:
                proof.append((0, self.cached_levels[level][curr_idx - 1].hex()))
            curr_idx //= 2
        return proof

def verify_merkle_proof(leaf_hash_hex: str, proof: list, root_hash_hex: str) -> bool:
    try:
        curr_raw = hashlib.sha256(LEAF_PREFIX + bytes.fromhex(leaf_hash_hex.replace("0x", ""))).digest()
        for direction, sibling_hex in proof:
            sibling_raw = bytes.fromhex(sibling_hex)
            h = hashlib.sha256()
            if direction == 1: h.update(INNER_PREFIX + curr_raw + sibling_raw)
            elif direction == 0: h.update(INNER_PREFIX + sibling_raw + curr_raw)
            elif direction == 2: h.update(INNER_PREFIX + curr_raw + curr_raw)
            else: return False
            curr_raw = h.digest()
        return "0x" + curr_raw.hex() == root_hash_hex
    except Exception: return False

# ==========================================
# PHASE III: FORK-AWARE ONTOLOGY DATA STORE
# ==========================================

class SemanticEntryGraph:
    def __init__(self):
        self.commits = {}                    
        self.refs = {"main": "ROOT_GENESIS"} 

    def to_dict(self) -> dict:
        return {"commits": self.commits, "refs": self.refs}

    @classmethod
    def from_dict(cls, data: dict):
        graph = cls()
        graph.commits = data.get("commits", {})
        graph.refs = data.get("refs", {"main": "ROOT_GENESIS"})
        return graph

class SystemCausalEvent:
    def __init__(self, event_id, action_type, payload, node_id="LOCAL", timestamp=None, event_hash=None):
        self.event_id = event_id
        self.action_type = action_type
        self.payload = payload
        self.node_id = node_id
        self.timestamp = timestamp if timestamp else time.time()
        self.event_hash = event_hash if event_hash else self._compute_hash()

    def _compute_hash(self) -> str:
        h = hashlib.sha256()
        payload_string = f"{self.event_id}{self.action_type}{self.node_id}{json.dumps(self.payload, sort_keys=True)}"
        h.update(payload_string.encode('utf-8'))
        return "0x" + h.hexdigest()

class ImmutableKnowledgeSubstrate:
    def __init__(self, journal_path="phoenix_journal.jsonl", snapshot_path="phoenix_snapshot.json"):
        self.journal_path = journal_path
        self.snapshot_path = snapshot_path
        self.node_registry = {}  
        self.proposal_registry = {}
        self.historical_ledger = []
        self.seen_nonces = {}
        self.quarantined_peers = set()
        self._stasis_event = threading.Event()
        
        # Operational Blueprint Realization: Instantiate active database tracking tables
        self.aistf_transactions = []  # Explicit LAW-035 Transaction Table
        self.dead_letter_queue = []   # Explicit LAW-030 Dead Letter Queue Table
        self.genesis_hash = "0x" + "0" * 64

        self.total_blocks_processed = 0
        self.merkle = IncrementalMerkleEngine()
        self.global_state_root = "0x" + "0" * 64
        self.last_event_hash = "0x" + "0" * 64

    def is_stasis_active(self) -> bool:
        return self._stasis_event.is_set()

    def set_stasis_lockdown(self):
        self._stasis_event.set()

    def commit_validated_event(self, event: SystemCausalEvent, recover_mode=False) -> bool:
        if self.is_stasis_active() and not recover_mode:
            return False

        p = event.payload
        current_iso_time = datetime.utcfromtimestamp(event.timestamp).isoformat() + "Z"

        if event.action_type == "SUBMIT_PROPOSAL":
            prop_id = event.event_id
            self.proposal_registry[prop_id] = {
                "proposal_id": prop_id,
                "status": "VOTING",
                "node_origin": event.node_id,
                "timestamp_created": current_iso_time,
                "support_stake": 0.0,
                "against_stake": 0.0,
                "data_payload": p
            }

        elif event.action_type == "COMMIT_VOTE":
            prop_id = p["proposal_id"]
            if prop_id in self.proposal_registry and self.proposal_registry[prop_id]["status"] == "VOTING":
                weight = p["stake_weight"]
                if p["vote"] == "SUPPORT": self.proposal_registry[prop_id]["support_stake"] += weight
                elif p["vote"] == "AGAINST": self.proposal_registry[prop_id]["against_stake"] += weight

        elif event.action_type == "FINALIZE_PROPOSAL":
            prop_id = p["proposal_id"]
            if prop_id in self.proposal_registry and self.proposal_registry[prop_id]["status"] == "VOTING":
                prop = self.proposal_registry[prop_id]
                if prop["support_stake"] > prop["against_stake"]:
                    prop["status"] = "RATIFIED"
                    node_data = prop["data_payload"]
                    entry_id = node_data["entry_id"]
                    
                    compiled_block = {
                        "entry_id": entry_id,
                        "term": node_data["term"],
                        "assertion": node_data["assertion"],
                        "parent_hash": node_data["lineage"]["parent_hash"],
                        "causal_trigger": node_data["lineage"]["causal_trigger"],
                        "justification": node_data["lineage"]["justification"],
                        "event_hash": event.event_hash,
                        "compiled_timestamp": current_iso_time
                    }
                    if entry_id not in self.node_registry:
                        self.node_registry[entry_id] = SemanticEntryGraph()
                    graph = self.node_registry[entry_id]
                    graph.commits[event.event_hash] = compiled_block
                    graph.refs[f"refs/proposals/{prop_id}"] = event.event_hash
                    graph.refs["main"] = event.event_hash 

                    # Architectural Lock: Commit records directly into the chronicle table on ratification
                    self.aistf_transactions.append({
                        "block_id": event.event_id,
                        "event_hash": event.event_hash,
                        "previous_hash": self.last_event_hash,
                        "timestamp_committed": current_iso_time
                    })
                else:
                    prop["status"] = "REJECTED"

        elif event.action_type == "REGISTER_FORK":
            entry_id = p["entry_id"]
            if entry_id not in self.node_registry:
                self.node_registry[entry_id] = SemanticEntryGraph()
            graph = self.node_registry[entry_id]
            graph.commits[p["compiled_block"]["event_hash"]] = p["compiled_block"]
            graph.refs[p["branch_name"]] = p["compiled_block"]["event_hash"]

        self.historical_ledger.append(event)
        if "nonce" in p:
            self.seen_nonces[p["nonce"]] = p["timestamp"]
        self.total_blocks_processed += 1
        self.global_state_root = self.merkle.append_event_hash(event.event_hash)
        self.last_event_hash = event.event_hash

        if not recover_mode:
            try:
                with open(self.journal_path, "a", encoding="utf-8") as j:
                    log_line = {
                        "event_id": event.event_id,
                        "action_type": event.action_type,
                        "node_id": event.node_id,
                        "payload": event.payload,
                        "timestamp": event.timestamp,
                        "event_hash": event.event_hash,
                        "state_root": self.global_state_root
                    }
                    j.write(json.dumps(log_line) + "\n")
                    j.flush()
                    os.fsync(j.fileno())
            except IOError as e:
                print(f"[!] Storage Exception: Failed to execute fsync: {str(e)}")
        return True

    def generate_compacted_state_snapshot(self) -> bool:
        try:
            flattened_graphs = {k: v.to_dict() for k, v in self.node_registry.items()}
            snapshot_data = {
                "snapshot_timestamp": time.time(),
                "total_blocks_processed": self.total_blocks_processed,
                "global_state_root": self.global_state_root,
                "last_event_hash": self.last_event_hash,
                "merkle_cache": self.merkle.serialize_state(),
                "stasis_mode": self.is_stasis_active(),
                "node_registry": flattened_graphs,
                "proposal_registry": self.proposal_registry,
                "aistf_transactions": self.aistf_transactions,
                "seen_nonces": self.seen_nonces
            }
            raw_blob = json.dumps(snapshot_data, sort_keys=True)
            snapshot_hash = hashlib.sha256(raw_blob.encode()).hexdigest()
            
            payload_with_attestation = {
                "manifest_integrity_hash": snapshot_hash,
                "snapshot_payload": snapshot_data
            }
            with open(self.snapshot_path, "w", encoding="utf-8") as s:
                json.dump(payload_with_attestation, s, indent=2, sort_keys=True)
            return True
        except IOError: return False

    def recover_local_journal_state(self):
        if os.path.exists(self.snapshot_path):
            print("[+] Active Snapshot Located. Executing manifest integrity check...")
            try:
                with open(self.snapshot_path, "r", encoding="utf-8") as s:
                    wrapper = json.load(s)
                raw_blob = json.dumps(wrapper["snapshot_payload"], sort_keys=True)
                recomputed_hash = hashlib.sha256(raw_blob.encode()).hexdigest()
                if recomputed_hash != wrapper["manifest_integrity_hash"]:
                    raise ValueError("Snapshot validation failed.")

                data = wrapper["snapshot_payload"]
                self.total_blocks_processed = data["total_blocks_processed"]
                self.global_state_root = data["global_state_root"]
                self.last_event_hash = data.get("last_event_hash", self.global_state_root)
                if data["stasis_mode"]: self.set_stasis_lockdown()
                self.seen_nonces = data["seen_nonces"]
                self.merkle.load_state(data["merkle_cache"])
                self.aistf_transactions = data.get("aistf_transactions", [])
                
                for k, v in data["node_registry"].items():
                    self.node_registry[k] = SemanticEntryGraph.from_dict(v)
                for k, v in data.get("proposal_registry", {}).items():
                    self.proposal_registry[int(k)] = v
                print(f"[+] Snapshot verified. Re-anchored graph up to block height {self.total_blocks_processed}.")
            except Exception as e:
                print(f"[!] Snapshot bypassed: {str(e)}. Executing full journal sweep.")

        if not os.path.exists(self.journal_path): return
        try:
            with open(self.journal_path, "r", encoding="utf-8") as j:
                for line in j:
                    if not line.strip(): continue
                    try: data = json.loads(line)
                    except json.JSONDecodeError: continue

                    if data["action_type"] == "SYSTEM_STASIS":
                        self.set_stasis_lockdown()
                        continue
                    if data["event_id"] <= self.total_blocks_processed: continue

                    event = SystemCausalEvent(
                        event_id=data["event_id"],
                        action_type=data["action_type"],
                        payload=data["payload"],
                        node_id=data.get("node_id", "UNKNOWN"),
                        timestamp=data["timestamp"],
                        event_hash=data["event_hash"]
                    )
                    if event._compute_hash() != data["event_hash"]:
                        sys.exit(1)
                    self.commit_validated_event(event, recover_mode=True)
        except Exception: sys.exit(1)

    def purge_expired_nonces(self, current_time):
        expired = [k for k, ts in self.seen_nonces.items() if current_time - ts > REPLAY_WINDOW_SECONDS]
        for k in expired: del self.seen_nonces[k]

# ==========================================
# PHASE IV: NET REPLICATION PLANE (WORKER)
# ==========================================

def single_writer_processing_loop():
    """The Authoritative Writer Thread. Implements thread-safe atomic branch conflict parsing."""
    global tx_queue, substrate, active_sockets

    while True:
        try: hash_task = tx_queue.get(timeout=1.0)
        except queue.Empty: continue

        try:
            action_type = hash_task["action_type"]
            p = hash_task["payload"]
            node_origin = hash_task.get("node_id", "LOCAL")

            current_time = time.time()
            substrate.purge_expired_nonces(current_time)

            if abs(current_time - p.get("timestamp", 0)) > REPLAY_WINDOW_SECONDS: continue
            if p.get("nonce") in substrate.seen_nonces: continue
            if substrate.is_stasis_active(): continue

            if action_type == "SUBMIT_PROPOSAL":
                entry_id = p.get("entry_id")
                declared_parent = p.get("lineage", {}).get("parent_hash")

                if declared_parent != "ROOT_GENESIS" and entry_id in substrate.node_registry:
                    graph = substrate.node_registry[entry_id]
                    current_tip_hash = graph.refs["main"]

                    if declared_parent != current_tip_hash:
                        if declared_parent not in graph.commits:
                            print(f"[-] Fork Rejected: Declared parent '{declared_parent}' is missing from the DAG store.")
                            continue
                        
                        conflicting_tip_block = graph.commits[current_tip_hash]
                        try:
                            tip_ts = datetime.fromisoformat(conflicting_tip_block["compiled_timestamp"].replace("Z", "+00:00")).timestamp()
                        except Exception: 
                            tip_ts = 0.0

                        incoming_ts = float(p.get("timestamp", 0))
                        if incoming_ts > tip_ts or (incoming_ts == tip_ts and node_origin > conflicting_tip_block.get("causal_trigger", "")):
                            print("[-] Branch Isolated: Alternative history route intercepted. Committing fork branch.")
                            
                            fork_id = substrate.total_blocks_processed
                            fork_hash = hashlib.sha256(f"{fork_id}REGISTER_FORK{node_origin}{json.dumps(p, sort_keys=True)}".encode('utf-8')).hexdigest()
                            
                            compiled_block = {
                                "entry_id": entry_id,
                                "term": p["term"],
                                "assertion": p["assertion"],
                                "parent_hash": declared_parent,
                                "causal_trigger": f"FORK_ISOLATION_{node_origin}",
                                "justification": p["lineage"]["justification"],
                                "event_hash": f"0x{fork_hash}",
                                "compiled_timestamp": datetime.utcfromtimestamp(incoming_ts).isoformat() + "Z"
                            }
                            
                            fork_payload = {
                                "entry_id": entry_id,
                                "branch_name": f"refs/forks/{fork_hash[:8]}",
                                "compiled_block": compiled_block,
                                "timestamp": p["timestamp"],
                                "nonce": p["nonce"]
                            }
                            
                            event = SystemCausalEvent(fork_id, "REGISTER_FORK", fork_payload, node_id=node_origin, timestamp=p["timestamp"])
                            substrate.commit_validated_event(event)
                            continue
                        elif incoming_ts == tip_ts and node_origin <= conflicting_tip_block.get("causal_trigger", ""):
                            print("[-] Branch Isolated: Lost lexicographical tie-breaker loop. Halting canonical integration path.")
                            continue

            next_id = substrate.total_blocks_processed
            event = SystemCausalEvent(next_id, action_type, p, node_id=node_origin, timestamp=p["timestamp"])
            substrate.commit_validated_event(event)

            if node_origin == "LOCAL":
                gossip_packet = json.dumps({"action_type": action_type, "payload": p, "node_id": "LOCAL"})
                with _sockets_lock: sockets_snapshot = set(active_sockets)
                for sock in sockets_snapshot:
                    _safe_broadcast(sock, gossip_packet)

            if substrate.total_blocks_processed % 1000 == 0:
                substrate.generate_compacted_state_snapshot()

        except Exception:
            print("[!] Writer loop caught unexpected exception:")
            traceback.print_exc()
        finally: tx_queue.task_done()

def _safe_broadcast(sock, message: str):
    global MAIN_EVENT_LOOP
    if MAIN_EVENT_LOOP is None:
        return
    future = asyncio.run_coroutine_threadsafe(sock.send_text(message), MAIN_EVENT_LOOP)
    def _on_broadcast_done(f):
        if f.exception():
            with _sockets_lock:
                active_sockets.discard(sock)
    future.add_done_callback(_on_broadcast_done)

# ==========================================
# PHASE V: API GATEWAY & P2P ROUTING
# ==========================================

def verify_signature_and_freshness(node_id: str, signature_hex: str, raw_body: bytes) -> dict:
    if node_id not in AUTHORIZED_PUBLIC_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[-] Access Denied: Unregistered node identity.")
    try:
        pub_bytes = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[node_id])
        sig_bytes = bytes.fromhex(signature_hex)
        ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes).verify(sig_bytes, raw_body)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[-] Access Denied: Signature mismatch.")
    try: payload = json.loads(raw_body.decode("utf-8"))
    except Exception: raise HTTPException(status_code=400, detail="[-] Malformed payload syntax.")
    declared_ts = payload.get("timestamp")
    if not isinstance(declared_ts, int) or abs(time.time() - declared_ts) > REPLAY_WINDOW_SECONDS:
        raise HTTPException(status_code=400, detail="[-] Timestamp outside freshness window.")
    return payload

@app.on_event("startup")
async def bootstrap_operating_substrate():
    global MAIN_EVENT_LOOP
    MAIN_EVENT_LOOP = asyncio.get_running_loop() 
    substrate.recover_local_journal_state()
    t = threading.Thread(target=single_writer_processing_loop, daemon=True)
    t.start()
    print("[+] Fork-Aware OPA Kernel Substrate Pipeline Fully Active.")

@app.on_event("shutdown")
def graceful_shutdown():
    substrate.generate_compacted_state_snapshot()

@app.websocket("/api/v1/network/sync")
async def websocket_p2p_synchronization_endpoint(websocket: WebSocket, x_phoenix_node_id: str = Header(...)):
    global active_sockets, substrate
    if x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    if x_phoenix_node_id in substrate.quarantined_peers:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    with _sockets_lock: active_sockets.add(websocket)
    print(f"[+] P2P Substrate Connection Established with Peer Node: {x_phoenix_node_id}")

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                packet = json.loads(raw_data)
                action_type = packet.get("action_type")
                payload = packet.get("payload", {})
                if not action_type or not isinstance(payload, dict):
                    continue
            except (json.JSONDecodeError, AttributeError, TypeError):
                continue

            sender_id = x_phoenix_node_id 
            if sender_id in substrate.quarantined_peers: continue
            if payload.get("nonce") in substrate.seen_nonces: continue

            try:
                tx_queue.put_nowait({"action_type": action_type, "payload": payload, "node_id": sender_id})
            except queue.Full:
                print(f"[-] Backpressure Engaged: Dropped message stream from node {sender_id}")
    except WebSocketDisconnect:
        print(f"[-] P2P Stream Terminated for Peer Node: {x_phoenix_node_id}")
    finally:
        with _sockets_lock:
            if websocket in active_sockets: active_sockets.remove(websocket)

@app.get("/api/v1/codex/entry/{entry_namespace:path}")
def get_complete_branch_ontology_history(entry_namespace: str):
    if entry_namespace not in substrate.node_registry:
        raise HTTPException(status_code=404, detail="[-] Namespace missing from active memory registries.")
    return substrate.node_registry[entry_namespace].to_dict()

@app.get("/api/v1/debug/dlq")
def get_dead_letter_queue_registry():
    """Exposes the internal LAW-030 Dead Letter Queue table registry maps for manual inspection."""
    return substrate.dead_letter_queue

@app.post("/api/v1/governance/propose", status_code=status.HTTP_202_ACCEPTED)
async def submit_new_version_proposal(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.is_stasis_active(): raise HTTPException(status_code=503, detail="[-] Substrate locked in Stasis Mode.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)

    if UIAC_PATTERN.search(payload.get("assertion", "")) or UIAC_PATTERN.search(payload.get("lineage", {}).get("justification", "")):
        raise HTTPException(status_code=422, detail="[-] UIAC-001 Violation: Inferred intent attribution blocked.")

    # 1. Structural Schema Validation Check
    validator = Draft202012Validator(PHOENIX_CODEX_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        # LAW-030 Trigger: Route structural schema validation rejections straight into the system DLQ
        dlq_entry = {
            "error_class": "SCHEMA_VALIDATION_FAILURE",
            "timestamp_captured": time.time(),
            "raw_payload": payload,
            "audit_meta": {"node_origin": x_phoenix_node_id, "reason": errors[0].message}
        }
        substrate.dead_letter_queue.append(dlq_entry)
        raise HTTPException(status_code=400, detail=f"[-] Schema Rule Broken: {errors[0].message}")

    # 2. LAW-035 OPA Admission Policy Evaluation Gate 
    opa_input_context = {
        "input": {
            "operation": "append_event", [cite: 1]
            "actor": {"id": x_phoenix_node_id, "role": "ARCHITECT"}, [cite: 2, 3]
            "chronicle": {
                "genesis_hash": substrate.genesis_hash, [cite: 3, 5]
                "latest_hash": substrate.last_event_hash, [cite: 3]
                "events": [{"event_hash": e.event_hash, "prev_hash": e.payload.get("lineage", {}).get("parent_hash")} for e in substrate.historical_ledger]
            },
            "event": {
                "id": f"evt_{payload['nonce'][:8]}", [cite: 3, 5]
                "artifact_id": "CORE.CODEX.PhoenixSchema", [cite: 3, 5]
                "law_id": "LAW-035", [cite: 3, 5]
                "type": "APPEND", [cite: 3, 4, 5]
                "timestamp": datetime.utcfromtimestamp(payload["timestamp"]).isoformat() + "Z", [cite: 3, 5]
                "prev_hash": payload["lineage"]["parent_hash"], [cite: 3, 5]
                "content_hash": hashlib.sha256(raw_body).hexdigest(), [cite: 3, 5]
                "event_hash": substrate.last_event_hash, [cite: 3, 5]
                "payload": payload, [cite: 3]
                "signatures": [{"role": "ARCHITECT", "signature": x_phoenix_signature}] [cite: 3]
            }
        }
    }

    try:
        with open("temp_input.json", "w") as f:
            json.dump(opa_input_context, f)
            
        cmd = ["opa", "eval", "-d", "chronicle_integrity.rego", "-i", "temp_input.json", "data.phoenix.chronicle.integrity.allow"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        opa_output = json.loads(result.stdout)
        allow_decision = opa_output["result"][0]["expressions"][0]["value"]
    except Exception as e:
        allow_decision = False
        print(f"[!] Policy Engine Execution Failure: {str(e)}")
    finally:
        if os.path.exists("temp_input.json"):
            os.remove("temp_input.json")

    if not allow_decision:
        # LAW-030 Trigger: Route policy validation rejections straight into the system DLQ
        dlq_entry = {
            "error_class": "OPA_POLICY_ADMISSION_DENIED",
            "timestamp_captured": time.time(),
            "raw_payload": payload,
            "audit_meta": {"node_origin": x_phoenix_node_id, "reason": "Failed chronicle_integrity.rego constraints."}
        }
        substrate.dead_letter_queue.append(dlq_entry)
        raise HTTPException(status_code=422, detail="[-] Security Perimeter Access Denied: OPA rules check failed.")

    try: 
        tx_queue.put_nowait({"action_type": "SUBMIT_PROPOSAL", "payload": payload, "node_id": x_phoenix_node_id})
    except queue.Full: raise HTTPException(status_code=429, detail="[-] Processing queue overflow.")
    return {"status": "PROPOSAL_ACCEPTED"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)