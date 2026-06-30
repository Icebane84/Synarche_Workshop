import hashlib
import json
import os
import sys
import threading
import time
from collections import deque
from datetime import datetime

from .config import DLQ_MAX_SIZE, LEDGER_MEMORY_LIMIT, REPLAY_WINDOW_SECONDS, VOTING_TIMEOUT_SECONDS

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
        self.lock = threading.RLock()

    def is_stasis_active(self) -> bool:
        return self._stasis_event.is_set()

    def set_stasis_lockdown(self):
        self._stasis_event.set()

    def append_dlq(self, entry: dict):
        safe = _sanitize_dlq_entry(entry)
        with self.lock:
            if len(self.dead_letter_queue) >= DLQ_MAX_SIZE:
                self.dead_letter_queue.pop(0)
            self.dead_letter_queue.append(safe)

    def commit_validated_event(self, event: SystemCausalEvent, recover_mode=False) -> bool:
        with self.lock:
            if self.is_stasis_active() and not recover_mode:
                return False

            p = event.payload
            current_iso_time = datetime.utcfromtimestamp(event.timestamp).isoformat() + "Z"

            if event.action_type == "SUBMIT_PROPOSAL":
                prop_id = event.event_id
                self.proposal_registry[prop_id] = {
                    "proposal_id": prop_id, "status": "VOTING", "node_origin": event.node_id,
                    "timestamp_created": current_iso_time, "unix_created": event.timestamp,
                    "support_stake": 0.0, "against_stake": 0.0, "data_payload": p,
                }
            elif event.action_type == "COMMIT_VOTE":
                prop = self.proposal_registry.get(p["proposal_id"])
                if prop and prop["status"] == "VOTING":
                    if p["vote"] == "SUPPORT": prop["support_stake"] += p["stake_weight"]
                    else: prop["against_stake"] += p["stake_weight"]
            elif event.action_type == "FINALIZE_PROPOSAL":
                prop = self.proposal_registry.get(p["proposal_id"])
                if prop and prop["status"] == "VOTING":
                    if time.time() - prop["unix_created"] > VOTING_TIMEOUT_SECONDS:
                        prop["status"] = "EXPIRED"
                    elif prop["support_stake"] > prop["against_stake"]:
                        prop["status"] = "RATIFIED"
                        node_data, entry_id = prop["data_payload"], prop["data_payload"]["entry_id"]
                        compiled_block = {
                            "entry_id": entry_id, "term": node_data["term"], "assertion": node_data["assertion"],
                            "parent_hash": node_data["lineage"]["parent_hash"], "causal_trigger": f"NODE_PROVENANCE_{event.node_id}",
                            "justification": node_data["lineage"]["justification"], "event_hash": event.event_hash,
                            "compiled_timestamp": current_iso_time,
                        }
                        if entry_id not in self.node_registry: self.node_registry[entry_id] = SemanticEntryGraph()
                        graph = self.node_registry[entry_id]
                        graph.commits[event.event_hash] = compiled_block
                        graph.refs[f"refs/proposals/{p['proposal_id']}"] = event.event_hash
                        graph.refs["main"] = event.event_hash
                    else:
                        prop["status"] = "REJECTED"
            elif event.action_type == "REGISTER_FORK":
                entry_id = p["entry_id"]
                if entry_id not in self.node_registry: self.node_registry[entry_id] = SemanticEntryGraph()
                graph, cb = self.node_registry[entry_id], p["compiled_block"]
                graph.commits[cb["event_hash"]] = cb
                graph.refs[p["branch_name"]] = cb["event_hash"]

            self._ledger.append(event)
            if "nonce" in p: self.seen_nonces[p["nonce"]] = p["timestamp"]
            self.total_blocks_processed += 1
            self.global_state_root = self.merkle.append_event_hash(event.event_hash)
            self.last_event_hash = event.event_hash

        if not recover_mode:
            try:
                with open(self.journal_path, "a", encoding="utf-8") as jf:
                    line = {**event.to_dict(), "state_root": self.global_state_root}
                    jf.write(json.dumps(line) + "\n")
                    jf.flush()
                    os.fsync(jf.fileno())
            except IOError as exc:
                print(f"[!] Storage Exception: fsync failed: {exc}")
        return True

    def generate_compacted_state_snapshot(self) -> bool:
        with self.lock:
            try:
                snapshot_data = {
                    "snapshot_timestamp": time.time(), "total_blocks_processed": self.total_blocks_processed,
                    "global_state_root": self.global_state_root, "last_event_hash": self.last_event_hash,
                    "merkle_cache": self.merkle.serialize_state(), "stasis_mode": self.is_stasis_active(),
                    "node_registry": {k: v.to_dict() for k, v in self.node_registry.items()},
                    "proposal_registry": self.proposal_registry, "aistf_transactions": self.aistf_transactions,
                    "dead_letter_queue": self.dead_letter_queue, "ledger_history": [e.to_dict() for e in self._ledger],
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
            try:
                with open(self.snapshot_path, "r", encoding="utf-8") as sf: wrapper = json.load(sf)
                raw_blob = json.dumps(wrapper["snapshot_payload"], sort_keys=True)
                if hashlib.sha256(raw_blob.encode()).hexdigest() != wrapper["manifest_integrity_hash"]: raise ValueError("Hash mismatch.")
                d = wrapper["snapshot_payload"]
                with self.lock:
                    self.total_blocks_processed = d["total_blocks_processed"]
                    self.global_state_root = d["global_state_root"]
                    self.last_event_hash = d.get("last_event_hash", d["global_state_root"])
                    if d["stasis_mode"]: self.set_stasis_lockdown()
                    self.seen_nonces = d["seen_nonces"]
                    self.aistf_transactions = d.get("aistf_transactions", [])
                    self.dead_letter_queue = d.get("dead_letter_queue", [])
                    self.merkle.load_state(d["merkle_cache"])
                    for raw_ev in d.get("ledger_history", []): self._ledger.append(SystemCausalEvent(**raw_ev))
                    for k, v in d["node_registry"].items(): self.node_registry[k] = SemanticEntryGraph.from_dict(v)
                    for k, v in d.get("proposal_registry", {}).items(): self.proposal_registry[int(k)] = v
                print(f"[+] Snapshot OK — block height {self.total_blocks_processed}.")
            except Exception as exc: print(f"[!] Snapshot bypassed ({exc}). Full journal replay.")

        if not os.path.exists(self.journal_path): return
        try:
            with open(self.journal_path, "r", encoding="utf-8") as jf:
                for raw_line in jf:
                    if not (line := raw_line.strip()): continue
                    try: d = json.loads(line)
                    except json.JSONDecodeError: continue
                    if d["action_type"] == "SYSTEM_STASIS": self.set_stasis_lockdown(); continue
                    if d["event_id"] <= self.total_blocks_processed: continue
                    ev = SystemCausalEvent(d["event_id"], d["action_type"], d["payload"], d.get("node_id", "UNKNOWN"), d["timestamp"], d["event_hash"])
                    if ev._compute_hash() != d["event_hash"]: sys.exit(1)
                    self.commit_validated_event(ev, recover_mode=True)
        except Exception: sys.exit(1)

    def purge_expired_nonces(self, current_time: float) -> None:
        with self.lock:
            expired = [k for k, ts in self.seen_nonces.items() if current_time - ts > REPLAY_WINDOW_SECONDS]
            for k in expired: del self.seen_nonces[k]
