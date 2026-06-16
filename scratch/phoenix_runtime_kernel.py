import hashlib
import json
import math  # noqa: F401
import mmap
import os
import queue
import re
import struct
import sys  # noqa: F401
import threading
import time
from collections import defaultdict, deque
from enum import Enum, auto

# ==========================================
# PHASE I: THE MULTI-TIER PROTOCOL CONTRACT
# ==========================================


class ExecutionStatus(Enum):
    SUCCESS = auto()
    REFUSED_VIOLATION = auto()
    SYSTEMIC_HALT = auto()
    REPAIR_DEGRADED = auto()


class EdgeOntology(Enum):
    STRUCTURAL = auto()
    GOVERNANCE = auto()
    EXECUTION = auto()


class SystemCausalEvent:
    """The immutable transaction block primitive for the append-only backbone."""

    def __init__(self, event_id: int, actor_id: str, action_type: str, payload: dict, parent_hash: str = "0" * 64):
        self.event_id = event_id
        self.actor_id = actor_id
        self.action_type = action_type
        self.payload = payload
        self.parent_hash = parent_hash
        self.timestamp = time.time()
        self.event_hash = self._compute_crypto_hash()

    def _compute_crypto_hash(self) -> str:
        h = hashlib.sha256()
        h.update(str(self.event_id).encode("utf-8"))
        h.update(str(self.actor_id).encode("utf-8"))
        h.update(str(self.action_type).encode("utf-8"))
        h.update(json.dumps(self.payload, sort_keys=True).encode("utf-8"))
        h.update(str(self.parent_hash).encode("utf-8"))
        h.update(str(self.timestamp).encode("utf-8"))
        return h.hexdigest()


# ==========================================
# PHASE II: VARIABLE-LENGTH BINARY PAGE STORE
# ==========================================


class DynamicVariablePageFrame:
    """
    Durable, binary page frame manager.
    Layout: [Magic:4B][Version:2B][NodeID:4B][Cost:4B][Priority:4B][EdgeCount:4B][PayloadLen:4B][Edges...][PackedString...]
    """

    HEADER_FMT = "<4sHIIIII"

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.header_size = struct.calcsize(self.HEADER_FMT)

    def write_safe_page(
        self, node_id: int, cost: int, priority: int, structural_edges_list: list, payload_string: str = ""
    ) -> None:
        payload_bytes = payload_string.encode("utf-8")
        payload_len = len(payload_bytes)
        edge_count = len(structural_edges_list)
        required_size = self.header_size + (edge_count * 4) + payload_len

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "wb") as f:
            f.write(b"\x00" * required_size)

        f_handle = open(self.file_path, "r+b")
        mm = mmap.mmap(f_handle.fileno(), 0)

        header = struct.pack(self.HEADER_FMT, b"PAGE", 1, node_id, cost, priority, edge_count, payload_len)
        mm.seek(0)
        mm.write(header)
        for target_id in structural_edges_list:
            mm.write(struct.pack("<I", target_id))
        if payload_len > 0:
            mm.write(payload_bytes)
        mm.flush()
        mm.close()
        f_handle.close()

    def read_safe_page(self) -> tuple[int, int, int, list[int], str]:
        f_handle = open(self.file_path, "rb")
        mm = mmap.mmap(f_handle.fileno(), 0, access=mmap.ACCESS_READ)
        header_bytes = mm.read(self.header_size)
        _, _, node_id, cost, priority, edge_count, payload_len = struct.unpack(self.HEADER_FMT, header_bytes)

        edges = []
        for _ in range(edge_count):
            edges.append(struct.unpack("<I", mm.read(4))[0])

        payload_string = ""
        if payload_len > 0:
            payload_string = mm.read(payload_len).decode("utf-8")

        mm.close()
        f_handle.close()
        return node_id, cost, priority, edges, payload_string


# ==========================================
# PHASE III: HARDENED POLICY ENGINE & UIAC-001
# ==========================================


class CentralizedPolicyEngine:
    """The unified governance evaluator enforcing word boundaries and intent gates."""

    def __init__(self, config_path=None):
        self.lexicon = {"THE FORGE": ["PERSISTENCE", "DATA"], "COGNITIVE CIRCUIT BREAKER": ["PRESENTATION"]}
        self.uiac_patterns = [
            r"you are optimizing for",
            r"your internal state is",
            r"you are experiencing",
            r"you are trapped in",
            r"what you really mean is",
            r"your intent is actually",
        ]
        self._compile_patterns()

        if config_path and os.path.exists(config_path):
            self.load_from_json(config_path)

    def _compile_patterns(self) -> None:
        pattern_str: str = r"\b(" + "|".join(self.uiac_patterns) + r")\b"
        self.uiac_pattern = re.compile(pattern_str, re.IGNORECASE)

    def load_from_json(self, file_path: str) -> None:
        """Dynamically loads lexicon and intent gate patterns from a JSON configuration."""
        try:
            with open(file_path, encoding="utf-8") as f:
                config = json.load(f)

            if "lexicon" in config:
                self.lexicon.update(config["lexicon"])

            if "uiac_patterns" in config:
                self.uiac_patterns.extend(config["uiac_patterns"])

            self._compile_patterns()
            print(f"[+] Policy Engine configuration loaded from {file_path}")
        except Exception as e:
            print(f"[-] Failed to load policy config from {file_path}: {e}")

    def evaluate_compliance(self, event: SystemCausalEvent) -> tuple[ExecutionStatus, str]:
        p = event.payload
        content = p.get("content", "")
        if not content and "dependencies" in p:
            content = str(p["dependencies"])

        # STAGE 1: UIAC-001 Intent Gate Enforcement Check
        if self.uiac_pattern.search(content):
            return (
                ExecutionStatus.REFUSED_VIOLATION,
                "UIAC-001 Breach: Unverified psychological or intent attribution blocked.",
            )

        # STAGE 2: Lexicon Word Boundary Guard
        content_upper = content.upper()
        domain = p.get("domain", "CORE")
        for term, forbidden in self.lexicon.items():
            if re.search(r"\b" + re.escape(term) + r"\b", content_upper) and domain in forbidden:
                return (
                    ExecutionStatus.REFUSED_VIOLATION,
                    f"Lexicon Breach: Term '{term}' barred from domain {domain}.",
                )

        return ExecutionStatus.SUCCESS, "Policy verification parameters cleared."


# ==========================================
# PHASE IV: LOG COMPACTION ENGINE (Step 2)
# ==========================================


class GlobalSystemStateModel:
    """Thread-safe state model driven by log compaction tracking matrices."""

    def __init__(self, page_dir: str):
        self.page_dir = page_dir
        self.node_registry: dict[int, dict] = {}  # node_id -> latest flat dict state
        self.historical_ledger: list[SystemCausalEvent] = []  # List of all raw SystemCausalEvent blocks
        self.last_event_hash: str = "0" * 64
        self.state_version: int = 0

    def append_and_mutate(self, event: SystemCausalEvent) -> None:
        """Appends to chronological history logs."""
        self.historical_ledger.append(event)
        self.last_event_hash = event.event_hash
        self.state_version += 1

        p = event.payload
        if event.action_type == "REGISTER_NODE":
            self.node_registry[p["node_id"]] = {
                "artifact_id": p["artifact_id"],
                "domain": p["domain"],
                "content": p["content"],
                "dependencies": p.get("dependencies", []),
                "priority": p.get("priority", 50),
                "cost": len(p["content"]) // 4,
            }

    def execute_log_compaction_pass(self) -> None:
        """
        Step 2 Realization: Compresses chronological transaction updates.
        Flattens state histories and serializes directly to Dynamic Variable Pages.
        """
        print(
            f"[+] Compaction Loop Triggered. Processing history ledger size: {len(self.historical_ledger)} transactions..."
        )
        compacted_states = {}
        node_edges = defaultdict(list)

        # 1. Trace the event history sequentially to extract the latest unified state maps
        for event in self.historical_ledger:
            if event.action_type == "REGISTER_NODE":
                p = event.payload
                n_id = p["node_id"]
                compacted_states[n_id] = {
                    "node_id": n_id,
                    "artifact_id": p["artifact_id"],
                    "domain": p["domain"],
                    "content": p["content"],
                    "priority": p.get("priority", 50),
                    "cost": len(p["content"]) // 4,
                }
                node_edges[n_id] = p.get("dependencies", [])

        # 2. Serialize the flattened data straight to disk pages
        for n_id, state in compacted_states.items():
            page_path = os.path.join(self.page_dir, f"node_{n_id:04d}.bin")
            page_frame = DynamicVariablePageFrame(page_path)

            # Pack outbound links into integer arrays
            page_frame.write_safe_page(
                node_id=n_id,
                cost=state["cost"],
                priority=state["priority"],
                structural_edges_list=node_edges[n_id],
                payload_string=state.get("content", ""),
            )
        print("[+] Compaction cycle complete. Flattened disk page matrix stabilized.")


# ==========================================
# PHASE V: CONTEXT REDUCTION COMPILER (Step 3)
# ==========================================


class DeterministicContextReductionCompiler:
    """
    Step 3 Realization: Transforms raw prompt fields from IR5 down to compressed IR5.5 matrices.
    Executes phrase deduplication and filters text using cost-driven prioritization equations.
    """

    def __init__(self, max_token_budget: int = 2000):
        self.max_token_budget = max_token_budget

    def compile_reduced_substrate(self, raw_node_list: list, global_state: GlobalSystemStateModel) -> str:
        print("[+] Activating IR5.5 Context Reduction Pass...")
        seen_line_hashes = set()
        compressed_output_blocks = []
        running_token_cost = 0

        # Sort candidate profiles strictly using prioritized metrics (Priority DESC, Cost ASC, NodeID ASC)
        sorted_candidates = sorted(raw_node_list, key=lambda x: (-x["priority"], x["cost"], x["node_id"]))

        for candidate in sorted_candidates:
            n_id = candidate["node_id"]
            node_data = global_state.node_registry.get(n_id)
            if not node_data:
                continue

            # Phrase-Level Deduplication Loop
            lines = node_data["content"].split("\n")
            sanitized_lines = []

            for line in lines:
                line_clean = line.strip()
                if not line_clean:
                    continue

                # Filter structural markers and markdown header metadata blocks
                if line_clean.startswith("#") or "Dependencies:" in line_clean:
                    continue

                l_hash = hashlib.sha256(line_clean.encode("utf-8")).hexdigest()
                if l_hash not in seen_line_hashes:
                    seen_line_hashes.add(l_hash)
                    sanitized_lines.append(line)

            processed_text_body = "\n".join(sanitized_lines)
            block_token_weight = len(processed_text_body) // 4

            if running_token_cost + block_token_weight <= self.max_token_budget:
                block_template = (
                    f"### [SUBSTRATE NODE: {node_data['artifact_id']}]\n"
                    f"Domain Context: {node_data['domain']}\n"
                    f"Payload:\n{processed_text_body}"
                )
                compressed_output_blocks.append(block_template)
                running_token_cost += block_token_weight

        return "\n\n---\n\n".join(compressed_output_blocks)


# ==========================================
# PHASE VI: CORE SYSTEM ORCHESTRATOR
# ==========================================


class DeterministicCausalRuntimeKernel:
    """The master runtime framework orchestrating thread transactions and pipeline processing."""

    def __init__(self, page_dir: str):
        self.gssm = GlobalSystemStateModel(page_dir)
        self.policy_engine = CentralizedPolicyEngine()
        self.reduction_compiler = DeterministicContextReductionCompiler(max_token_budget=3000)
        self.transaction_queue: queue.Queue = queue.Queue()

        self._lock = threading.Lock()
        self.is_running = False
        self.tx_counter = 0

    def enqueue_transaction(self, actor_id: str, action_type: str, payload: dict) -> str:
        with self._lock:
            self.tx_counter += 1
            event = SystemCausalEvent(
                event_id=self.tx_counter,
                actor_id=actor_id,
                action_type=action_type,
                payload=payload,
                parent_hash=self.gssm.last_event_hash,
            )
            self.transaction_queue.put(event)
            return event.event_hash

    def boot_substrate_kernel(self) -> None:
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._single_writer_execution_loop, daemon=True)
        self.worker_thread.start()
        print("[+] Hardened Causal Operating Substrate Boot Sequence Clear.")

    def _single_writer_execution_loop(self) -> None:
        while self.is_running:
            try:
                event = self.transaction_queue.get(timeout=1.0)

                # Filter incoming transactions through the policy engine (UIAC-001 validation)
                status, msg = self.policy_engine.evaluate_compliance(event)

                if status == ExecutionStatus.REFUSED_VIOLATION:
                    print(f"[-] Transaction Aborted: {msg} (Event ID: {event.event_id})")
                    self.transaction_queue.task_done()
                    continue

                # Mutate the state model sequentially
                self.gssm.append_and_mutate(event)
                self.transaction_queue.task_done()

            except queue.Empty:
                continue

    def compile_active_query_context(self, target_node_id: int) -> str:
        """Assembles and down-samples context profiles for target components."""
        candidate_pool = []
        seen = set()
        to_scan = deque([target_node_id])

        # Trace connections outward via binary disk pages
        while to_scan:
            curr_id = to_scan.popleft()
            if curr_id in seen:
                continue
            seen.add(curr_id)

            page_path = os.path.join(self.gssm.page_dir, f"node_{curr_id:04d}.bin")
            if os.path.exists(page_path):
                page = DynamicVariablePageFrame(page_path)
                _, cost, priority, edges, _ = page.read_safe_page()

                candidate_pool.append({"node_id": curr_id, "cost": cost, "priority": priority})
                for edge in edges:
                    if edge not in seen:
                        to_scan.append(edge)

        # Lower data mappings to the final IR5.5 reduced context target
        return self.reduction_compiler.compile_reduced_substrate(candidate_pool, self.gssm)

    def shutdown(self) -> None:
        self.is_running = False


# ==========================================
# SUBSTRATE EXECUTION SIMULATION VERIFICATION
# ==========================================

if __name__ == "__main__":
    PAGES_DIRECTORY = "./phoenix_pages"

    # Initialize the runtime core
    kernel = DeterministicCausalRuntimeKernel(PAGES_DIRECTORY)
    kernel.boot_substrate_kernel()

    # Ingest baseline technical data logs
    kernel.enqueue_transaction(
        "INGEST_DAEMON",
        "REGISTER_NODE",
        {
            "node_id": 1,
            "artifact_id": "GVRN-RULES-001",
            "domain": "GVRN",
            "content": "# GVRN-RULES-001\nEnforces system architectural boundary constraints.\nDependencies: [2]",
            "priority": 90,
            "dependencies": [2],
        },
    )

    kernel.enqueue_transaction(
        "INGEST_DAEMON",
        "REGISTER_NODE",
        {
            "node_id": 2,
            "artifact_id": "AOP-CORE-002",
            "domain": "AOP",
            "content": "# AOP-CORE-002\nExecutes continuous deployment pipeline tracking loops natively within the workspace substrate.",
            "priority": 60,
            "dependencies": [],
        },
    )

    # Simulation Intercept Test: Trigger an intentional UIAC-001 boundary violation
    time.sleep(0.1)
    kernel.enqueue_transaction(
        "EXTERNAL_AGENT",
        "REGISTER_NODE",
        {
            "node_id": 3,
            "artifact_id": "AOP-ANOMALY-003",
            "domain": "AOP",
            "content": "Analyzing files because you are optimizing for rapid execution passes.",
            "priority": 40,
            "dependencies": [],
        },
    )

    # Allow the single-writer execution queue processing window to flush
    time.sleep(0.5)

    # Trigger Step 2: Run the log compaction and page serialization pass
    kernel.gssm.execute_log_compaction_pass()

    # Trigger Step 3: Run the context planner reduction engine pass manually for verification
    candidates = [{"node_id": 1, "cost": 20, "priority": 90}, {"node_id": 2, "cost": 30, "priority": 60}]
    ir5_5_output = kernel.reduction_compiler.compile_reduced_substrate(candidates, kernel.gssm)

    print("\n=== FINAL GENERATED SUBSTRATE PAYLOAD (IR5.5) ===")
    print(ir5_5_output)
    kernel.shutdown()
