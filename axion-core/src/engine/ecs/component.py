"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-STO-001`             | The Sovereign ID. |
| **Official Name**   | `component.py`                | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Component Integrity (Law 14)**
> Implemented from Blueprint `GVRN.REG.EcsComponent.md`.
> Ethos: Truth through Storage.
"""

import threading
import uuid
from typing import Any, Dict, Set, Type, TypeVar, Optional, Tuple

from .resonance import ResonanceAuditor, ResonanceDomain

T = TypeVar("T")


class ComponentStore:
    """
    Stores components associated with entities.
    Includes a ResonanceAuditor to enforce semantic security and domain isolation.
    """

    def __init__(self, auditor: Optional[ResonanceAuditor] = None) -> None:
        """
        Initializes the ComponentStore.
        
        Args:
            auditor (Optional[ResonanceAuditor]): The auditor used for access control.
        """
        # type -> {entity_id -> component_instance}
        self.stores: Dict[Type, Dict[uuid.UUID, Any]] = {}
        self._lock = threading.Lock()
        self.auditor = auditor
        self._current_system: str = "UNKNOWN"
        self._current_domain: ResonanceDomain = ResonanceDomain.CORE

    def set_access_context(self, system_name: str, domain: ResonanceDomain) -> None:
        """
        Sets the security context for the currently executing system.
        
        Args:
            system_name (str): The name of the active system.
            domain (ResonanceDomain): The domain associated with the system.
        """
        self._current_system = system_name
        self._current_domain = domain

    def __getstate__(self) -> Dict[str, Any]:
        """
        Custom serialization logic to exclude threading locks.
        
        Returns:
            Dict[str, Any]: The serializable state of the store.
        """
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        Custom deserialization logic to restore state and recreate locks.
        
        Args:
            state (Dict[str, Any]): The serialized state.
        """
        self.__dict__.update(state)
        self._lock = threading.Lock()

    def add_component(self, entity_id: uuid.UUID, component: Any) -> None:
        """
        Associates a component with an entity. Thread-safe and audited.
        
        Args:
            entity_id (uuid.UUID): The entity handle.
            component (Any): The component instance to add.
            
        Raises:
            RuntimeError: If the current system violates resonance boundaries.
        """
        comp_type = type(component)
        if self.auditor:
            if not self.auditor.validate_access(self._current_system, self._current_domain, comp_type):
                raise RuntimeError(
                    f"RESONANCE VIOLATION: System '{self._current_system}' unauthorized for {comp_type.__name__}"
                )

        with self._lock:
            if comp_type not in self.stores:
                self.stores[comp_type] = {}
            self.stores[comp_type][entity_id] = component

    def get_component(self, entity_id: uuid.UUID, comp_type: Type[T]) -> Optional[T]:
        """
        Retrieves a component instance for a given entity and type.
        
        Args:
            entity_id (uuid.UUID): The entity handle.
            comp_type (Type[T]): The class of the component to retrieve.
            
        Returns:
            Optional[T]: The component instance, or None if not found.
            
        Raises:
            RuntimeError: If the current system violates resonance boundaries.
        """
        if self.auditor:
            if not self.auditor.validate_access(self._current_system, self._current_domain, comp_type):
                raise RuntimeError(
                    f"RESONANCE VIOLATION: System '{self._current_system}' unauthorized for {comp_type.__name__}"
                )
        return self.stores.get(comp_type, {}).get(entity_id)

    def remove_component(self, entity_id: uuid.UUID, comp_type: Type) -> None:
        """
        Disassociates a component type from an entity. Thread-safe and audited.
        
        Args:
            entity_id (uuid.UUID): The entity handle.
            comp_type (Type): The class of the component to remove.
            
        Raises:
            RuntimeError: If the current system violates resonance boundaries.
        """
        if self.auditor:
            if not self.auditor.validate_access(self._current_system, self._current_domain, comp_type):
                raise RuntimeError(
                    f"RESONANCE VIOLATION: System '{self._current_system}' unauthorized for {comp_type.__name__}"
                )

        with self._lock:
            if comp_type in self.stores:
                self.stores[comp_type].pop(entity_id, None)

    def get_entities_with(self, *comp_types: Type) -> Set[uuid.UUID]:
        """
        Returns a set of entity IDs that possess ALL specified component types.
        Used for system queries and filtered processing loops.
        
        Args:
            *comp_types (Type): Variable number of component types to filter by.
            
        Returns:
            Set[uuid.UUID]: A set of entity IDs matching all types.
        """
        if not comp_types:
            return set()

        sets = [set(self.stores.get(t, {}).keys()) for t in comp_types]
        if not sets:
            return set()
        return set.intersection(*sets)

    def __repr__(self) -> str:
        """Returns a string representation of the component store state."""
        return f"<ComponentStore types={list(self.stores.keys())}>"
