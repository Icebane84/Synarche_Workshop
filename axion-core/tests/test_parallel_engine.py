import sys
import os
import time

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.deterministic import DeterministicEngine, Task

def test_parallel_execution():
    """
    Validates that the ParallelScheduler correctly identifies independent tasks
    and executes them concurrently while respecting DAG barriers.
    """
    print("--- [START] PARALLEL EXECUTION VALIDATION ---")
    
    # Initialize engine in Parallel mode
    engine = DeterministicEngine(use_parallel=True)
    engine.state['results'] = []

    # System A and B are independent (Layer 0)
    # They both take 0.1s. In serial, this takes 0.2s. In parallel, it takes ~0.1s.
    def system_a(ctx):
        time.sleep(0.1)
        ctx['state']['results'].append("A")

    def system_b(ctx):
        time.sleep(0.1)
        ctx['state']['results'].append("B")

    # System C depends on both A and B (Layer 1)
    def system_c(ctx):
        ctx['state']['results'].append("C")

    # Build the DAG
    task_a = Task("System_A", system_a)
    task_b = Task("System_B", system_b)
    task_c = Task("System_C", system_c, dependencies=[task_a, task_b])

    engine.register_task(task_a)
    engine.register_task(task_b)
    engine.register_task(task_c)
    engine.initialize()

    print("\nExecuting Frame 1 (Parallel)...")
    start_time = time.perf_counter()
    engine.run(frames=1)
    end_time = time.perf_counter()
    
    total_duration = end_time - start_time
    print(f"Total Execution Time: {total_duration:.4f}s")
    print(f"Final State Order: {engine.state['results']}")
    print(f"\nExecution Summary:\n{engine.scheduler.get_summary()}")

    # ASSERTIONS
    # 1. Parallel Speedup: Total time should be significantly less than 0.2s
    assert total_duration < 0.15, f"Parallel execution too slow: {total_duration:.4f}s. Expected < 0.15s."
    
    # 2. Dependency Integrity: C must ALWAYS be executed after A and B
    assert engine.state['results'][-1] == "C", "Dependency Violation: C executed before dependencies finished."
    
    # 3. Completeness: All tasks must be present
    assert set(engine.state['results']) == {"A", "B", "C"}

    print("\n--- [SUCCESS] Parallel Deterministic Execution verified. ---")

if __name__ == "__main__":
    try:
        test_parallel_execution()
    except Exception as e:
        print(f"\n[FAILURE] Parallel Validation Failed: {e}")
        sys.exit(1)
