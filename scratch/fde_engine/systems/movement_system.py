"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-SYSTEMS-MOVEMENT_SYSTEM` | The Sovereign ID. |
| **Official Name** | `movement_system.py`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `SYSTEMS`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

# systems/movement_system.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: float
    y: float


@dataclass(frozen=True)
class Velocity:
    dx: float
    dy: float


class MovementSystem:
    execution_index = 10

    def query(self, world):
        return [
            arch
            for sig, arch in world.registry._archetypes.items()
            if Position in sig and Velocity in sig
        ]

    def compute_chunk(self, world, chunk):
        delta = {"mutations": {Position: {}}}

        pos = chunk.archetype.columns[Position]
        vel = chunk.archetype.columns[Velocity]
        eids = chunk.archetype.entity_ids

        for i in range(chunk.start, chunk.end):
            eid = eids[i]
            p = pos[i]
            v = vel[i]

            delta["mutations"][Position][eid] = Position(p.x + v.dx, p.y + v.dy)

        return delta
