"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-PSCH-001`            | The Sovereign ID. |
| **Official Name**   | `parallel_scheduler.py`       | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Concurrent Synthesis (Law 18)**
> Implemented from Blueprint `GVRN.REG.ParallelScheduler.md`.
> Ethos: Throughput through structural parallelism.
"""

import concurrent.futures
from typing import Any, Dict, List, Optional

from .graph import TaskGraph


class ParallelScheduler:
    """Executes a TaskGraph using multi-core parallelism while maintaining determinism.

    Architecture:
    1. Tasks are grouped into 'layers' (sets of tasks with no mutual dependencies).
    2. All tasks within a single layer are executed concurrently in a thread pool.
    3. The scheduler waits for a layer to finish entirely before starting the next one.

    This 'Layered Barrier' approach ensures bit-perfect determinism while
    dramatically increasing throughput for independent systems.
    """

    def __init__(self, graph: TaskGraph, max_workers: Optional[int] = None) -> None:
        """Initializes the parallel scheduler.

        Args:
            graph (TaskGraph): The DAG of tasks to execute.
            max_workers (Optional[int]): Maximum number of threads to spawn.
                                         Defaults to machine processor count.

        """
        self.graph = graph
        self.max_workers = max_workers
        self.execution_log: List[str] = []

    def execute(self, context: Dict[str, Any]) -> None:
        """Processes the task graph layer-by-layer across multiple threads.
        Ensures all tasks in a layer are completed before progressing to the next layer.

        Args:
            context (Dict[str, Any]): The execution context shared across all tasks.

        Raises:
            RuntimeError: If a task execution fails or enters an invalid state.

        """
        self.execution_log = []
        layers = self.graph.get_layers()

        # We use ThreadPoolExecutor for lightweight context switching.
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            for i, layer in enumerate(layers):
                self.execution_log.append(f"--- LAYER {i} (CONCURRENT) ---")

                # Step A: Dispatch all tasks in the current layer
                futures = {executor.submit(task.run, context): task for task in layer}

                # Step B: Wait for the 'Layer Barrier'
                # We collect results as they finish, but we don't proceed to the
                # next layer until ALL tasks here are completed.
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        # result() will re-raise any exception occurred during task execution
                        future.result()
                        self.execution_log.append(f"COMPLETED: {task.name}")
                    except Exception as e:
                        # Wrap the error for engine-level awareness
                        raise RuntimeError(
                            f"Parallel Execution Failure in '{task.name}': {e}"
                        ) from e

    def get_summary(self) -> str:
        """Retrieves a summary of the parallel execution flow.

        Returns:
            str: A newline-delimited log of layer transitions and task completions.

        """
        return "\n".join(self.execution_log)
