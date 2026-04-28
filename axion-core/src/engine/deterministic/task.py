"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-TSK-001`             | The Sovereign ID. |
| **Official Name**   | `task.py`                     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[COMET]`                     | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Atomic Execution (Law 06)**
> Implemented from Blueprint `GVRN.REG.DeterministicTask.md`.
> Ethos: Authority through semantic isolation.
"""

from typing import Callable, List, Optional, Any, Dict
import uuid
from ..ecs.resonance import ResonanceDomain


class Task:
    """
    A discrete, deterministic unit of work within the Coherent Verse Engine.
    Includes a ResonanceDomain to define its semantic authority during execution.
    
    Tasks are the building blocks of the simulation, linked together in a DAG
    and executed by the DeterministicEngine.
    """

    def __init__(
        self, 
        name: str, 
        action: Callable[..., Any], 
        dependencies: Optional[List['Task']] = None,
        metadata: Optional[Dict[str, Any]] = None,
        domain: ResonanceDomain = ResonanceDomain.CORE
    ) -> None:
        """
        Initializes a task with its action and dependencies.
        
        Args:
            name (str): Human-readable name for the task.
            action (Callable): The function to execute.
            dependencies (Optional[List[Task]]): Tasks that must complete before this one starts.
            metadata (Optional[Dict[str, Any]]): Arbitrary configuration data.
            domain (ResonanceDomain): The security domain this task operates within.
        """
        self.id: uuid.UUID = uuid.uuid4()
        self.name: str = name
        self.action: Callable[..., Any] = action
        self.dependencies: List['Task'] = dependencies or []
        self.metadata: Dict[str, Any] = metadata or {}
        self.domain: ResonanceDomain = domain
        self.completed: bool = False
        self.result: Any = None

    def is_ready(self) -> bool:
        """
        Checks if all prerequisite tasks have completed successfully.
        
        Returns:
            bool: True if all dependencies are done.
        """
        return all(dep.completed for dep in self.dependencies)

    def run(self, context: Dict[str, Any]) -> Any:
        """
        Executes the task's action and marks it as completed.
        Automatically establishes semantic context for ECS interactions.
        
        Args:
            context (Dict[str, Any]): The execution context containing simulation state.
            
        Returns:
            Any: The result returned by the task's action.
        """
        # Establish Semantic Context: Set current system and domain for the ECS
        components = context.get('state', {}).get('components')
        if components and hasattr(components, 'set_access_context'):
            components.set_access_context(self.name, self.domain)
            
        self.result = self.action(context)
        self.completed = True
        return self.result

    def reset(self) -> None:
        """Resets the task state (completion status and result) for a new execution cycle."""
        self.completed = False
        self.result = None

    def __repr__(self) -> str:
        """Returns a string representation showing task readiness and domain."""
        return f"<Task {self.name} [{self.domain.name}] (ready={self.is_ready()}, done={self.completed})>"
