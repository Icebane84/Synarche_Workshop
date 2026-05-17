"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-COMMAND_BUFFER` | The Sovereign ID. |
| **Official Name** | `command_buffer.py`           | The Filename.     |
| **Version** | **v15.0 [OMEGA]** | The Standard.     |
| **Domain** | `ECS`                         | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/ecs/command_buffer.py`

**Ethos:** Intent is Deferred; Execution is Absolute.
"""

from dataclasses import dataclass
from typing import Any, Optional, Type


@dataclass(frozen=True)
class Command:
    """Immutable intent packet generated safely by parallel threads."""

    execution_index: int
    action: str  # "SPAWN", "DESTROY", "SET"
    entity_id: int
    component_type: Optional[Type]
    payload: Any


class CommandBuffer:
    """Thread-local storage for deferred system intents."""

    def __init__(self, execution_index: int):
        self.execution_index = execution_index
        self.commands = []

    def add(self, action: str, entity_id: int, component_type: Optional[Type], payload: Any) -> None:
        """Records a deterministic command to be executed during the single-threaded commit phase."""
        self.commands.append(Command(self.execution_index, action, entity_id, component_type, payload))

    def clear(self) -> None:
        self.commands.clear()
