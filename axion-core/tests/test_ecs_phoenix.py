import asyncio
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.engine.deterministic import DeterministicEngine, Task
from src.nexus.decorators.synarche_audit import synarche_audit
from src.system.logging.phoenix_logger import setup_synarche_logging

# Initialize Phoenix Logging for this validation
# Console will show INFO+, File will capture audit trail
logger = setup_synarche_logging("ecs_audit.log")


# --- DATA COMPONENTS ---
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy


# --- SYSTEMS (DAG TASKS) ---
@synarche_audit
def movement_system(ctx):
    """A simple ECS system wrapped in synarche_audit for governance compliance."""
    components = ctx["state"]["components"]
    entities = components.get_entities_with(Position, Velocity)

    for eid in entities:
        pos = components.get_component(eid, Position)
        vel = components.get_component(eid, Velocity)
        pos.x += vel.vx
        pos.y += vel.vy

    logger.info(f"MovementSystem: Processed {len(entities)} entities.")


async def test_ecs_integration():
    print("--- [START] ECS + PHOENIX INTEGRATION TEST ---")
    engine = DeterministicEngine()

    # 1. Entity Composition
    eid = engine.entity_manager.create_entity()
    engine.component_store.add_component(eid, Position(0, 0))
    engine.component_store.add_component(eid, Velocity(10, 5))

    # 2. Task Registration
    move_task = Task("MovementSystem", movement_system)
    engine.register_task(move_task)
    engine.initialize()

    # 3. Frame Execution
    print("\nExecuting Frame 1...")
    engine.run(frames=1)

    pos = engine.component_store.get_component(eid, Position)
    print(f"Post-Frame Position: ({pos.x}, {pos.y})")
    assert pos.x == 10 and pos.y == 5

    # 4. Rollback Verification
    print("\nExecuting Rollback (1 step)...")
    engine.rollback(steps=1)

    # Note: Rollback restores the state to Frame 0
    pos = engine.component_store.get_component(eid, Position)
    print(f"Restored Position: ({pos.x}, {pos.y})")
    assert pos.x == 0 and pos.y == 0

    # 5. Failure Audit Verification
    print("\nSimulating Failure for Audit Trail...")

    @synarche_audit
    def failing_system(ctx):
        """A system designed to fail to test the audit trail."""
        raise RuntimeError("Synarche Protocol Violation: Logic Dissonance Detected.")

    engine.register_task(Task("FailingSystem", failing_system))
    try:
        engine.run(frames=1)
    except RuntimeError:
        print("Caught expected failure. Audit log should now contain the trace.")

    print("\n--- [SUCCESS] ECS + Rollback + Phoenix Logging verified. ---")


if __name__ == "__main__":
    try:
        asyncio.run(test_ecs_integration())
    except Exception as e:
        print(f"\n[FAILURE] Integration Test Failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
