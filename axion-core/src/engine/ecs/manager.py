"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-MAN-001`             | The Sovereign ID. |
| **Official Name**   | `manager.py`                  | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Entity Persistence (Law 12)**
> Implemented from Blueprint `GVRN.REG.EcsManager.md`.
> Ethos: Continuity through ID.
"""

import uuid
from typing import Set


class EntityManager:
    """
    Manages the lifecycle of entities (IDs) in the ECS.
    Entities are opaque handles (UUIDs) that serve as keys for component sets.
    """

    def __init__(self) -> None:
        """Initializes the entity set."""
        self.entities: Set[uuid.UUID] = set()

    def create_entity(self) -> uuid.UUID:
        """
        Generates a new unique entity ID and registers it.
        
        Returns:
            uuid.UUID: The newly created entity handle.
        """
        entity_id = uuid.uuid4()
        self.entities.add(entity_id)
        return entity_id

    def destroy_entity(self, entity_id: uuid.UUID) -> None:
        """
        Removes an entity from the registry.
        
        Args:
            entity_id (uuid.UUID): The handle of the entity to destroy.
        """
        if entity_id in self.entities:
            self.entities.remove(entity_id)

    def __repr__(self) -> str:
        """Returns a string representation of the manager state."""
        return f"<EntityManager count={len(self.entities)}>"
