"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-GRA-001`             | The Sovereign ID. |
| **Official Name**   | `graph.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: DAG Integrity (Law 04)**
> Implemented from Blueprint `GVRN.REG.TaskGraph.md`.
> Ethos: Stability through structural validation.
"""

from typing import List, Set, Dict, Any
from .task import Task


class TaskGraph:
    """
    Manages a collection of tasks as a Directed Acyclic Graph (DAG).
    Ensures architectural integrity via cycle detection and dependency validation.
    
    The TaskGraph is responsible for defining the execution order and
    organizing tasks into layers for optimal deterministic scheduling.
    """

    def __init__(self) -> None:
        """Initializes an empty task graph."""
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """
        Registers a new task in the graph.
        
        Args:
            task (Task): The task instance to add.
        """
        self.tasks.append(task)

    def reset(self) -> None:
        """Resets the state of all tasks in the graph for a new execution cycle."""
        for task in self.tasks:
            task.reset()

    def validate(self) -> None:
        """
        Performs a depth-first search (DFS) to detect cycles in the dependency graph.
        Ensures the engine does not enter a deadlock or infinite loop state.
        
        Raises:
            RuntimeError: If a circular dependency is detected.
        """
        visited: Set[Task] = set()
        path: Set[Task] = set()

        def check_cycle(task: Task) -> None:
            """
            Recursive DFS helper for detecting circular dependencies.
            
            Args:
                task (Task): The current task being explored.
            """
            if task in path:
                raise RuntimeError(f"Cycle detected in TaskGraph: {task.name} is part of a dependency loop.")
            if task in visited:
                return

            path.add(task)
            for dep in task.dependencies:
                check_cycle(dep)
            path.remove(task)
            visited.add(task)

        for task in self.tasks:
            check_cycle(task)
            
    def get_layers(self) -> List[List[Task]]:
        """
        Organizes tasks into discrete layers based on dependency hierarchy.
        Used primarily by parallel and layered schedulers.
        
        Layer 0 contains tasks with no dependencies. 
        Subsequent layers contain tasks whose dependencies are satisfied by previous layers.
        
        Returns:
            List[List[Task]]: A list of layers, each containing a list of tasks.
            
        Raises:
            RuntimeError: If unresolved dependencies remain after sorting (indicates cycle).
        """
        layers: List[List[Task]] = []
        # Mapping of task to number of dependencies remaining to be satisfied
        in_degree: Dict[Task, int] = {t: len(t.dependencies) for t in self.tasks}
        # Mapping of dependency to tasks that depend on it
        dependents: Dict[Task, List[Task]] = {t: [] for t in self.tasks}
        
        for t in self.tasks:
            for dep in t.dependencies:
                dependents[dep].append(t)

        # Start with tasks that have zero dependencies
        current_layer: List[Task] = [t for t in self.tasks if in_degree[t] == 0]

        while current_layer:
            # Sort current layer by name to maintain lexicographical determinism
            current_layer.sort(key=lambda t: t.name)
            layers.append(current_layer)
            
            next_layer: List[Task] = []
            for task in current_layer:
                for dep in dependents[task]:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        next_layer.append(dep)
            current_layer = next_layer

        if sum(len(layer) for layer in layers) < len(self.tasks):
            raise RuntimeError("Unresolved dependencies found. Structural integrity compromised (Cycle?).")

        return layers

    def __repr__(self) -> str:
        """Returns a string representation of the graph nodes count."""
        return f"<TaskGraph nodes={len(self.tasks)}>"
