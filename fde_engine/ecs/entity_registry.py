"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-ENTITY_REGISTRY`| The Sovereign ID. |
| **Official Name** | `entity_registry.py`          | The Filename.     |
| **Version** | **v15.0 [OMEGA]** | The Standard.     |
| **Domain** | `ECS`                         | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/ecs/entity_registry.py`

**Ethos:** Identity is Pre-Allocated; Growth is Static.
"""


class EntityRegistry:
    """Zero-allocation pool manager for entity IDs and Archetype routing."""

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        # Stored in reverse so pop() operates in O(1) time without shifting arrays
        self.free = list(range(capacity, 0, -1))
        self.alive = set()

        self._archetypes = {}  # signature -> Archetype object
        self._entity_index = {}  # eid -> (signature, row_index)

    def create(self) -> int:
        if not self.free:
            raise RuntimeError("FDE Violation: Entity Pool Capacity Exhausted.")
        eid = self.free.pop()
        self.alive.add(eid)
        return eid

    def release(self, eid: int) -> None:
        if eid in self.alive:
            self.alive.remove(eid)
            self.free.append(eid)
            self._entity_index.pop(eid, None)

    def snapshot(self) -> dict:
        """Lightweight pointer copy for rollback anchoring."""
        return {"free": self.free.copy(), "alive": self.alive.copy()}

    def restore(self, snap: dict) -> None:
        self.free = snap["free"].copy()
        self.alive = snap["alive"].copy()
