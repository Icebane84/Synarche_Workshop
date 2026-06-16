"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-ARCHETYPE_STORAGE` | The Sovereign ID. |
| **Official Name** | `archetype_storage.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `ECS`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

# ecs/archetype_storage.py


class Archetype:
    def __init__(self, signature):
        self.signature = signature
        self.entity_ids = []
        self.columns = {ctype: [] for ctype in signature}

    def add_entity(self, eid, components):
        self.entity_ids.append(eid)

        for ctype in self.signature:
            self.columns[ctype].append(components[ctype])

        return len(self.entity_ids) - 1

    def remove_entity(self, row):
        last = len(self.entity_ids) - 1
        swapped_eid = self.entity_ids[last]

        if row != last:
            self.entity_ids[row] = swapped_eid
            for ctype in self.signature:
                self.columns[ctype][row] = self.columns[ctype][last]

        self.entity_ids.pop()
        for ctype in self.signature:
            self.columns[ctype].pop()

        return swapped_eid

    def snapshot(self):
        return {
            "entity_ids": self.entity_ids.copy(),
            "columns": {k: v.copy() for k, v in self.columns.items()},
        }
