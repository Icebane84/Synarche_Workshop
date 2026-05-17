"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-SYSTEMS-BASE_SYSTEM` | The Sovereign ID. |
| **Official Name** | `base_system.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `SYSTEMS`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/systems/base_system.py`

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""


class BaseSystem:
    name = "base"
    execution_index = 0

    reads = set()
    writes = set()
    accumulates = set()

    def query(self, world):
        raise NotImplementedError

    def compute_chunk(self, world, chunk):
        """
        MUST return deterministic delta packet
        """
        return {"mutations": {}, "structural_migrations": {}}
