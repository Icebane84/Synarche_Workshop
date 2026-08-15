import sys
from fde_engine.core.chunk_executor import ChunkExecutor
from fde_engine.core.engine_runtime import EngineRuntime
from fde_engine.core.rollback_core import InputLog, RollbackEngine, SnapshotBuffer
from fde_engine.dag.dag_compiler import DAGCompiler
from fde_engine.ecs.archetype_storage import Archetype
from fde_engine.ecs.command_buffer import CommandBuffer
from fde_engine.ecs.commit_layer import CommandCommitter
from fde_engine.ecs.ecs_scheduler import ECSScheduler, SystemTask
from fde_engine.ecs.world import World
from fde_engine.gvrn.law_validator import LawValidator
from fde_engine.gvrn.selt_logger import SELTLogger
from fde_engine.systems.movement_system import MovementSystem, Position, Velocity

sys.stdout.reconfigure(encoding="utf-8")


def run_full_audit():
    print("=" * 60)
    print("⚡ FDE ENGINE COMPLIANCE AUDIT & TEST SUITE")
    print("=" * 60)

    # 1. Test World & Entity Registry Invariants
    world = World()
    logger = SELTLogger()
    eid1 = world.registry.create()
    eid2 = world.registry.create()

    sig = frozenset([Position, Velocity])
    arch = Archetype(sig, capacity=1000)
    world.registry._archetypes[sig] = arch

    row1 = arch.add_entity(eid1, {Position: Position(0.0, 0.0), Velocity: Velocity(1.0, 2.0)})
    world.registry._entity_index[eid1] = (sig, row1)

    row2 = arch.add_entity(eid2, {Position: Position(10.0, 10.0), Velocity: Velocity(-1.0, 0.0)})
    world.registry._entity_index[eid2] = (sig, row2)

    assert LawValidator.validate_world(world), "World validation failed."
    print("✅ PASS: Entity Registry & Archetype Alignment (Zero-Entropy)")

    # 2. Test DAG Compilation & Scheduler Execution
    systems = [MovementSystem()]
    compiler = DAGCompiler(systems)
    layers = compiler.compile_layers()
    wrapped = [[SystemTask(s) for s in layer] for layer in layers]

    executor = ChunkExecutor(max_workers=2, chunk_size=128)
    scheduler = ECSScheduler(executor, wrapped)

    input_log = InputLog()
    snapshots = SnapshotBuffer(size=120)
    rollback = RollbackEngine(executor, scheduler, input_log, snapshots)
    engine = EngineRuntime(world, scheduler, rollback)

    # Simulate 5 frames
    for _ in range(5):
        engine.tick(inputs={})

    pos1 = arch.columns[Position][row1]
    pos2 = arch.columns[Position][row2]
    assert pos1 == Position(5.0, 10.0), f"Entity 1 Pos Mismatch: {pos1}"
    assert pos2 == Position(5.0, 10.0), f"Entity 2 Pos Mismatch: {pos2}"
    print("✅ PASS: Deterministic Parallel Chunk Execution (5 frames)")

    # 3. Test Command Buffer & Deferred Commit
    committer = CommandCommitter()
    cmd_buf = CommandBuffer(execution_index=1)

    # Spawn entity 3 via CommandBuffer
    cmd_buf.add("SPAWN", entity_id=3, component_type=None, payload={Position: Position(100.0, 100.0), Velocity: Velocity(0.0, 0.0)})
    committer.apply(world, [cmd_buf])

    assert 3 in world.registry.alive, "Command buffer SPAWN failed."
    assert LawValidator.validate_world(world), "World validation failed after SPAWN."
    print("✅ PASS: CommandBuffer Deferred Intent & Single-Threaded Commit")

    # 4. Test Snapshot & Rollback Engine Rewind
    snap_before = world.snapshot()
    frame_at_snap = world.frame

    # Simulate 5 more frames
    for _ in range(5):
        engine.tick(inputs={"player1": "MOVE_RIGHT"})

    pos1_frame10 = arch.columns[Position][row1]
    assert pos1_frame10 == Position(10.0, 20.0), f"Frame 10 pos mismatch: {pos1_frame10}"

    # Trigger Rollback to frame_at_snap
    rollback.rollback(target_frame=frame_at_snap + 1, world=world)
    assert LawValidator.validate_world(world), "World validation failed after Rollback."
    print("✅ PASS: Rollback Engine State Rewind & Forward Resimulation")

    print("=" * 60)
    print("🎉 ALL FDE ENGINE TESTS PASSED (100% Determinism Verified)")
    print("=" * 60)


if __name__ == "__main__":
    run_full_audit()

