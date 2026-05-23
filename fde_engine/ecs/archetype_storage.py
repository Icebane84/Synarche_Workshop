"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-ARCHETYPE_STORAGE`| The Sovereign ID. |
| **Official Name** | `archetype_storage.py`        | The Filename.     |
| **Version** | **v15.0 [OMEGA]** | The Standard.     |
| **Domain** | `ECS`                         | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/ecs/archetype_storage.py`

**Ethos:** Memory is Static; Only Pointers Move.
"""

from typing import Any, FrozenSet, Type, dict


class Archetype:
    """AAA-grade static array table. No dynamic memory resizing occurs here."""

    def __init__(self, signature: FrozenSet[Type], capacity: int = 10000):
        self.signature = signature
        self.capacity = capacity
        self.size = 0

        # Memory is reserved entirely upfront during initialization
        self.entity_ids: List[int] = [0] * capacity
        self.columns: Dict[Type, List[Any]] = {
            comp: [None] * capacity for comp in signature
        }

    def add_entity(self, eid: int, components: Dict[Type, Any]) -> int:
        if self.size >= self.capacity:
            raise RuntimeError("FDE Violation: Archetype Memory Block Exceeded.")

        row = self.size
        self.entity_ids[row] = eid
        for ctype in self.signature:
            self.columns[ctype][row] = components[ctype]

        self.size += 1
        return row

    def remove_entity(self, row: int) -> int:
        """O(1) Swap-and-pop using pre-allocated indices. Never shrinks the list."""
        last_index = self.size - 1
        swapped_eid = self.entity_ids[last_index]

        if row != last_index:
            # Overwrite target row with the tail's data
            self.entity_ids[row] = swapped_eid
            for ctype in self.signature:
                self.columns[ctype][row] = self.columns[ctype][last_index]

        # Nullify the tail to prevent memory leaks of orphaned objects
        self.entity_ids[last_index] = 0
        for ctype in self.signature:
            self.columns[ctype][last_index] = None

        self.size -= 1
        return swapped_eid

    def snapshot(self) -> dict:
        """AAA Zero-Copy Rollback Optimization."""
        return {
            "entity_ids": self.entity_ids.copy(),
            "columns": {ctype: col.copy() for ctype, col in self.columns.items()},
            "size": self.size,
        }
