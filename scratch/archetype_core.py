"""Artifact ID: CORE-FDE-ARCH-011
Ethos: Memory is Contiguous; Access is Linear.
"""

from typing import Any, Dict, FrozenSet, List, Type


class Archetype:
    """A strictly columnar table holding all entities with an identical component signature."""

    def __init__(self, signature: FrozenSet[Type]):
        self.signature = signature
        self.entity_ids: List[int] = []
        # Structure of Arrays (SoA): {ComponentType: [Instance1, Instance2, ...]}
        self.columns: Dict[Type, List[Any]] = {comp_type: [] for comp_type in signature}

    def add_entity(self, entity_id: int, components: Dict[Type, Any]) -> int:
        """Adds an entity to the end of the arrays and returns its row index."""
        self.entity_ids.append(entity_id)
        for comp_type in self.signature:
            self.columns[comp_type].append(components[comp_type])
        return len(self.entity_ids) - 1

    def snapshot(self) -> Dict[str, Any]:
        """Rollback anchor: Fast shallow copy due to frozen dataclasses."""
        return {
            "entity_ids": self.entity_ids.copy(),
            "columns": {ctype: col.copy() for ctype, col in self.columns.items()},
        }


class ArchetypeRegistry:
    """Replaces ComponentStore. Routes entities into the correct Archetype tables."""

    def __init__(self):
        self._archetypes: Dict[FrozenSet[Type], Archetype] = {}
        # Tracks which Archetype table and row an entity currently lives in
        self._entity_index: Dict[int, tuple[FrozenSet[Type], int]] = {}

    def get_matching_archetypes(
        self, required_components: set[Type]
    ) -> List[Archetype]:
        """O(1) System Query. Returns entire tables that contain the required components,
        completely bypassing entity-level set intersections.
        """
        matches = []
        for signature, archetype in self._archetypes.items():
            if required_components.issubset(signature):
                matches.append(archetype)
        return matches


# --- UPDATED SYSTEM CONTRACT ---


class MovementSystem:
    name = "movement"
    execution_index = 10
    reads = {Position, Velocity}
    writes = {Position}
    accumulates = set()

    def query(self, world) -> List[Archetype]:
        # The query now returns tables, not entity IDs.
        return world.registry.get_matching_archetypes(self.reads | self.writes)

    def compute(self, world, archetypes: List[Archetype]) -> Dict[str, Any]:
        delta = {"mutations": {Position: {}}, "spawns": [], "despawns": []}

        for arch in archetypes:
            # Linear, cache-friendly iteration through contiguous arrays
            positions = arch.columns[Position]
            velocities = arch.columns[Velocity]

            for i in range(len(arch.entity_ids)):
                eid = arch.entity_ids[i]
                p = positions[i]
                v = velocities[i]

                # Generate frozen dataclass delta
                delta["mutations"][Position][eid] = Position(p.x + v.dx, p.y + v.dy)

        return delta
