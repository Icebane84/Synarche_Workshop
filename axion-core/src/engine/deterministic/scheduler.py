"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-SCH-001`             | The Sovereign ID. |
| **Official Name**   | `scheduler.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Deterministic Ordering (Law 15)**
> Implemented from Blueprint `GVRN.REG.DeterministicScheduler.md`.
> Ethos: Predictability through strict sequencing.
"""

from typing import Set, Dict, Any, List
from .graph import TaskGraph
from .task import Task


class DeterministicScheduler:
    """
    Executes a TaskGraph in a strictly deterministic order.
    Ensures that for any given state and graph, the execution sequence 
    is identical across all platforms and runs.
    """

    def __init__(self, graph: TaskGraph) -> None:
        """
        Initializes the scheduler with a target task graph.
        
        Args:
            graph (TaskGraph): The DAG of tasks to be scheduled.
        """
        self.graph = graph
        self.execution_log: List[str] = []

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Executes the tasks in the graph until all are completed.
        Enforces lexicographical sorting of ready tasks to guarantee determinism.
        
        Args:
            context (Dict[str, Any]): The execution context shared across all tasks.
            
        Raises:
            RuntimeError: If execution enters a deadlock state (unresolved dependencies).
        """
        self.execution_log = []
        remaining: Set[Task] = set(self.graph.tasks)

        while remaining:
            progress: bool = False
            
            # Deterministic sorting (by name) is the key to reproducible behavior.
            ready_tasks = sorted(
                [t for t in remaining if t.is_ready()],
                key=lambda t: t.name
            )

            for task in ready_tasks:
                self.execution_log.append(f"EXEC: {task.name}")
                task.run(context)
                remaining.remove(task)
                progress = True

            if not progress and remaining:
                # Safety net for runtime dependency failures.
                raise RuntimeError("Execution Deadlock: Unresolved dependencies or cycles in graph.")

    def get_summary(self) -> str:
        """
        Retrieves a summary string of the last execution sequence.
        
        Returns:
            str: A newline-delimited log of executed tasks.
        """
        return "\n".join(self.execution_log)
