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
import tempfile
from collections import deque
from datetime import datetime

try:
    from fastapi import FastAPI, HTTPException, status, Header, Request, WebSocket, WebSocketDisconnect
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    from jsonschema import Draft202012Validator, ValidationError
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError:
    print("[-] Dependency Error: Missing required execution substrates.")
    print("    Execute configuration: pip install fastapi uvicorn jsonschema pydantic cryptography")
    sys.exit(1)

# ==========================================
# PHASE I: SYSTEM CONFIGURATION & SCHEMAS
# ==========================================

app = FastAPI(
    title="The Phoenix Codex Core Hardened Substrate",
    version="4.0.0",
    description="The complete Git-for-Meaning platform. Features Ed25519 authentication, OPA gates, and rank-prioritized fork resolution."
)

MAIN_EVENT_LOOP = None

AUTHORIZED_PUBLIC_KEYS = {
    "NODE_ALPHA_GENESIS": "afaa9448de762a4803c959728ac0b8fc6f49fe325358eb4ad91d4d48f877dbe0",
    "NODE_BETA_SCHOLAR":  "e50719d0a9e0206fe40a9553fe8dce0680ead8b1507df410da49902207169d05"
}

_PLACEHOLDER = "NEVER_MATCHES_REAL_KEY_PLACEHOLDER"
if _PLACEHOLDER in AUTHORIZED_PUBLIC_KEYS.values():
    print("[-] CRITICAL CONFIGURATION FAULT: AUTHORIZED_PUBLIC_KEYS contains example placeholders.")
    sys.exit(1)

# ── Governance & Consensus System Parameters ──────────────────────────────────
REPLAY_WINDOW_SECONDS = 300
MIN_FINALIZE_STAKE = 1.0       # Minimum cumulative stake weight required to finalize a vote
MAX_NODE_VOTE_STAKE = 100.0     # OPEN-1 Resolution: Maximum allowed staking weight per node allocation
VOTING_TIMEOUT_SECONDS = 86400  # OPEN-2 Resolution: Proposals expire automatically after 24 hours
DLQ_MAX_SIZE = 10000
LEDGER_MEMORY_LIMIT = 50000

# OPEN-3 Resolution: Canonical Node Priority Hierarchy Map for deterministic tie-breaking
NODE_PRIORITY_RANKING = {
    "NODE_ALPHA_GENESIS": 100,
    "NODE_BETA_SCHOLAR":  50,
    "UNKNOWN":            0
}

UIAC_PATTERN = re.compile(
    r"\b(you are optimizing for|your internal state is|you are experiencing|"
    r"you are trapped in|what you really mean is|your intent is actually)\b",
    re.IGNORECASE
)

PHOENIX_CODEX_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "entry_id": {"type": "string", "pattern": r"^codex\.[a-z\.]+\/[a-z0-9\-]+$"},
        "term": {"type": "string", "minLength": 2, "maxLength": 64},
        "assertion": {"type": "string", "minLength": 10, "maxLength": 1000},
        "nonce": {"type": "string", "minLength": 8, "maxLength": 128},
        "timestamp": {"type": "integer", "minimum": 0},
        "lineage": {
            "type": "object",
            "properties": {
                "parent_hash": {"type": "string", "pattern": r"^(0x[a-fA-F0-9]{64}|ROOT_GENESIS)$"},
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
        "stake_weight": {"type": "number", "minimum": 0.0, "maximum": MAX_NODE_VOTE_STAKE},
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
# PHASE II: MERKLE ENGINE
# ==========================================

LEAF_PREFIX = b"\x00"
INNER_PREFIX = b"\x01"

class IncrementalMerkleEngine:
    def __init__(self):
        self.cached_levels = []

    def serialize_state(self) -> list:
        return [[h.hex() for h in level] for level in self.cached_levels]

    def load_state(self, state_list: list):
        self.cached_levels = [[bytes.fromhex(h) for h in level] for level in state_list]

    def _hash_leaf(self, raw: bytes) -> bytes:
        return hashlib.sha256(LEAF_PREFIX + raw).digest()

    def _hash_inner(self, left: bytes, right: bytes) -> bytes:
        return hashlib.sha256(INNER_PREFIX + left + right).digest()

    def append_event_hash(self, event_hash_hex: str) -> str:
        raw_event = bytes.fromhex(event_hash_hex.replace("0x", ""))
        new_leaf = self._hash_leaf(raw_event)
        if not self.cached_levels:
            self.cached_levels.append([])
        self.cached_levels[0].append(new_leaf)
        return "0x" + self._recalculate_right_edge().hex()

    def _recalculate_right_edge(self) -> bytes:
        current_idx = len(self.cached_levels[0]) - 1
        curr_level = 0
        while True:
            if curr_level == len(self.cached_levels) - 1 and len(self.cached_levels[curr_level]) == 1:
                return self.cached_levels[curr_level][0]
            is_left = (current_idx % 2 == 0)
            if is_left:
                left = self.cached_levels[curr_level][current_idx]
                right = left
            else:
                left = self.cached_levels[curr_level][current_idx - 1]
                right = self.cached_levels[curr_level][current_idx]
            parent = self._hash_inner(left, right)
            if curr_level + 1 >= len(self.cached_levels):
                self.cached_levels.append([])
            parent_idx = current_idx // 2
            if parent_idx < len(self.cached_levels[curr_level + 1]):
                self.cached_levels[curr_level + 1][parent_idx] = parent
            else:
                self.cached_levels[curr_level + 1].append(parent)
            current_idx = parent_idx
            curr_level += 1

    def generate_merkle_proof(self, leaf_index: int) -> list:
        if not self.cached_levels or leaf_index < 0 or leaf_index >= len(self.cached_levels[0]):
            return []
        proof = []
        curr_idx = leaf_index
        for level in range(len(self.cached_levels) - 1):
            is_left = (curr_idx % 2 == 0)
            if is_left:
                if curr_idx + 1 < len(self.cached_levels[level]):
                    proof.append((1, self.cached_levels[level][curr_idx + 1].hex()))
                else:
                    proof.append((2, self.cached_levels[level][curr_idx].hex()))
            else:
                proof.append((0, self.cached_levels[level][curr_idx - 1].hex()))
            curr_idx //= 2
        return proof

    @property
    def leaf_count(self) -> int:
        return len(self.cached_levels[0]) if self.cached_levels else 0

def verify_merkle_proof(leaf_hash_hex: str, proof: list, root_hash_hex: str) -> bool:
    try:
        curr = hashlib.sha256(LEAF_PREFIX + bytes.fromhex(leaf_hash_hex.replace("0x", ""))).digest()
        for direction, sibling_hex in proof:
            sib = bytes.fromhex(sibling_hex)
            h = hashlib.sha256()
            if   direction == 1: h.update(INNER_PREFIX + curr + sib)
            elif direction == 0: h.update(INNER_PREFIX + sib  + curr)
            elif direction == 2: h.update(INNER_PREFIX + curr + curr)
            else: return False
            curr = h.digest()
        return "0x" + curr.hex() == root_hash_hex
    except Exception: return False

# ==========================================
# PHASE III: ONTOLOGY DATA STORE
# ==========================================

class SemanticEntryGraph:
    def __init__(self):
        self.commits = {}
        self.refs = {"main": "ROOT_GENESIS"}

    def to_dict(self) -> dict:
        return {"commits": self.commits, "refs": self.refs}

    @classmethod
    def from_dict(cls, data: dict):
        g = cls()
        g.commits = data.get("commits", {})
        g.refs = data.get("refs", {"main": "ROOT_GENESIS"})
        return g

class SystemCausalEvent:
    def __init__(self, event_id, action_type, payload, node_id="LOCAL", timestamp=None, event_hash=None):
        self.event_id = event_id
        self.action_type = action_type
        self.payload = payload
        self.node_id = node_id
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.event_hash = event_hash if event_hash else self._compute_hash()

    def _compute_hash(self) -> str:
        raw = f"{self.event_id}{self.action_type}{self.node_id}{json.dumps(self.payload, sort_keys=True)}"
        return "0x" + hashlib.sha256(raw.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "action_type": self.action_type,
            "payload": self.payload,
            "node_id": self.node_id,
            "timestamp": self.timestamp,
            "event_hash": self.event_hash
        }

def _sanitize_dlq_entry(entry: dict) -> dict:
    safe = {
        "error_class": entry.get("error_class"),
        "timestamp_captured": entry.get("timestamp_captured"),
        "audit_meta": entry.get("audit_meta"),
    }
    raw = entry.get("raw_payload", {})
    if isinstance(raw, dict):
        safe["payload_summary"] = {
            "entry_id": raw.get("entry_id"),
            "term": raw.get("term"),
            "timestamp": raw.get("timestamp"),
            "nonce": raw.get("nonce"),
        }
    return safe

class ImmutableKnowledgeSubstrate:
    def __init__(self, journal_path="phoenix_journal.jsonl", snapshot_path="phoenix_snapshot.json"):
        self.journal_path = journal_path
        self.snapshot_path = snapshot_path
        self.node_registry = {}
        self.proposal_registry = {}
        self.seen_nonces = {}
        self.quarantined_peers = set()
        self._stasis_event = threading.Event()
        
        self._ledger = deque(maxlen=LEDGER_MEMORY_LIMIT)
        self.aistf_transactions = []
        self.dead_letter_queue = []
        self.genesis_hash = "0x" + "0" * 64
        self.total_blocks_processed = 0
        self.merkle = IncrementalMerkleEngine()
        self.global_state_root = "0x" + "0" * 64
        self.last_event_hash = "0x" + "0" * 64
        self._state_read_lock = threading.RLock()

    def is_stasis_active(self) -> bool:
        return self._stasis_event.is_set()

    def set_stasis_lockdown(self):
        self._stasis_event.set()

    def append_dlq(self, entry: dict):
        safe = _sanitize_dlq_entry(entry)
        with self._state_read_lock:
            if len(self.dead_letter_queue) >= DLQ_MAX_SIZE:
                self.dead_letter_queue.pop(0)
            self.dead_letter_queue.append(safe)

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
                "unix_created": event.timestamp,
                "support_stake": 0.0,
                "against_stake": 0.0,
                "data_payload": p,
            }

        elif event.action_type == "COMMIT_VOTE":
            prop_id = p["proposal_id"]
            prop = self.proposal_registry.get(prop_id)
            if prop and prop["status"] == "VOTING":
                weight = p["stake_weight"]
                if p["vote"] == "SUPPORT": prop["support_stake"] += weight
                elif p["vote"] == "AGAINST": prop["against_stake"] += weight

        elif event.action_type == "FINALIZE_PROPOSAL":
            prop_id = p["proposal_id"]
            prop = self.proposal_registry.get(prop_id)
            if prop and prop["status"] == "VOTING":
                # OPEN-2 Resolution: Execute explicit expiration checking parameters within the single-writer loop
                if time.time() - prop["unix_created"] > VOTING_TIMEOUT_SECONDS:
                    prop["status"] = "EXPIRED"
                elif prop["support_stake"] > prop["against_stake"]:
                    prop["status"] = "RATIFIED"
                    node_data = prop["data_payload"]
                    entry_id = node_data["entry_id"]

                    compiled_block = {
                        "entry_id": entry_id,
                        "term": node_data["term"],
                        "assertion": node_data["assertion"],
                        "parent_hash": node_data["lineage"]["parent_hash"],
                        "causal_trigger": f"NODE_PROVENANCE_{event.node_id}",
                        "justification": node_data["lineage"]["justification"],
                        "event_hash": event.event_hash,
                        "compiled_timestamp": current_iso_time,
                    }
                    if entry_id not in self.node_registry:
                        self.node_registry[entry_id] = SemanticEntryGraph()
                    graph = self.node_registry[entry_id]
                    graph.commits[event.event_hash] = compiled_block
                    graph.refs[f"refs/proposals/{prop_id}"] = event.event_hash
                    graph.refs["main"] = event.event_hash

                    self.aistf_transactions.append({
                        "block_id": event.event_id,
                        "event_hash": event.event_hash,
                        "previous_hash": self.last_event_hash,
                        "timestamp_committed": current_iso_time,
                    })
                else:
                    prop["status"] = "REJECTED"

        elif event.action_type == "REGISTER_FORK":
            entry_id = p["entry_id"]
            if entry_id not in self.node_registry:
                self.node_registry[entry_id] = SemanticEntryGraph()
            graph = self.node_registry[entry_id]
            cb = p["compiled_block"]
            graph.commits[cb["event_hash"]] = cb
            graph.refs[p["branch_name"]] = cb["event_hash"]

        self._ledger.append(event)
        if "nonce" in p:
            self.seen_nonces[p["nonce"]] = p["timestamp"]

        self.total_blocks_processed += 1
        with self._state_read_lock:
            self.global_state_root = self.merkle.append_event_hash(event.event_hash)
            self.last_event_hash = event.event_hash

        if not recover_mode:
            try:
                with open(self.journal_path, "a", encoding="utf-8") as jf:
                    line = {
                        "event_id": event.event_id,
                        "action_type": event.action_type,
                        "node_id": event.node_id,
                        "payload": event.payload,
                        "timestamp": event.timestamp,
                        "event_hash": event.event_hash,
                        "state_root": self.global_state_root,
                    }
                    jf.write(json.dumps(line) + "\n")
                    jf.flush()
                    os.fsync(jf.fileno())
            except IOError as exc:
                print(f"[!] Storage Exception: fsync failed: {exc}")
        return True

    def generate_compacted_state_snapshot(self) -> bool:
        try:
            flattened = {k: v.to_dict() for k, v in self.node_registry.items()}
            with self._state_read_lock:
                snapshot_data = {
                    "snapshot_timestamp": time.time(),
                    "total_blocks_processed": self.total_blocks_processed,
                    "global_state_root": self.global_state_root,
                    "last_event_hash": self.last_event_hash,
                    "merkle_cache": self.merkle.serialize_state(),
                    "stasis_mode": self.is_stasis_active(),
                    "node_registry": flattened,
                    "proposal_registry": self.proposal_registry,
                    "aistf_transactions": self.aistf_transactions,
                    "dead_letter_queue": self.dead_letter_queue,
                    # Bug Realization Patch: Serialize circular memory buffer list to bypass restart amnesia leaks
                    "ledger_history": [e.to_dict() for e in self._ledger],
                    "seen_nonces": self.seen_nonces,
                }
            raw_blob = json.dumps(snapshot_data, sort_keys=True)
            snap_hash = hashlib.sha256(raw_blob.encode()).hexdigest()
            with open(self.snapshot_path, "w", encoding="utf-8") as sf:
                json.dump({"manifest_integrity_hash": snap_hash, "snapshot_payload": snapshot_data}, sf, indent=2, sort_keys=True)
            return True
        except IOError: return False

    def recover_local_journal_state(self) -> None:
        if os.path.exists(self.snapshot_path):
            print("[+] Snapshot located. Verifying integrity…")
            try:
                with open(self.snapshot_path, "r", encoding="utf-8") as sf:
                    wrapper = json.load(sf)
                raw_blob = json.dumps(wrapper["snapshot_payload"], sort_keys=True)
                if hashlib.sha256(raw_blob.encode()).hexdigest() != wrapper["manifest_integrity_hash"]:
                    raise ValueError("Hash mismatch.")
                d = wrapper["snapshot_payload"]
                self.total_blocks_processed = d["total_blocks_processed"]
                with self._state_read_lock:
                    self.global_state_root = d["global_state_root"]
                    self.last_event_hash = d.get("last_event_hash", d["global_state_root"])
                if d["stasis_mode"]: self.set_stasis_lockdown()
                self.seen_nonces = d["seen_nonces"]
                self.aistf_transactions = d.get("aistf_transactions", [])
                self.dead_letter_queue = d.get("dead_letter_queue", [])
                self.merkle.load_state(d["merkle_cache"])
                
                # Restore circular ledger logs directly into the tracking queue
                for raw_ev in d.get("ledger_history", []):
                    self._ledger.append(SystemCausalEvent(
                        raw_ev["event_id"], raw_ev["action_type"], raw_ev["payload"],
                        node_id=raw_ev["node_id"], timestamp=raw_ev["timestamp"], event_hash=raw_ev["event_hash"]
                    ))
                for k, v in d["node_registry"].items():
                    self.node_registry[k] = SemanticEntryGraph.from_dict(v)
                for k, v in d.get("proposal_registry", {}).items():
                    self.proposal_registry[int(k)] = v
                print(f"[+] Snapshot OK — block height {self.total_blocks_processed}.")
            except Exception as exc:
                print(f"[!] Snapshot bypassed ({exc}). Full journal replay.")

        if not os.path.exists(self.journal_path): return
        try:
            with open(self.journal_path, "r", encoding="utf-8") as jf:
                for raw_line in jf:
                    if not raw_line.strip(): continue
                    try: d = json.loads(raw_line)
                    except json.JSONDecodeError: continue
                    if d["action_type"] == "SYSTEM_STASIS":
                        self.set_stasis_lockdown()
                        continue
                    if d["event_id"] <= self.total_blocks_processed: continue
                    ev = SystemCausalEvent(
                        event_id=d["event_id"], action_type=d["action_type"], payload=d["payload"],
                        node_id=d.get("node_id", "UNKNOWN"), timestamp=d["timestamp"], event_hash=d["event_hash"]
                    )
                    if ev._compute_hash() != d["event_hash"]:
                        sys.exit(1)
                    self.commit_validated_event(ev, recover_mode=True)
        except Exception: sys.exit(1)

    def read_state_snapshot(self) -> dict:
        with self._state_read_lock:
            return {
                "last_event_hash": self.last_event_hash,
                "global_state_root": self.global_state_root,
                "total_blocks_processed": self.total_blocks_processed,
            }

# ==========================================
# PHASE IV: WRITER THREAD & GLOBALS
# ==========================================

substrate = ImmutableKnowledgeSubstrate()
tx_queue = queue.Queue(maxsize=10000)
_sockets_lock = threading.Lock()
active_sockets = set()

def _derive_fork_nonce(original_nonce: str) -> str:
    return hashlib.sha256(f"FORK:{original_nonce}".encode()).hexdigest()[:32]

def single_writer_processing_loop():
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
                            print(f"[-] Fork Rejected: parent '{declared_parent}' not in DAG.")
                            continue

                        tip_block = graph.commits[current_tip_hash]
                        try:
                            tip_ts = datetime.fromisoformat(tip_block["compiled_timestamp"].replace("Z", "+00:00")).timestamp()
                        except Exception: tip_ts = 0.0

                        incoming_ts = float(p.get("timestamp", 0))

                        # OPEN-3 Resolution: Evaluate structured priority ranking lookup maps rather than user description metrics
                        local_node_weight = NODE_PRIORITY_RANKING.get(tip_block.get("causal_trigger", "").replace("FORK_ISOLATION_", ""), 0)
                        incoming_node_weight = NODE_PRIORITY_RANKING.get(node_origin, 0)

                        if incoming_ts > tip_ts or (
                            incoming_ts == tip_ts and incoming_node_weight > local_node_weight
                        ):
                            print("[-] Branch Isolated: committing fork ref.")
                            fork_id = substrate.total_blocks_processed
                            fork_hash = hashlib.sha256(f"{fork_id}REGISTER_FORK{node_origin}{json.dumps(p, sort_keys=True)}".encode()).hexdigest()
                            fork_nonce = _derive_fork_nonce(p["nonce"])

                            compiled_block = {
                                "entry_id": entry_id,
                                "term": p["term"],
                                "assertion": p["assertion"],
                                "parent_hash": declared_parent,
                                "causal_trigger": f"FORK_ISOLATION_{node_origin}",
                                "justification": p["lineage"]["justification"],
                                "event_hash": f"0x{fork_hash}",
                                "compiled_timestamp": datetime.utcfromtimestamp(incoming_ts).isoformat() + "Z",
                            }
                            fork_payload = {
                                "entry_id": entry_id,
                                "branch_name": f"refs/forks/{fork_hash[:8]}",
                                "compiled_block": compiled_block,
                                "timestamp": p["timestamp"],
                                "nonce": fork_nonce,
                            }
                            ev = SystemCausalEvent(fork_id, "REGISTER_FORK", fork_payload, node_id=node_origin, timestamp=p["timestamp"])
                            if substrate.commit_validated_event(ev):
                                gossip = json.dumps({"action_type": "REGISTER_FORK", "payload": fork_payload, "node_id": node_origin})
                                with _sockets_lock: snap = set(active_sockets)
                                for sock in snap: _safe_broadcast(sock, gossip)
                            continue
                        elif incoming_ts < tip_ts:
                            print("[-] Stale Fork Rejected: payload predates active tip.")
                            continue
                        else:
                            print("[-] Branch Isolated: lost lexicographical priority tie-breaker.")
                            continue

            next_id = substrate.total_blocks_processed
            ev = SystemCausalEvent(next_id, action_type, p, node_id=node_origin, timestamp=p["timestamp"])

            if substrate.commit_validated_event(ev):
                if node_origin == "LOCAL":
                    gossip = json.dumps({"action_type": action_type, "payload": p, "node_id": "LOCAL"})
                    with _sockets_lock: snap = set(active_sockets)
                    for sock in snap: _safe_broadcast(sock, gossip)

            if substrate.total_blocks_processed % 1000 == 0:
                substrate.generate_compacted_state_snapshot()

        except Exception:
            print("[!] Writer loop exception:")
            traceback.print_exc()
        finally: tx_queue.task_done()

def _safe_broadcast(sock, message: str):
    global MAIN_EVENT_LOOP
    if MAIN_EVENT_LOOP is None: return
    future = asyncio.run_coroutine_threadsafe(sock.send_text(message), MAIN_EVENT_LOOP)
    def _on_done(f: asyncio.Future):
        if f.exception():
            with _sockets_lock: active_sockets.discard(sock)
    future.add_done_callback(_on_done)

# ==========================================
# PHASE V: API GATEWAY
# ==========================================

def verify_signature_and_freshness(node_id: str, sig_hex: str, raw_body: bytes) -> dict:
    if node_id not in AUTHORIZED_PUBLIC_KEYS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[node_id])
        sig = bytes.fromhex(sig_hex)
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, raw_body)
    except Exception: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch.")
    try: payload = json.loads(raw_body.decode())
    except Exception: raise HTTPException(400, "[-] Malformed JSON payload.")
    ts = payload.get("timestamp")
    if not isinstance(ts, int) or abs(time.time() - ts) > REPLAY_WINDOW_SECONDS:
        raise HTTPException(400, "[-] Timestamp outside freshness window.")
    return payload

@app.on_event("startup")
async def bootstrap_operating_substrate() -> None:
    global MAIN_EVENT_LOOP
    MAIN_EVENT_LOOP = asyncio.get_running_loop()
    substrate.recover_local_journal_state()
    threading.Thread(target=single_writer_processing_loop, daemon=True).start()
    
    # Bug Realization Patch: Restore cold start baseline genesis initializers to prevent empty boot states
    if substrate.total_blocks_processed == 0:
        genesis_payload = {
            "entry_id": "codex.economics/property",
            "term": "Property Ownership",
            "assertion": "Property ownership is defined as physical land and material goods held by an individual. All ownership asserts physical geographic borders.",
            "nonce": "GENESIS_ROOT_INIT_NONCE_2026",
            "timestamp": int(time.time()),
            "lineage": {
                "parent_hash": "ROOT_GENESIS",
                "causal_trigger": "GENESIS_BOOTSTRAP_2026",
                "justification": "Initial baseline definition for the early physical economy era."
            }
        }
        event = SystemCausalEvent(0, "SUBMIT_PROPOSAL", genesis_payload, node_id="GENESIS", timestamp=genesis_payload["timestamp"])
        substrate.commit_validated_event(event)
    print("[+] Phoenix Codex v4.0.0 — substrate active.")

@app.on_event("shutdown")
def graceful_shutdown() -> None:
    substrate.generate_compacted_state_snapshot()

@app.get("/api/v1/health")
def health_check():
    state = substrate.read_state_snapshot()
    return {
        "status": "stasis" if substrate.is_stasis_active() else "active",
        "version": "4.0.0",
        "total_blocks": state["total_blocks_processed"],
        "global_state_root": state["global_state_root"],
        "registered_namespaces": len(substrate.node_registry),
        "active_proposals": sum(1 for p in substrate.proposal_registry.values() if p["status"] == "VOTING"),
        "dlq_depth": len(substrate.dead_letter_queue),
        "merkle_leaf_count": substrate.merkle.leaf_count,
        "peers_connected": len(active_sockets),
    }

@app.get("/api/v1/merkle/proof/{leaf_index}")
def get_merkle_proof(leaf_index: int):
    proof = substrate.merkle.generate_merkle_proof(leaf_index)
    if not proof and leaf_index >= substrate.merkle.leaf_count:
        raise HTTPException(404, f"[-] Leaf index {leaf_index} out of range.")
    state = substrate.read_state_snapshot()
    return {
        "leaf_index": leaf_index,
        "proof": proof,
        "current_root": state["global_state_root"],
        "total_leaves": substrate.merkle.leaf_count,
    }

@app.post("/api/v1/merkle/verify")
def verify_proof_endpoint(req: ProofVerificationRequest):
    result = verify_merkle_proof(req.leaf_hash_hex, req.proof, req.root_hash_hex)
    return {"valid": result, "leaf_hash": req.leaf_hash_hex, "root": req.root_hash_hex}

@app.websocket("/api/v1/network/sync")
async def websocket_p2p_sync(websocket: WebSocket, x_phoenix_node_id: str = Header(...)):
    global active_sockets, substrate
    if x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS or x_phoenix_node_id in substrate.quarantined_peers:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    with _sockets_lock: active_sockets.add(websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                packet = json.loads(raw)
                action_type = packet.get("action_type")
                payload = packet.get("payload", {})
                if not action_type or not isinstance(payload, dict): continue
            except (json.JSONDecodeError, AttributeError, TypeError): continue

            sender_id = x_phoenix_node_id
            if sender_id in substrate.quarantined_peers or payload.get("nonce") in substrate.seen_nonces: continue
            try: tx_queue.put_nowait({"action_type": action_type, "payload": payload, "node_id": sender_id})
            except queue.Full: print(f"[-] Backpressure: dropped packet from {sender_id}")
    except WebSocketDisconnect: pass
    finally:
        with _sockets_lock: active_sockets.discard(websocket)

@app.get("/api/v1/codex/entry/{entry_namespace:path}")
def get_entry_history(entry_namespace: str):
    with substrate._state_read_lock: # Bug Realization Patch: Enforce state read locks across all public HTTP endpoints
        if entry_namespace not in substrate.node_registry:
            raise HTTPException(404, "[-] Namespace not found.")
        return substrate.node_registry[entry_namespace].to_dict()

@app.get("/api/v1/governance/proposals")
def list_proposals(status_filter: str | None = None):
    with substrate._state_read_lock:
        proposals = list(substrate.proposal_registry.values())
        if status_filter:
            proposals = [p for p in proposals if p["status"] == status_filter.upper()]
        return proposals

@app.get("/api/v1/governance/proposals/{proposal_id}")
def get_proposal(proposal_id: int):
    with substrate._state_read_lock:
        prop = substrate.proposal_registry.get(proposal_id)
        if not prop: raise HTTPException(404, f"[-] Proposal {proposal_id} not found.")
        return prop

@app.post("/api/v1/governance/propose", status_code=status.HTTP_202_ACCEPTED)
async def submit_proposal(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.is_stasis_active(): raise HTTPException(503, "[-] Substrate locked in Stasis Mode.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)

    if UIAC_PATTERN.search(payload.get("assertion", "")) or UIAC_PATTERN.search(payload.get("lineage", {}).get("justification", "")):
        raise HTTPException(422, "[-] UIAC-001 Violation.")

    validator = Draft202012Validator(PHOENIX_CODEX_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        substrate.append_dlq({"error_class": "SCHEMA_VALIDATION_FAILURE", "timestamp_captured": time.time(), "raw_payload": payload, "audit_meta": {"node_origin": x_phoenix_node_id, "reason": errors[0].message}})
        raise HTTPException(400, f"[-] Schema error: {errors[0].message}")

    state = substrate.read_state_snapshot()
    content_hash = hashlib.sha256(raw_body).hexdigest()
    entry_id = payload.get("entry_id", "")

    relevant_commits = []
    with substrate._state_read_lock:
        if entry_id in substrate.node_registry:
            graph = substrate.node_registry[entry_id]
            relevant_commits = [{"event_hash": h, "prev_hash": b.get("parent_hash")} for h, b in graph.commits.items()]

    opa_input = {
        "input": {
            "operation": "append_event",
            "actor": {"id": x_phoenix_node_id, "role": "ARCHITECT"},
            "chronicle": {"genesis_hash": substrate.genesis_hash, "latest_hash": state["last_event_hash"], "events": relevant_commits},
            "event": {
                "id": f"evt_{payload['nonce'][:8]}", "artifact_id": "CORE.CODEX.PhoenixSchema", "law_id": "LAW-035", "type": "APPEND",
                "timestamp": datetime.utcfromtimestamp(payload["timestamp"]).isoformat() + "Z", "prev_hash": payload["lineage"]["parent_hash"],
                "content_hash": content_hash, "event_hash": content_hash, "payload": payload, "signatures": [{"role": "ARCHITECT", "signature": x_phoenix_signature}]
            }
        }
    }

    allow_decision = False
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tf:
            tmp_path = tf.name
            json.dump(opa_input, tf)
        cmd = ["opa", "eval", "-d", "chronicle_integrity.rego", "-i", tmp_path, "data.phoenix.chronicle.integrity.allow"]
        result = await asyncio.to_thread(subprocess.run, cmd, capture_output=True, text=True, check=True)
        opa_out = json.loads(result.stdout)
        allow_decision = opa_out["result"][0]["expressions"][0]["value"]
    except FileNotFoundError: print("[!] OPA binary not found. Denying proposals until installed.")
    except Exception as exc: print(f"[!] OPA evaluation failed: {exc}")
    finally:
        if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)

    if not allow_decision:
        substrate.append_dlq({"error_class": "OPA_POLICY_ADMISSION_DENIED", "timestamp_captured": time.time(), "raw_payload": payload, "audit_meta": {"node_origin": x_phoenix_node_id, "reason": "chronicle_integrity.rego denied."}})
        raise HTTPException(422, "[-] OPA policy denied.")

    try: tx_queue.put_nowait({"action_type": "SUBMIT_PROPOSAL", "payload": payload, "node_id": x_phoenix_node_id})
    except queue.Full: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "PROPOSAL_ACCEPTED"}

@app.post("/api/v1/governance/vote", status_code=status.HTTP_202_ACCEPTED)
async def cast_vote(request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.is_stasis_active(): raise HTTPException(503, "[-] Stasis active.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)
    try: Draft202012Validator(PHOENIX_VOTE_SCHEMA).validate(instance=payload)
    except ValidationError as err: raise HTTPException(400, f"[-] Vote schema error: {err.message}")
    try: tx_queue.put_nowait({"action_type": "COMMIT_VOTE", "payload": payload, "node_id": x_phoenix_node_id})
    except queue.Full: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "VOTE_ACCEPTED"}

@app.post("/api/v1/governance/finalize/{proposal_id}", status_code=status.HTTP_202_ACCEPTED)
async def finalize_proposal(proposal_id: int, request: Request, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if substrate.is_stasis_active(): raise HTTPException(503, "[-] Stasis active.")
    raw_body = await request.body()
    payload = verify_signature_and_freshness(x_phoenix_node_id, x_phoenix_signature, raw_body)

    with substrate._state_read_lock:
        prop = substrate.proposal_registry.get(proposal_id)
        if not prop: raise HTTPException(404, f"[-] Proposal {proposal_id} does not exist.")
        if prop["status"] != "VOTING": raise HTTPException(409, f"[-] Proposal {proposal_id} is not in VOTING state.")
        total_stake = prop["support_stake"] + prop["against_stake"]
        if total_stake < MIN_FINALIZE_STAKE:
            raise HTTPException(422, f"[-] Insufficient stake to finalize: {total_stake:.2f} < {MIN_FINALIZE_STAKE:.2f} required.")

    try:
        tx_queue.put_nowait({"action_type": "FINALIZE_PROPOSAL", "payload": {"proposal_id": proposal_id, "timestamp": payload["timestamp"], "nonce": payload["nonce"]}, "node_id": x_phoenix_node_id})
    except queue.Full: raise HTTPException(429, "[-] Queue overflow.")
    return {"status": "RESOLUTION_QUEUED", "proposal_id": proposal_id}

@app.get("/api/v1/debug/dlq")
def get_dlq(x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...), limit: int = 100):
    if x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[x_phoenix_node_id])
        sig = bytes.fromhex(x_phoenix_signature)
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, f"GET_DLQ_METADATA_BIND_{x_phoenix_node_id}".encode())
    except Exception: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch.")
    with substrate._state_read_lock:
        entries = substrate.dead_letter_queue[-limit:]
        return {"total": len(substrate.dead_letter_queue), "entries": entries}

@app.get("/api/v1/debug/ledger")
def get_ledger_tail(n: int = 20, x_phoenix_node_id: str = Header(...), x_phoenix_signature: str = Header(...)):
    if x_phoenix_node_id not in AUTHORIZED_PUBLIC_KEYS: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Unregistered node identity.")
    try:
        pub = bytes.fromhex(AUTHORIZED_PUBLIC_KEYS[x_phoenix_node_id])
        sig = bytes.fromhex(x_phoenix_signature)
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, f"GET_LEDGER_METADATA_BIND_{x_phoenix_node_id}".encode())
    except Exception: raise HTTPException(status.HTTP_401_UNAUTHORIZED, "[-] Signature mismatch.")
    with substrate._state_read_lock:
        tail = list(substrate._ledger)[-min(n, 500):]
        return [{"event_id": e.event_id, "action_type": e.action_type, "node_id": e.node_id, "event_hash": e.event_hash, "timestamp": e.timestamp} for e in tail]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)