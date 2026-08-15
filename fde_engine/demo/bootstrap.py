"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-DEMO-BOOTSTRAP` | The Sovereign ID. |
| **Official Name** | `bootstrap.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `DEMO`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/demo/bootstrap.py`

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

from fde_engine.core.chunk_executor import ChunkExecutor
from fde_engine.core.engine_runtime import EngineRuntime
from fde_engine.core.rollback_core import InputLog, RollbackEngine, SnapshotBuffer
from fde_engine.dag.dag_compiler import DAGCompiler
from fde_engine.ecs.archetype_storage import Archetype
from fde_engine.ecs.ecs_scheduler import ECSScheduler, SystemTask
from fde_engine.ecs.world import World
from fde_engine.systems.movement_system import MovementSystem, Position, Velocity


def main():
    # 1. Create world & populate test entities
    world = World()
    eid = world.registry.create()
    sig = frozenset([Position, Velocity])
    world.registry._archetypes[sig] = Archetype(sig)
    row = world.registry._archetypes[sig].add_entity(eid, {Position: Position(0.0, 0.0), Velocity: Velocity(1.0, 2.0)})
    world.registry._entity_index[eid] = (sig, row)

    # 2. Register systems
    systems = [MovementSystem()]

    # 3. Compile DAG layers
    compiler = DAGCompiler(systems)
    layers = compiler.compile_layers()
    wrapped_layers = [[SystemTask(s) for s in layer] for layer in layers]

    # 4. Create Executor & Scheduler
    executor = ChunkExecutor(max_workers=4, chunk_size=256)
    scheduler = ECSScheduler(executor, wrapped_layers)

    # 5. Create Rollback components
    input_log = InputLog()
    snapshots = SnapshotBuffer(size=60)
    rollback = RollbackEngine(executor, scheduler, input_log, snapshots)

    # 6. Initialize Runtime
    engine = EngineRuntime(world, scheduler, rollback)

    # 7. Run frames
    print("[BOOTSTRAP] Running 10 deterministic simulation ticks...")
    for i in range(10):
        engine.tick(inputs={})
        print(f"Frame {world.frame} complete")

    final_pos = world.registry._archetypes[sig].columns[Position][row]
    print(f"[BOOTSTRAP] Entity 1 Final Position: {final_pos}")
    print("[BOOTSTRAP] Simulation completed successfully.")


if __name__ == "__main__":
    main()

