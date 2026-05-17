"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-COM-001`             | The Sovereign ID. |
| **Official Name**   | `compiler.py`                 | The Filename.     |
| **Version**         | **v15.1 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Semantic Synthesis (Law 14)**
> Implemented from Blueprint `CORE-FDE-DAG-009`.
> Ethos: Data dictates the flow.
"""

from typing import List, Any
from ..scheduling.compiled_graph import CompiledGraph

class ECSSystemTask:
    """
    Adapter that wraps an ECS System for the CompiledGraph.
    """
    def __init__(self, system_instance: Any) -> None:
        self.system = system_instance
        self.name = system_instance.name
        self.execution_index = system_instance.execution_index
        self.deps: List[str] = [] # To be populated by compiler

    def compute_pure(self, context: Any) -> Any:
        """Proxies execution to the system. Returns a delta packet."""
        if hasattr(self.system, "compute"):
            world = context.get("world")
            return self.system.compute(world, None)
        return {}

    def run(self, context: Any) -> None:
        """Sequential execution fallback."""
        self.compute_pure(context)

class ECSSystemCompiler:
    """
    Analyzes ECS Systems and compiles them into a dependency-aware CompiledGraph.
    """
    def __init__(self, systems: List[Any]) -> None:
        self.systems = [ECSSystemTask(s) for s in systems]

    def compile(self) -> CompiledGraph:
        """
        Calculates dependencies based on read/write signatures and returns a graph.
        """
        for a in self.systems:
            for b in self.systems:
                if a == b:
                    continue
                
                if self._depends(a.system, b.system):
                    # B depends on A (A must run before B)
                    if a.name not in b.deps:
                        b.deps.append(a.name)

        return CompiledGraph(self.systems)

    def _depends(self, a: Any, b: Any) -> bool:
        """
        Determines if System A must execute before System B.
        Logic derived from CORE-FDE-DAG-009.
        """
        # Temporal Directive: Edges can ONLY flow forward in time.
        if a.execution_index >= b.execution_index:
            return False

        # Semantic Data Overlaps
        write_read = a.writes & b.reads
        read_write = a.reads & b.writes
        write_write = a.writes & b.writes
        
        # Accumulate interactions
        write_accum = a.writes & b.accumulates
        accum_write = a.accumulates & b.writes
        read_accum = a.reads & b.accumulates
        accum_read = a.accumulates & b.reads

        return bool(
            write_read or read_write or write_write or 
            write_accum or accum_write or 
            read_accum or accum_read
        )
