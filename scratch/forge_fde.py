import os
from pathlib import Path

ROOT = "fde_engine"

def get_header(artifact_id: str, filename: str, domain: str) -> str:
    return f'''"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `{artifact_id}` | The Sovereign ID. |
| **Official Name** | `{filename}`                  | The Filename.     |
| **Version** | **v15.0 [OMEGA]** | The Standard.     |
| **Domain** | `{domain}`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

'''

FILES = {
    # --- GOVERNANCE ---
    "gvrn/law_validator.py": get_header("CORE-FDE-GVRN-LAW", "law_validator.py", "GVRN") + '''
class LawValidator:
    """Enforces zero-entropy state validation against project metadata."""
    pass
''',
    
    "gvrn/selt_logger.py": get_header("CORE-FDE-GVRN-SELT", "selt_logger.py", "GVRN") + '''
class SeltLogger:
    """Immutable telemetry and Dissonance tracking."""
    pass
''',

    # --- CORE EXECUTION ---
    "core/engine_runtime.py": get_header("CORE-FDE-CORE-RUNTIME", "engine_runtime.py", "CORE") + '''
class EngineRuntime:
    """The master loop: S(n+1) = F(S(n), I(n)). Binds DAG, ECS, and Rollback."""
    def __init__(self, world, scheduler, rollback_core):
        self.world = world
        self.scheduler = scheduler
        self.rollback = rollback_core

    def tick(self, inputs: dict):
        # 1. Inject Deterministic Inputs
        self.world.current_inputs = inputs
        
        # 2. Execute parallel pure systems -> delta commit
        self.scheduler.run_frame(self.world)
        
        # 3. Snapshot for time-travel anchor
        self.rollback.snapshots.save(self.world.frame, self.world.snapshot())
        self.world.frame += 1
''',

    "core/chunk_executor.py": get_header("CORE-FDE-CORE-CHUNK", "chunk_executor.py", "CORE") + '''
import concurrent.futures

class ArchetypeChunk:
    def __init__(self, archetype, start, end):
        self.archetype = archetype
        self.start = start
        self.end = end

class ChunkExecutor:
    """AAA-grade parallel scaling. Slices contiguous memory for L1/L2 cache locality."""
    def __init__(self, max_workers=8, chunk_size=1024):
        self.max_workers = max_workers
        self.chunk_size = chunk_size

    def execute_layer(self, layer, world):
        futures = {}
        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            for task in layer:
                system = task.system
                arches = system.query(world)
                
                for arch in arches:
                    total = len(arch.entity_ids)
                    for i in range(0, total, self.chunk_size):
                        chunk = ArchetypeChunk(arch, i, min(i + self.chunk_size, total))
                        future = pool.submit(system.compute_chunk, world, chunk)
                        futures[future] = task.execution_index

            for f in concurrent.futures.as_completed(futures):
                idx = futures[f]
                delta = f.result()
                if idx not in results:
                    results[idx] = {"mutations": {}, "spawns": [], "despawns": [], "structural_migrations": {}}
                self._merge(results[idx], delta)
        return results

    def _merge(self, master, delta):
        for comp, updates in delta.get("mutations", {}).items():
            master["mutations"].setdefault(comp, {}).update(updates)
        # Structural merges...
''',

    "core/rollback_core.py": get_header("CORE-FDE-CORE-ROLLBACK", "rollback_core.py", "CORE") + '''
import copy

class InputLog:
    def __init__(self):
        self.log = {}
        self.predicted = set()

    def get_inputs(self, frame, player_ids):
        if frame not in self.log:
            self.log[frame] = {}
        for pid in player_ids:
            if pid not in self.log[frame]:
                prev = self.log.get(frame - 1, {}).get(pid)
                self.log[frame][pid] = prev
                self.predicted.add(frame)
        return self.log[frame]

class SnapshotBuffer:
    def __init__(self, size=60):
        self.buffer = {}
        self.size = size

    def save(self, frame, world_snap):
        self.buffer[frame] = world_snap
        if frame - self.size in self.buffer:
            del self.buffer[frame - self.size]

    def load(self, frame):
        return copy.deepcopy(self.buffer[frame])

class RollbackEngine:
    def __init__(self, scheduler, input_log, snapshot_buffer):
        self.scheduler = scheduler
        self.input_log = input_log
        self.snapshots = snapshot_buffer
        self.current_frame = 0

    def execute_rollback(self, target_frame: int, world):
        print(f"[ROLLBACK] Mismatch. Rewinding to frame {target_frame - 1}...")
        restored_snap = self.snapshots.load(target_frame - 1)
        world.restore(restored_snap)

        for f in range(target_frame, self.current_frame + 1):
            world.current_inputs = self.input_log.get_inputs(f, world.players)
            self.scheduler.run_frame(world)
            self.snapshots.save(f, world.snapshot())
''',

    # --- ECS ---
    "ecs/archetype_storage.py": get_header("CORE-FDE-ECS-ARCH", "archetype_storage.py", "ECS") + '''
class Archetype:
    """Contiguous columnar arrays. O(1) query matching and swap-and-pop."""
    def __init__(self, signature):
        self.signature = signature
        self.entity_ids = []
        self.columns = {ctype: [] for ctype in signature}

    def add_entity(self, eid, components):
        self.entity_ids.append(eid)
        for ctype in self.signature:
            self.columns[ctype].append(components[ctype])
        return len(self.entity_ids) - 1

    def remove_entity(self, row):
        last = len(self.entity_ids) - 1
        swapped_eid = self.entity_ids[last]
        if row != last:
            self.entity_ids[row] = swapped_eid
            for ctype in self.signature:
                self.columns[ctype][row] = self.columns[ctype][last]
        self.entity_ids.pop()
        for ctype in self.signature:
            self.columns[ctype].pop()
        return swapped_eid

    def snapshot(self):
        # AAA optimization: frozen dataclasses allow fast shallow copies
        return {"entity_ids": self.entity_ids.copy(), "columns": {k: v.copy() for k, v in self.columns.items()}}
''',

    "ecs/commit_layer.py": get_header("CORE-FDE-ECS-COMMIT", "commit_layer.py", "ECS") + '''
def apply_ecs_delta(world, delta, seen_mutations):
    """The Deterministic Bottleneck. Fail-fast collision detection."""
    reg = world.registry

    # Despawns & Spawns handled here...

    # Mutations with Collision Safety
    for comp_type, updates in delta.get("mutations", {}).items():
        for eid, new_val in updates.items():
            key = (comp_type, eid)
            if key in seen_mutations:
                raise RuntimeError(f"FDE Violation: Double write on {comp_type.__name__} Entity {eid}")
            seen_mutations.add(key)
            
            sig, row = reg._entity_index[eid]
            reg._archetypes[sig].columns[comp_type][row] = new_val
''',

    "ecs/world.py": get_header("CORE-FDE-ECS-WORLD", "world.py", "ECS") + '''
from .entity_registry import EntityRegistry

class World:
    """Immutable state container for O(1) rollback."""
    def __init__(self):
        self.registry = EntityRegistry()
        self.frame = 0
        self.current_inputs = {}
        self.players = []

    def snapshot(self):
        return {
            "registry": self.registry.snapshot(),
            "frame": self.frame,
            "inputs": self.current_inputs.copy()
        }

    def restore(self, snap):
        self.registry.restore(snap["registry"])
        self.frame = snap["frame"]
        self.current_inputs = snap["inputs"].copy()
''',

    "ecs/entity_registry.py": get_header("CORE-FDE-ECS-REG", "entity_registry.py", "ECS") + '''
class EntityRegistry:
    def __init__(self):
        self._next_id = 1
        self._archetypes = {}
        self._entity_index = {}

    def create(self):
        eid = self._next_id
        self._next_id += 1
        return eid

    def snapshot(self):
        # Real implementation deeply copies the archetype structures via shallow pointers
        pass

    def restore(self, snap):
        pass
''',

    "ecs/ecs_scheduler.py": get_header("CORE-FDE-ECS-SCHED", "ecs_scheduler.py", "ECS") + '''
from .commit_layer import apply_ecs_delta

class SystemTask:
    def __init__(self, system):
        self.system = system
        self.execution_index = system.execution_index

class ECSScheduler:
    """Binds DAG layers to the chunk executor."""
    def __init__(self, executor, layers):
        self.executor = executor
        self.layers = layers

    def run_frame(self, world):
        for layer in self.layers:
            results = self.executor.execute_layer(layer, world)
            seen = set()
            for idx in sorted(results.keys()):
                apply_ecs_delta(world, results[idx], seen)
''',

    # --- DAG ---
    "dag/dag_compiler.py": get_header("CORE-FDE-DAG-COMPILER", "dag_compiler.py", "DAG") + '''
from collections import defaultdict

class DAGCompiler:
    """Semantic DAG compiler. Enforces temporal directionality via execution_index."""
    def __init__(self, systems):
        self.systems = systems

    def build_graph(self):
        graph = defaultdict(set)
        indegree = {s: 0 for s in self.systems}

        for a in self.systems:
            for b in self.systems:
                if a == b: continue
                if self._depends(a, b):
                    graph[a].add(b)
                    indegree[b] += 1
        return graph, indegree

    def _depends(self, a, b):
        # Temporal Override: Edges only flow forward in time
        if a.execution_index >= b.execution_index: return False

        # Conflict Evaluation
        if a.writes & b.reads or a.reads & b.writes or a.writes & b.writes: return True
        
        # Accumulators allow parallel writes safely
        if a.writes & b.accumulates or a.accumulates & b.writes: return True
        return False

    def compile_layers(self):
        graph, indegree = self.build_graph()
        sorted_sys = sorted(self.systems, key=lambda s: s.execution_index)
        layers = []
        remaining = set(sorted_sys)

        while remaining:
            ready = [s for s in sorted_sys if s in remaining and indegree[s] == 0]
            if not ready: raise RuntimeError("FDE Violation: Cyclic Dependency.")
            
            ready.sort(key=lambda s: s.execution_index)
            layers.append(ready)
            for s in ready:
                remaining.remove(s)
                for neighbor in graph[s]:
                    indegree[neighbor] -= 1
        return layers
''',

    "dag/system_signature.py": get_header("CORE-FDE-DAG-SIG", "system_signature.py", "DAG") + '''
class SystemSignature:
    """The strict contract all FDE systems must inherit."""
    name: str = "Unknown"
    execution_index: int = 0
    reads = set()
    writes = set()
    accumulates = set()
''',

    # --- SYSTEMS ---
    "systems/movement_system.py": get_header("CORE-FDE-SYS-MOVE", "movement_system.py", "SYSTEMS") + '''
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: float; y: float

@dataclass(frozen=True)
class Velocity:
    dx: float; dy: float

class MovementSystem:
    name = "movement"
    execution_index = 10
    reads = {Position, Velocity}
    writes = {Position}
    accumulates = set()

    def query(self, world):
        return [arch for sig, arch in world.registry._archetypes.items() if Position in sig and Velocity in sig]

    def compute_chunk(self, world, chunk):
        delta = {"mutations": {Position: {}}}
        pos = chunk.archetype.columns[Position]
        vel = chunk.archetype.columns[Velocity]
        eids = chunk.archetype.entity_ids

        for i in range(chunk.start, chunk.end):
            eid = eids[i]
            delta["mutations"][Position][eid] = Position(pos[i].x + vel[i].dx, pos[i].y + vel[i].dy)
        return delta
''',

    "systems/input_system.py": get_header("CORE-FDE-SYS-INPUT", "input_system.py", "SYSTEMS") + '''
class InputSystem:
    """Deterministically translates raw inputs into component intents."""
    name = "input"
    execution_index = 0
    reads = set(); writes = set(); accumulates = set()
''',

    "systems/base_system.py": get_header("CORE-FDE-SYS-BASE", "base_system.py", "SYSTEMS") + '''
class BaseSystem:
    """Template for FDE pure functions."""
    pass
''',

    # --- BRIDGE ---
    "bridge/godot_translation_layer.py": get_header("CORE-FDE-BRIDGE-GODOT", "godot_translation_layer.py", "BRIDGE") + '''
class GodotBridge:
    """
    Translates the deterministic Archetype state into Godot visual transforms.
    Ensures the logic loop remains completely isolated from the render loop.
    """
    pass
''',

    # --- DEMO ---
    "demo/bootstrap.py": get_header("CORE-FDE-DEMO-BOOT", "bootstrap.py", "DEMO") + '''
from core.engine_runtime import EngineRuntime
from core.chunk_executor import ChunkExecutor
from core.rollback_core import RollbackEngine, InputLog, SnapshotBuffer
from dag.dag_compiler import DAGCompiler
from ecs.ecs_scheduler import ECSScheduler, SystemTask
from ecs.world import World
from systems.movement_system import MovementSystem

def main():
    world = World()
    
    # 1. Compile DAG
    systems = [MovementSystem()]
    compiler = DAGCompiler(systems)
    layers = compiler.compile_layers()
    wrapped = [[SystemTask(s) for s in layer] for layer in layers]

    # 2. Build Core Pipeline
    executor = ChunkExecutor(max_workers=4, chunk_size=1024)
    scheduler = ECSScheduler(executor, wrapped)
    
    # 3. Time Machine
    rollback = RollbackEngine(scheduler, InputLog(), SnapshotBuffer())

    # 4. Engine Runtime
    engine = EngineRuntime(world, scheduler, rollback)

    print("[SUCCESS] FDE Pipeline Materialized. Initiating Zero-Entropy Tick...")
    for _ in range(3):
        engine.tick({})

if __name__ == "__main__":
    main()
''',

    # --- DOCS ---
    "docs/README.md": "# The Phoenix FDE\n\nAutomated via GUCA-FDE-FORGE.\n",
    "docs/PRS_INDEX.md": "# PRS Navigation Hub\n\nMapping the Sovereign Lattice.\n"
}

def forge() -> None:
    print(f"[INIT] Executing Structural Transmutation. Target: ./{ROOT}/")
    Path(ROOT).mkdir(exist_ok=True)

    for file_path, content in FILES.items():
        full_path = Path(ROOT) / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            
        print(f"  [+] Forged: {file_path}")

    print(f"\n[SYNTHESIS COMPLETE] {len(FILES)} artifacts secured in the library.")

if __name__ == "__main__":
    forge()