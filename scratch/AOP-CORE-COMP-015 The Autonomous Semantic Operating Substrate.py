import os
import json
import re
import struct
import mmap
import time
import hashlib
from enum import Enum, auto
from collections import defaultdict, deque

# ==========================================
# PHASE I: STRONGLY-TYPED SYSTEM INTERFACES
# ==========================================

class IRLayer(Enum):
    IR0_RAW_AST = auto()
    IR1_LINKED_GRAPH = auto()
    IR2_INFERRED_CLOSURE = auto()
    IR3_RUNTIME_SUBSTRATE = auto()

class EdgeOntology(Enum):
    STRUCTURAL = auto()
    GOVERNANCE = auto()
    EXECUTION = auto()

class Edge:
    """First-Class relational edge pinned to an explicit Ontological Plane."""
    def __init__(self, source_id, target_id, kind, ontology: EdgeOntology):
        self.source_id = source_id
        self.target_id = target_id
        self.kind = kind
        self.ontology = ontology
        self.timestamp = 1781201520  # Explicit 2026 Temporal Alignment Sync

class StructuralDiff:
    """Captures granular attribute deltas across execution steps."""
    def __init__(self):
        self.added = {}
        self.removed = {}
        self.modified = {}

    def is_empty(self) -> bool:
        return not (self.added or self.removed or self.modified)

class InferencePath:
    """Tracks the complete, unbroken lineage history of inherited laws."""
    def __init__(self, law_id, path_sequence):
        self.law_id = law_id
        self.path = path_sequence  # Step trace vector: [AOP-001, UMB-001, Law-11]

class SectionNode:
    def __init__(self, kind, content):
        self.kind = kind
        self.content = content.strip()
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()

# ==========================================
# PHASE II: PERSISTENT MEMORY-MAPPED STACK
# ==========================================

class MMAPSCCFrame:
    """
    Durable, offset-addressable binary container for an SCC macro-node execution frame.
    Elimines slow runtime text serialization loops.
    """
    HEADER_FMT = "<III I 32s"  # scc_id, version, dirty, state_size, state_hash

    def __init__(self, file_path, scc_int_id):
        self.file_path = file_path
        self.scc_int_id = scc_int_id
        self._initialize_storage()

    def _initialize_storage(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "wb") as f:
                f.write(b"\x00" * 4096)  # Direct page boundary block allocation

        self.f = open(self.file_path, "r+b")
        self.mm = mmap.mmap(self.f.fileno(), 0)

    def read_frame_state(self) -> dict:
        self.mm.seek(0)
        header_size = struct.calcsize(self.HEADER_FMT)
        header_bytes = self.mm.read(header_size)
        
        scc_id, version, dirty, state_size, state_hash = struct.unpack(self.HEADER_FMT, header_bytes)
        if state_size == 0:
            return {}
            
        state_blob = self.mm.read(state_size)
        return json.loads(state_blob.decode('utf-8'))

    def write_frame_state(self, state_dict, version=1, dirty=0):
        # Secure binary serialization replaces primitive eval blocks
        state_blob = json.dumps(state_dict).encode('utf-8')
        state_size = len(state_blob)
        state_hash = hashlib.sha256(state_blob).digest()

        header = struct.pack(
            self.HEADER_FMT,
            self.scc_int_id,
            version,
            1 if dirty else 0,
            state_size,
            state_hash
        )

        self.mm.seek(0)
        self.mm.write(header + state_blob)
        self.mm.flush()

    def close(self):
        self.mm.close()
        self.f.close()

# ==========================================
# PHASE III: AUTOMATED LOOP CONTROL PLANE
# ==========================================

class BiDirectionalDependencyIndex:
    """Maintains highly efficient tracking vectors for change invalidation processing."""
    def __init__(self):
        self.forward = defaultdict(set)  # node_id -> set(dependencies)
        self.reverse = defaultdict(set)  # node_id -> set(parent_nodes)

    def register_edge(self, src, dst):
        self.forward[src].add(dst)
        self.reverse[dst].add(src)

    def clear_node_edges(self, node_id):
        if node_id in self.forward:
            for dst in self.forward[node_id]:
                if node_id in self.reverse[dst]:
                    self.reverse[dst].remove(node_id)
            del self.forward[node_id]

class TarjanSCCEngine:
    """Partitions complex cyclic loops into explicit execution units."""
    def __init__(self, index: BiDirectionalDependencyIndex):
        self.index = index
        self.index_map = {}
        self.lowlink = {}
        self.stack = []
        self.on_stack = set()
        self.sccs = []

    def compute_sccs(self) -> list:
        for node in list(self.index.forward.keys()):
            if node not in self.index_map:
                self._strong_connect(node)
        return self.sccs

    def _strong_connect(self, v):
        idx = len(self.index_map)
        self.index_map[v] = idx
        self.lowlink[v] = idx
        self.stack.append(v)
        self.on_stack.add(v)

        for w in self.index.forward.get(v, []):
            if w not in self.index_map:
                self._strong_connect(w)
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w])
            elif w in self.on_stack:
                self.lowlink[v] = min(self.lowlink[v], self.index_map[w])

        if self.lowlink[v] == self.index_map[v]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                scc.append(w)
                if w == v: break
            self.sccs.append(scc)

class SemiNaiveDirtyPropagator:
    """Executes breadth-first change propagation based exclusively on dirty worklists."""
    def __init__(self, index: BiDirectionalDependencyIndex):
        self.index = index

    def calculate_impact_radius(self, modified_scc_ids) -> set:
        queue = deque(modified_scc_ids)
        affected_set = set(modified_scc_ids)

        while queue:
            current_scc = queue.popleft()
            # Scan reverse links to identify impacted upstream systems
            for parent in self.index.reverse.get(current_scc, []):
                if parent not in affected_set:
                    affected_set.add(parent)
                    queue.append(parent)
        return affected_set

# ==========================================
# PHASE IV: DETECTING CHANGES & THE TRIAD POLICY
# ==========================================

class StructuralDiffEngine:
    """Tracks state updates step-by-step to prevent redundant re-computation loops."""
    def compute_delta(self, old_state: dict, new_state: dict) -> StructuralDiff:
        delta = StructuralDiff()
        old_keys = set(old_state.keys())
        new_keys = set(new_state.keys())

        for k in new_keys - old_keys:
            delta.added[k] = new_state[k]
        for k in old_keys - new_keys:
            delta.removed[k] = old_state[k]
        for k in old_keys & new_keys:
            if old_state[k] != new_state[k]:
                delta.modified[k] = (old_state[k], new_state[k])
        return delta

class CoreTriadPolicyEngine:
    """
    Natively runs the Core Triad (Sentinel, Axion, Sophia) inside the transformation loop,
    replacing primitive placeholder logic with real system rules.
    """
    def __init__(self):
        # Strongly typed Ontological Lexicon boundary rules
        self.lexicon = {
            "THE FORGE": ["PERSISTENCE", "DATA"],
            "COGNITIVE CIRCUIT BREAKER": ["PRESENTATION"]
        }
        self.rnc_pattern = re.compile(r"\b(?:CORE|UMB|AOP|GUCA|SELT|GVRN|CPD|CBM)-[A-Z0-9_]+-\d+\b")

    def transform_and_govern(self, node_id, domain, key, raw_value) -> str:
        value_str = str(raw_value)
        
        # 1. THE SENTINEL (Conscience): Enforces Lexicon Boundaries and the SovereignFabric Axiom
        for term, forbidden_domains in self.lexicon.items():
            if re.search(r"\b" + re.escape(term) + r"\b", value_str.upper()):
                if domain in forbidden_domains:
                    print(f"[-] Sentinel Intervention: Term '{term}' blocked within forbidden domain {domain} at {node_id}")
                    return "[LEXICON_VIOLATION_SANCTIONS]"

        # SovereignFabric Check: Internal paths must use relative configurations; global aliases are barred internally
        if "@" in value_str and not value_str.startswith(f"@{domain.lower()}"):
            print(f"[-] Sentinel Enforcer: SovereignFabric alias leak blocked within {node_id}")
            return "[SOVEREIGN_FABRIC_LEAK_REMEDIATED]"

        # 2. THE AXION (Logic): Validates structural configurations and resolves module dependencies
        if key == "dependencies":
            found_symbols = self.rnc_pattern.findall(value_str)
            return ", ".join(list(set(found_symbols)))

        # 3. THE SOPHIA (Forethought): Tracks rule transmission histories to maintain systemic clarity
        if key == "policy_link" and domain != "GVRN":
            print(f"[-] Sophia Forethought: Policy link projection blocked from non-governance artifact {node_id}")
            return "[INVALID_POLICY_PROJECTION]"

        return raw_value

# ==========================================
# PHASE V: PERSISTENT RUNTIME KERNEL
# ==========================================

class AutonomousSemanticOSSubstrate:
    """The master runtime engine coordinating file hot-reloads and partitioned loop processing."""
    def __init__(self, vault_dir, db_dir):
        self.vault_dir = vault_dir
        self.db_dir = db_dir
        os.makedirs(db_dir, exist_ok=True)

        self.symbol_table = {}          # node_id -> domain string
        self.node_to_scc_map = {}       # node_id -> scc_macro_id
        self.scc_members_map = {}       # scc_macro_id -> list(node_ids)
        self.macro_frames = {}          # scc_macro_id -> MMAPSCCFrame object
        
        self.graph_index = BiDirectionalDependencyIndex()
        self.diff_engine = StructuralDiffEngine()
        self.policy_engine = CoreTriadPolicyEngine()
        self.propagator = SemiNaiveDirtyPropagator(self.graph_index)

    def ingest_initial_vault(self):
        print("[+] Commencing initial repository ingestion pass...")
        raw_deps_cache = {}

        # Scan and load the source workspace directory
        for root, _, files in os.walk(self.vault_dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    node_id, domain, deps, sections = self._parse_source_file(path)
                    
                    self.symbol_table[node_id] = domain
                    raw_deps_cache[node_id] = deps
                    
                    # Register foundational links in the dependency index
                    for dep in deps:
                        self.graph_index.register_edge(node_id, dep)

        # Compute strongly connected components across the registry map
        tarjan = TarjanSCCEngine(self.graph_index)
        sccs = tarjan.compute_sccs()

        # Build and format persistent macro execution frames
        for idx, scc in enumerate(sccs):
            scc_macro_id = f"SCC_MACRO_{idx:03d}"
            self.scc_members_map[scc_macro_id] = scc
            
            frame_path = os.path.join(self.db_dir, f"{scc_macro_id}.bin")
            self.macro_frames[scc_macro_id] = MMAPSCCFrame(frame_path, idx)
            
            # Initialize seed data across the active nodes
            initial_state = {}
            for node_id in scc:
                self.node_to_scc_map[node_id] = scc_macro_id
                initial_state[f"{node_id}.dependencies"] = ", ".join(raw_deps_cache[node_id])
                initial_state[f"{node_id}.status"] = "INITIALIZED"
            
            self.macro_frames[scc_macro_id].write_frame_state(initial_state, version=1, dirty=1)

    def trigger_runtime_mutation(self, modified_node_id, key, new_raw_value):
        """API Layer: Processes individual text edits incrementally without triggering full system recompiles."""
        scc_macro_id = self.node_to_scc_map.get(modified_node_id)
        if not scc_macro_id:
            return

        print(f"\n[MUTATION] Node {modified_node_id} -> Mutating {key}...")
        frame = self.macro_frames[scc_macro_id]
        current_state = frame.read_frame_state()
        
        # Apply the Core Triad governance checks to evaluate the raw value mutation
        domain = self.symbol_table.get(modified_node_id, "CORE")
        sanitized_value = self.policy_engine.transform_and_govern(modified_node_id, domain, key, new_raw_value)
        
        state_key = f"{modified_node_id}.{key}"
        current_state[state_key] = sanitized_value
        
        # Calculate localized structural metrics
        old_frame_state = frame.read_frame_state()
        delta = self.diff_engine.compute_delta(old_frame_state, current_state)
        
        if delta.is_empty():
            print("    -> Value change matches current state. Invalidation wave skipped.")
            return

        # Commit updates directly to the memory-mapped layer
        frame.write_frame_state(current_state, version=1, dirty=1)

        # Trigger semi-naive dirty propagation across the tracking index
        impacted_scc_ids = self.propagator.calculate_impact_radius([scc_macro_id])
        print(f"[PROPAGATION] Invalidation wave complete. Impacted cluster count: {len(impacted_scc_ids)}")

        # Step Phase: Execute only the dirty macro-nodes identified in the impact path
        for dirty_scc_id in impacted_scc_ids:
            self._step_macro_node(dirty_scc_id)

    def _step_macro_node(self, scc_macro_id):
        frame = self.macro_frames[scc_macro_id]
        state = frame.read_frame_state()
        members = self.scc_members_map[scc_macro_id]
        
        print(f"    -> Running local fixed-point solver loop inside cluster {scc_macro_id}...")
        loop_cycles = 0
        state_changed = True
        
        while state_changed:
            loop_cycles += 1
            state_changed = False
            updated_state = dict(state)
            
            for node_id in members:
                domain = self.symbol_table.get(node_id, "CORE")
                dep_key = f"{node_id}.dependencies"
                
                if dep_key in state:
                    # Run the rule loop to propagate cascading values across internal links
                    current_deps = state[dep_key]
                    transformed_deps = self.policy_engine.transform_and_govern(node_id, domain, "dependencies", current_deps)
                    updated_state[dep_key] = transformed_deps

            # Verify local structural convergence via hash matching
            if updated_state != state:
                state = updated_state
                state_changed = True
            
            if loop_cycles > 20:
                print(f"    [!] Oscillation Warning: Unstable feedback loop halted inside component {scc_macro_id}")
                break

        # Flush the finalized execution states back to disk memory layers
        frame.write_frame_state(state, version=1, dirty=0)
        print(f"    -> Component stabilized in {loop_cycles} loop iterations.")

    def run_live_filesystem_reloader_loop(self):
        """Watcher Module: Automatically tracks files and applies live updates directly to the engine."""
        print("\n[+] Substrate active. Live file system hot-reloader monitoring active...")
        last_seen_hashes = {}

        try:
            while True:
                for root, _, files in os.walk(self.vault_dir):
                    for file in files:
                        if file.endswith('.md'):
                            path = os.path.join(root, file)
                            try:
                                with open(path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                                if last_seen_hashes.get(path) != file_hash:
                                    # Trigger an incremental update pass if an explicit file change is detected
                                    if path in last_seen_hashes:
                                        node_id, domain, deps, sections = self._parse_source_file(path)
                                        print(f"\n[HOT RELOAD] File system update detected for module: {node_id}")
                                        self.trigger_runtime_mutation(node_id, "dependencies", ", ".join(deps))
                                    last_seen_hashes[path] = file_hash
                            except Exception as e:
                                pass
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[-] Shutting down Persistent SVM Engine Substrate.")
            self.shutdown()

    def _parse_source_file(self, file_path) -> tuple:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        filename = os.path.basename(file_path)
        rnc_pattern = re.compile(r"\b(?:CORE|UMB|AOP|GUCA|SELT|GVRN|CPD|CBM)-[A-Z0-9_]+-\d+\b")
        
        rnc_match = rnc_pattern.search(filename) or rnc_pattern.search(text)
        artifact_id = rnc_match.group(0) if rnc_match else filename.replace(".md", "")
        domain = artifact_id.split("-")[0] if "-" in artifact_id else "CORE"
        
        dependencies = list(set(rnc_pattern.findall(text)))
        if artifact_id in dependencies:
            dependencies.remove(artifact_id)
            
        blocks = re.split(r'\n---+\n', text)
        sections = [SectionNode("CORE", b) for b in blocks if b.strip()]
        return artifact_id, domain, dependencies, sections

    def shutdown(self):
        for frame in self.macro_frames.values():
            frame.close()

# ==========================================
# SUBSTRATE INITIALIZATION ENGINE ENTRY
# ==========================================

if __name__ == "__main__":
    VAULT_DIRECTORY = "./Phoenix_Vault"
    DATABASE_DIRECTORY = "./phoenix_substrate_db"

    # Generate a sandbox file layout to verify core functionality
    os.makedirs(VAULT_DIRECTORY, exist_ok=True)
    
    # Write a base governance rule file to seed the environment
    with open(os.path.join(VAULT_DIRECTORY, "GVRN-RULES-001.md"), "w") as f:
        f.write("# GVRN-RULES-001\n---\nWHAT: Core System Governance Constraints.\n---\nDependencies: UMB-CORE-002")
        
    # Write a blueprint module dependent on our core guidelines
    with open(os.path.join(VAULT_DIRECTORY, "UMB-CORE-002.md"), "w") as f:
        f.write("# UMB-CORE-002\n---\nHOW: Structural Implementation Layer.\n---\nDependencies: GVRN-RULES-001, @global/leak")

    # Initialize the Autonomous Semantic OS Substrate
    substrate_os = AutonomousSemanticOSSubstrate(VAULT_DIRECTORY, DATABASE_DIRECTORY)
    substrate_os.ingest_initial_vault()
    
    # Run an manual test mutation to verify validation loop containment
    substrate_os.trigger_runtime_mutation("GVRN-RULES-001", "dependencies", "UMB-CORE-002, THE FORGE")
    
    # Engage the file watcher engine pass
    substrate_os.run_live_filesystem_reloader_loop()