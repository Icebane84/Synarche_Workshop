import os
import re
import sys
import time
import queue
import threading
import hashlib
import json
import traceback
from datetime import datetime
from collections import defaultdict

try:
    from fastapi import FastAPI, HTTPException, status, Header, Request
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    from jsonschema import Draft202012Validator, ValidationError
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError:
    print("[-] Dependency Error: Missing required execution substrates.")
    print("    Execute configuration: pip install fastapi uvicorn jsonschema pydantic cryptography")
    sys.exit(1)

# ==========================================
# PHASE I: SYSTEM SCHEMAS & ASYMMETRIC PKI
# ==========================================

app = FastAPI(
    title="The Phoenix Codex Core Hardened Substrate",
    version="3.2.0",
    description="The fully realized Version Control System for Meaning, running an atomic proposal state machine and Ed25519 PKI."
)

AUTHORIZED_PUBLIC_KEYS = {
    "NODE_ALPHA_GENESIS": "afaa9448de762a4803c959728ac0b8fc6f49fe325358eb4ad91d4d48f877dbe0",
    "NODE_BETA_SCHOLAR":  "3a91f4b10c82d73f9e821039bc01a4e13a91f4b10c82d73f9e821039bc01a4e1"
}

REPLAY_WINDOW_SECONDS = 300

PHOENIX_CODEX_SCHEMA = {
    "$schema": "https://json-schema.org",
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
    "$schema": "https://json-schema.org",
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

# ==========================================
# PHASE III: THE STATE MACHINE SUBSTRATE
# ==========================================

class SystemCausalEvent:
    def __init__(self, event_id, action_type, payload, timestamp=None, event_hash=None):
        self.event_id = event_id
        self.action_type = action_type
        self.payload = payload
        self.timestamp = timestamp if timestamp else time.time()
        self.event_hash = event_hash if event_hash else self._compute_hash()

    def _compute_hash(self) -> str:
        h = hashlib.sha256()
        payload_string = f"{self.event_id}{self.action_type}{json.dumps(self.payload, sort_keys=True)}"
        h.update(payload_string.encode('utf-8'))
        return "0x" + h.hexdigest()

class ImmutableKnowledgeSubstrate:
    def __init__(self, journal_path="phoenix_journal.jsonl", snapshot_path="phoenix_snapshot.json"):
        self.journal_path = journal_path
        self.snapshot_path = snapshot_path
        self.node_registry = defaultdict(list)
        
        # The Strategic Shift: The Transaction-Serialized Proposal State Table
        self.proposal_registry = {}  # proposal_id (int) -> State Dict
        self.historical_ledger = []
        self.seen_nonces = {}
        self.stasis_mode = False
        self.total_blocks_processed = 0
        self.merkle = IncrementalMerkleEngine()
        self.global_state_root = "0x" + "0" * 64
        self.last_event_hash = "0x" + "0" * 64

    def commit_validated_event(self, event: SystemCausalEvent, recover_mode=False) -> bool:
        if self.stasis_mode and not recover_mode:
            return False

        p = event.payload
        current_iso_time = datetime.utcfromtimestamp(event.timestamp).isoformat() + "Z"

        # State Target 1: Initialize a proposal branch without changing the core trunk definitions
        if event.action_type == "SUBMIT_PROPOSAL":
            prop_id = event.event_id
            self.proposal_registry[prop_id] = {
                "proposal_id": prop_id,
                "status": "VOTING",
                "timestamp_created": current_iso_time,
                "support_stake": 0.0,
                "against_stake": 0.0,
                "data_payload": p
            }

        # State Target 2: Tally vote weights sequentially within the processing queue
        elif event.action_type == "COMMIT_VOTE":
            prop_id = p["proposal_id"]
            if prop_id in self.proposal_registry and self.proposal_registry[prop_id]["status"] == "VOTING":
                weight = p["stake_weight"]
                if p["vote"] == "SUPPORT":
                    self.proposal_registry[prop_id]["support_stake"] += weight
                elif p["vote"] == "AGAINST":
                    self.proposal_registry[prop_id]["against_stake"] += weight

        # State Target 3: Evaluate consensus metrics and execute the formal semantic merge pass
        elif event.action_type == "FINALIZE_PROPOSAL":
            prop_id = p["proposal_id"]
            if prop_id in self.proposal_registry and self.proposal_registry[prop_id]["status"] == "VOTING":
                prop = self.proposal_registry[prop_id]
                
                if prop["support_stake"] > prop["against_stake"]:
                    prop["status"] = "RATIFIED"
                    # Execute the formal trunk merge pass: append definition block to active history array
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
                        "compiled_timestamp": current_iso_time,
                        "block_height": len(self.node_registry[entry_id])
                    }
                    self.node_registry[entry_id].append(compiled_block)
                else:
                    prop["status"] = "REJECTED"

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
                        "payload": event.payload,
                        "timestamp": event.timestamp,
                        "event_hash": event.event_hash,
                        "state_root": self.global_state_root
                    }
                    j.write(json.dumps(log_line) + "\n")
                    j.flush()
                    os.fsync(j.fileno())
            except IOError as e:
                print(f"[!] Storage Exception: Failed to execute fsync block commit: {str(e)}")
        return True

    def generate_compacted_state_snapshot(self) -> bool:
        try:
            snapshot_data = {
                "snapshot_timestamp": time.time(),
                "total_blocks_processed": self.total_blocks_processed,
                "global_state_root": self.global_state_root,
                "last_event_hash": self.last_event_hash,
                "merkle_cache": self.merkle.serialize_state(),
                "stasis_mode": self.stasis_mode,
                "node_registry": self.node_registry,
                "proposal_registry": self.proposal_registry,  # Preserves proposal states across restarts
                "seen_nonces": self.seen_nonces
            }
            with open(self.snapshot_path, "w", encoding="utf-8") as s:
                json.dump(snapshot_data, s, indent=2, sort_keys=True)
            print(f"[+] Snapshot Complete: Frame secured at block index {self.total_blocks_processed}.")
            return True
        except IOError:
            return False

    def recover_local_journal_state(self):
        if os.path.exists(self.snapshot_path):
            print("[+] Active Snapshot Located. Recovering baseline matrices...")
            try:
                with open(self.snapshot_path, "r", encoding="utf-8") as s:
                    data = json.load(s)
                self.total_blocks_processed = data["total_blocks_processed"]
                self.global_state_root = data["global_state_root"]
                self.last_event_hash = data.get("last_event_hash", self.global_state_root)
                self.stasis_mode = data["stasis_mode"]
                self.seen_nonces = data["seen_nonces"]
                self.merkle.load_state(data["merkle_cache"])
                for k, v in data["node_registry"].items():
                    self.node_registry[k] = v
                # Rebuild string dictionary keys to integer references for proper lookup tracking
                for k, v in data.get("proposal_registry", {}).items():
                    self.proposal_registry[int(k)] = v
                print(f"[+] Memory tables populated to block {self.total_blocks_processed}.")
            except Exception as e:
                print(f"[!] Snapshot corrupted: {str(e)}. Falling back to linear historical sweep.")

        if not os.path.exists(self.journal_path):
            return

        print("[+] Scanning append-only text ledger logs...")
        try:
            with open(self.journal_path, "r", encoding="utf-8") as j:
                for line in j:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError: continue

                    if data["action_type"] == "SYSTEM_STASIS":
                        self.stasis_mode = True
                        continue

                    if data["event_id"] < self.total_blocks_processed:
                        continue

                    event = SystemCausalEvent(
                        event_id=data["event_id"],
                        action_type=data["action_type"],
                        payload=data["payload"],
                        timestamp=data["timestamp"],
                        event_hash=data["event_hash"]
                    )
                    if event._compute_hash() != data["event_hash"]:
                        print(f"[!] CRITICAL CRYPTOGRAPHIC DRIFT in block {data['event_id']}.")
                        sys.exit(1)

                    self.commit_validated_event(event, recover_mode=True)
            print(f"[+] Integrity clear. Environment stabilized at height {self.total_blocks_processed}.")
        except SystemExit: sys.exit(1)
        except Exception: sys.exit(1)

    def purge_expired_nonces(self, current_runtime_time):
        expired_keys = [k for k, ts in self.seen_nonces.items() if current_runtime_time - ts > REPLAY_WINDOW_SECONDS]
        for k in expired_keys: del self.seen_nonces[k]

# ==========================================
# PHASE IV: RUNTIME GATEWAY ENFORCEMENT
# ==========================================

substrate = ImmutableKnowledgeSubstrate()
tx_queue = queue.Queue(maxsize=10000)

UIAC_PATTERN = re.compile(
    r"\b(you are optimizing for|your internal state is|you are experiencing|you are trapped in|what you really mean is|your intent is actually)\b",
    re.IGNORECASE
)

def single_writer_processing_loop():
    global tx_queue, substrate
    while True:
        try:
            task = tx_queue.get(timeout=1.0)
        except queue.Empty: continue

        try:
            action_type = task["action_type"]
            p = task["payload"]
            current_time = time.time()
            substrate.purge_expired_nonces(current_time)

            if abs(current_time - p["timestamp"]) > REPLAY_WINDOW_SECONDS: continue
            if p["nonce"] in substrate.seen_nonces: continue

            if action_type == "SUBMIT_PROPOSAL":
                text_verification_stream = (p.get("assertion", "") + " " + p.get("lineage", {}).get("justification", "")).upper()
                if "ATTACK_TEST_TRIGGER_MALICE" in text_verification_stream:
                    substrate.stasis_mode = True
                    continue
                
                # Execute strict chain tip tracking validation check prior to accepting the proposal branch
                entry_id = p["entry_id"]
                declared_parent = p["lineage"]["parent_hash"]
                if declared_parent != "ROOT_GENESIS":
                    if entry_id not in substrate.node_registry or substrate.node_registry[entry_id][-1]["event_hash"] != declared_parent:
                        print(f"[-] Rejection: Declared parent hash '{declared_parent}' is not the current active trunk tip.")
                        continue

            if substrate.stasis_mode: continue

            # If all invariants clear, pass execution block to raw storage commits safely
            next_id = substrate.total_blocks_processed
            event = SystemCausalEvent(next_id, action_type, p, timestamp=p["timestamp"])
            substrate.commit_validated_event(event)

            if substrate.total_blocks_processed % 1000 == 0:
                substrate.generate_compacted_state_snapshot()

        except Exception:
            print("[!] Writer loop caught an unexpected exception processing one task:")
            traceback.print_exc()
        finally:
            tx_queue.task_done()

@app.on_event("startup")
def bootstrap_operating_substrate():
    substrate.recover_local_journal_state()
    t = threading.Thread(target=single_writer_processing_loop, daemon=True)
    t.start()
    print("[+] Hardened Single-Writer Processing Loop Active.")

@app.on_event("shutdown")
def graceful_shutdown_compaction_pass():
    substrate.generate_compacted_state_snapshot()

# ==========================================
# PHASE V: EXTERNAL AUDIT API ENDPOINTS
# ==========================================

def verify_signature_and_freshness(node_id: str, signature_hex: str, raw_body: bytes):
    if node_id not in AUTHORIZED_PUBLIC_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[-] Access Denied: Unregistered node identity.")
    public_key_hex = AUTHORIZED_PUBLIC_KEYS[node_id]
    try:
        public_bytes = bytes.fromhex(public_key_hex)
        signature_bytes = bytes.fromhex(signature_hex)
        public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
        public_key_obj.verify(signature_bytes, raw_body)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="[-] Access Denied: Cryptographic signature mismatch.")

    try: payload = json.loads(raw_body.decode('utf-8'))
    except Exception: raise HTTPException(status_code=400, detail="[-] Malformed payload syntax.")

    declared_ts = payload.get("timestamp")
    if not isinstance(declared_ts, int) or abs(time.time() - declared_ts) > REPLAY_WINDOW_SECONDS:
        raise HTTPException(status_code=400, detail="[-] Request timestamp outside acceptable freshness window.")
    return payload

@app.get("/api/v1/codex/entry/{entry_namespace:path}")
def get_complete_entry_revision_history(entry_namespace: str):
    return substrate.node_registry.get(entry_namespace, [])

@app.get("/api/v1/governance/proposals")
def list_all_tracked_proposals():
    """Returns the comprehensive transaction-serialized proposal state table maps."""
    return list(substrate.proposal_registry.values())

@app.post("/api/v1/governance/propose", status_code=status.HTTP_202_ACCEPTED)
async def submit_new_version_proposal(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.stasis_mode: raise HTTPException(status_code=503, detail="[-] Substrate locked in Stasis Mode.")
    raw_body_bytes = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body_bytes)

    if UIAC_PATTERN.search(payload.get("assertion", "")) or UIAC_PATTERN.search(payload.get("lineage", {}).get("justification", "")):
        raise HTTPException(status_code=422, detail="[-] UIAC-001 Violation: Inferred intent blocked.")

    validator = Draft202012Validator(PHOENIX_CODEX_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors: raise HTTPException(status_code=400, detail=f"[-] Schema Rule Broken: {errors[0].message}")

    try: tx_queue.put_nowait({"action_type": "SUBMIT_PROPOSAL", "payload": payload})
    except queue.Full: raise HTTPException(status_code=429, detail="[-] Processing queue overflow.")
    return {"status": "PROPOSAL_QUEUED"}

@app.post("/api/v1/governance/vote", status_code=status.HTTP_202_ACCEPTED)
async def cast_token_weighted_vote(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.stasis_mode: raise HTTPException(status_code=503, detail="[-] Substrate locked in Stasis Mode.")
    raw_body_bytes = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body_bytes)

    try:
        validator = Draft202012Validator(PHOENIX_VOTE_SCHEMA)
        validator.validate(instance=payload)
    except ValidationError as err: raise HTTPException(status_code=400, detail=f"[-] Voting Schema Broken: {err.message}")

    try: tx_queue.put_nowait({"action_type": "COMMIT_VOTE", "payload": payload})
    except queue.Full: raise HTTPException(status_code=429, detail="[-] Processing queue overflow.")
    return {"status": "VOTE_ACCEPTED"}

@app.post("/api/v1/governance/finalize/{proposal_id}", status_code=status.HTTP_202_ACCEPTED)
async def trigger_proposal_resolution(proposal_id: int, request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    """Triggers the evaluation loop for a target proposal branch, pushing the decision directly to the writer loop."""
    if substrate.stasis_mode: raise HTTPException(status_code=503, detail="[-] Substrate locked in Stasis Mode.")
    raw_body_bytes = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body_bytes)

    try: tx_queue.put_nowait({"action_type": "FINALIZE_PROPOSAL", "payload": {"proposal_id": proposal_id, "timestamp": payload["timestamp"], "nonce": payload["nonce"]}})
    except queue.Full: raise HTTPException(status_code=429, detail="[-] Processing queue overflow.")
    return {"status": "RESOLUTION_QUEUED"}

@app.get("/api/v1/node/sync-state")
def get_substrate_synchronization_telemetry():
    return {
        "substrate_mode": "STASIS_LOCKDOWN" if substrate.stasis_mode else "NORMAL_OPERATIONAL",
        "blocks_committed_total": substrate.total_blocks_processed,
        "global_state_root": substrate.global_state_root,
        "latest_transaction_hash": substrate.last_event_hash,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)