"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-SCH-LAY-001`             | The Sovereign ID. |
| **Official Name**   | `layered_scheduler.py`        | The Filename.     |
| **Version**         | **v15.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-SCH`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Layered Progression (Law 13)**
> Implemented from Blueprint `UMB-QB-PHX-001`.
> Ethos: Progress is a staircase, not a slope.
"""

from typing import Dict, Any, Optional, List
from .compiled_graph import CompiledGraph

class LayeredScheduler:
    """
    Executes a CompiledGraph layer-by-layer.
    Supports both sequential and parallel execution (if an executor is provided).
    """
    def __init__(self, graph: Optional[CompiledGraph], executor: Optional[Any] = None) -> None:
        self.graph = graph
        self.executor = executor

    def execute(self, context: Dict[str, Any]) -> None:
        """
        Sequentially executes each layer of the compiled graph.
        Tasks within a layer are executed in parallel if self.executor exists.
        
        Args:
            context (Dict[str, Any]): The execution context shared across all tasks.
        """
        if self.graph is None:
            raise ValueError("FDE Violation: No graph provided to LayeredScheduler.")

        for i, layer in enumerate(self.graph.layers):
            if self.executor:
                # Parallel Execution within layer
                if hasattr(self.executor, "execute_layer"):
                     self.executor.execute_layer(layer, context)
                elif hasattr(self.executor, "execute"):
                     self.executor.execute(layer, context)
                else:
                    # Fallback to sequential if executor interface is unknown
                    for task in layer:
                        task.run(context)
            else:
                # Sequential Execution
                for task in layer:
                    task.run(context)
