"""
### **Block A: The Identification Lock (UIP-V15)**

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

from ecs.world import World
from core.engine_runtime import EngineRuntime
from core.parallel_executor import DeterministicParallelExecutor
from core.rollback_core import InputLog, RollbackEngine, SnapshotBuffer
from dag.dag_compiler import DAGCompiler
from ecs.ecs_scheduler import ECSScheduler, SystemTask
from systems.movement_system import MovementSystem


def main():
    # 1. Create world
    world = World()

    # 2. Register systems
    systems = [
        MovementSystem(),
    ]

    # 3. Compile DAG
    compiler = DAGCompiler(systems)
    layers = compiler.compile_layers()

    # 4. Wrap systems
    wrapped_layers = [[SystemTask(s) for s in layer] for layer in layers]

    # 5. Executor
    executor = DeterministicParallelExecutor(max_workers=4)

    # 6. Scheduler
    scheduler = ECSScheduler(executor, wrapped_layers)

    # 7. Runtime
    engine = EngineRuntime(world, scheduler, rollback)

    # 8. Run frames
    for i in range(10):
        engine.tick(inputs={})
        print(f"Frame {world.frame} complete")

    # 9. Rollback
    rollback = RollbackEngine(executor, scheduler, input_log, snapshots)


if __name__ == "__main__":
    main()
    input_log = InputLog()
    snapshots = SnapshotBuffer(size=60)
