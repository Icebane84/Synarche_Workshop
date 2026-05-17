"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-ECS-COMMIT_LAYER`   | The Sovereign ID. |
| **Official Name** | `commit_layer.py`             | The Filename.     |
| **Version** | **v15.0 [OMEGA]** | The Standard.     |
| **Domain** | `ECS`                         | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Location:** `fde_engine/ecs/commit_layer.py`

**Ethos:** The Single-Threaded Bottleneck of Truth.
"""

from typing import List

from fde_engine.ecs.archetype_storage import Archetype
from fde_engine.ecs.command_buffer import Command, CommandBuffer


class CommandCommitter:
    """Applies deferred intent packets deterministically to pre-allocated memory."""

    def apply(self, world, command_buffers: List[CommandBuffer]) -> None:
        commands = []
        for buf in command_buffers:
            commands.extend(buf.commands)

        # 1. Deterministic Multi-Key Sort
        # Primary Key: Entity ID (Groups entity changes together)
        # Secondary Key: Execution Index (Preserves system order if multiple hit the same entity)
        commands.sort(key=lambda c: (c.entity_id, c.execution_index))

        # 2. Sequential Execution (Zero Race Conditions)
        for cmd in commands:
            self._execute(world, cmd)

    def _execute(self, world, cmd: Command) -> None:
        reg = world.registry

        if cmd.action == "SET":
            if cmd.entity_id not in reg._entity_index:
                return  # Entity may have been destroyed earlier in this commit phase

            sig, row = reg._entity_index[cmd.entity_id]
            reg._archetypes[sig].columns[cmd.component_type][row] = cmd.payload

        elif cmd.action == "SPAWN":
            # cmd.payload is a dictionary of frozen component instances
            eid = reg.create()
            sig = frozenset(cmd.payload.keys())

            if sig not in reg._archetypes:
                reg._archetypes[sig] = Archetype(sig)

            row = reg._archetypes[sig].add_entity(eid, cmd.payload)
            reg._entity_index[eid] = (sig, row)

        elif cmd.action == "DESTROY":
            if cmd.entity_id not in reg._entity_index:
                return

            sig, row = reg._entity_index[cmd.entity_id]
            arch = reg._archetypes[sig]

            swapped_eid = arch.remove_entity(row)
            if swapped_eid != cmd.entity_id:
                # Update the index of the entity that was swapped to fill the hole
                reg._entity_index[swapped_eid] = (sig, row)

            reg.release(cmd.entity_id)
