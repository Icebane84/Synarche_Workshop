"""Artifact ID: CORE-FDE-ECS-WRLD-001
Ethos: The Universe in a Frozen Box.
"""

import copy
from typing import Any, Dict

from .ecs_hardened_core import ComponentStore  # (From Phase 6 Hardened Core)
from .entity_registry import EntityRegistry


class World:
    """The master state container. Replaces the generic 'global_context'.
    Designed specifically for $O(1)$ rollback snapshotting.
    """

    def __init__(self):
        self.components = ComponentStore()
        self.registry = EntityRegistry()
        self.frame: int = 0
        self.current_inputs: Dict[str, Any] = {}

    def snapshot(self) -> Dict[str, Any]:
        """Creates a rollback-safe anchor.
        Because components are frozen dataclasses, this is extremely fast.
        """
        return {
            "components": self.components.snapshot(),
            "registry_id": self.registry.snapshot(),
            "frame": self.frame,
            "inputs": copy.deepcopy(self.current_inputs),
        }

    def restore(self, snap: Dict[str, Any]) -> None:
        """Instantly overwrites the current reality with a past state."""
        self.components.restore(snap["components"])
        self.registry.restore(snap["registry_id"])
        self.frame = snap["frame"]
        self.current_inputs = copy.deepcopy(snap["inputs"])
