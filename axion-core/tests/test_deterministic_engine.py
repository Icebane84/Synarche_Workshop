import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.deterministic import DeterministicEngine, Task

def test_engine():
    engine = DeterministicEngine()
    engine.state['counter'] = 0

    def load_task(ctx):
        ctx["state"]["counter"] += 1

    def process_task(ctx):
        ctx["state"]["counter"] *= 2

    # Build the DAG
    # Note: Using 'dependencies' to match our implementation's parameter name
    A = Task("Load", load_task)
    B = Task("Process", process_task, dependencies=[A])

    engine.register_task(A)
    engine.register_task(B)
    engine.initialize()

    print("--- Frame 0 -> 1 ---")
    # Frame 0: Initial 0 -> Step 1 (Exec A then B) -> 2
    engine.run(frames=1)
    print(f"Frame {engine.executor.clock.frame} State: {engine.state}")
    assert engine.state['counter'] == 2

    print("\n--- Frame 1 -> 2 ---")
    # Frame 1: 2 -> Step 2 (Exec A then B) -> 6
    engine.run(frames=1)
    print(f"Frame {engine.executor.clock.frame} State: {engine.state}")
    assert engine.state['counter'] == 6

    print("\n--- Rollback ---")
    # Rollback by 1 step (to Frame 1)
    # Our engine's frame logic: step() saves state BEFORE execution.
    # So Frame 1 snapshot = state 2. Frame 2 snapshot = state 6.
    # When we rollback 1 step from Frame 2, we return to Frame 1.
    print("Rolling back by 1 step...")
    engine.rollback(steps=1)
    print(f"Restored Frame {engine.executor.clock.frame} State: {engine.state}")
    assert engine.state['counter'] == 2
    print("Rollback successful.")

if __name__ == "__main__":
    try:
        test_engine()
        print("\n[SUCCESS] Deterministic Engine Refinement validated.")
    except Exception as e:
        print(f"\n[FAILURE] Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
