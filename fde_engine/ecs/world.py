"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-WORLD` | The Sovereign ID. |
| **Official Name** | `world.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `ECS`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/ecs/world.py`

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

from fde_engine.ecs.archetype_storage import Archetype
from fde_engine.ecs.entity_registry import EntityRegistry


class World:
    def __init__(self):
        self.registry = EntityRegistry()
        self.registry._archetypes = {}
        self.registry._entity_index = {}

        self.frame = 0
        self.current_inputs = {}

    def snapshot(self):
        # Gathers shallow copies from all registries
        return {
            "registry_id": self.registry.snapshot(),
            "archetypes": {sig: arch.snapshot() for sig, arch in self.registry._archetypes.items()},
            "entity_index": self.registry._entity_index.copy(),
            "frame": self.frame,
            "inputs": self.current_inputs.copy(),
        }

    def restore(self, snap):
        # Instantly snaps memory pointers back to the historical state
        self.registry.restore(snap["registry_id"])
        self.frame = snap["frame"]
        self.current_inputs = snap["inputs"].copy()

        self.registry._entity_index = snap["entity_index"].copy()
        for sig, arch_snap in snap["archetypes"].items():
            arch = self.registry._archetypes[sig]
            arch.entity_ids = arch_snap["entity_ids"].copy()
            arch.columns = {ctype: col.copy() for ctype, col in arch_snap["columns"].items()}
