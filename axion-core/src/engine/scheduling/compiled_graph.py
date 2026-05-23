"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-SCH-GRA-001`             | The Sovereign ID. |
| **Official Name**   | `compiled_graph.py`           | The Filename.     |
| **Version**         | **v15.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-SCH`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Structural Determinism (Law 12)**
> Implemented from Blueprint `UMB-QB-PHX-001`.
> Ethos: Order is the antidote to chaos.
"""

from typing import Any, Dict, List, Set


class CompiledGraph:
    """Translates a flat list of interdependent tasks into a deterministic layered DAG."""

    def __init__(self, tasks: List[Any]) -> None:
        self.tasks = tasks
        self.layers: List[List[Any]] = []

    def build(self) -> None:
        """Builds the execution layers using Kahn's algorithm variant.
        Enforces lexicographical sorting within layers for absolute determinism.
        """
        if not self.tasks:
            self.layers = []
            return

        # 1. Map task names to objects for dependency resolution
        task_map = {t.name: t for t in self.tasks}

        # 2. Build adjacency list and calculate in-degrees
        graph: Dict[str, Set[str]] = {t.name: set() for t in self.tasks}
        in_degree: Dict[str, int] = {t.name: 0 for t in self.tasks}

        for task in self.tasks:
            for dep_name in task.deps:
                if dep_name not in task_map:
                    # In this system, missing dependencies are considered terminal errors
                    raise RuntimeError(
                        f"FDE Violation: Task '{task.name}' depends on unknown task '{dep_name}'."
                    )

                graph[dep_name].add(task.name)
                in_degree[task.name] += 1

        # 3. Layering process
        remaining_names = set(task_map.keys())
        resolved_layers = []

        while remaining_names:
            # Find tasks with zero in-degree
            ready = [name for name in remaining_names if in_degree[name] == 0]

            if not ready:
                raise RuntimeError(
                    "FDE Violation: Cycle detected in CompiledGraph. Temporal collapse imminent."
                )

            # Enforce determinism: sort alphabetically
            ready.sort()

            # Map back to objects
            layer_tasks = [task_map[name] for name in ready]
            resolved_layers.append(layer_tasks)

            # Update dependencies
            for name in ready:
                remaining_names.remove(name)
                for neighbor in graph[name]:
                    in_degree[neighbor] -= 1

        self.layers = resolved_layers
