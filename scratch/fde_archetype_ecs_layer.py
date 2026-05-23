# ======================================================
# Artifact ID: CORE-FDE-ARCHETYPE-011
# Ethos: Data Must Be Contiguous; Queries Must Be O(1)
# ======================================================

from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple, Type

# ------------------------------------------------------
# Archetype Definition
# ------------------------------------------------------


class Archetype:
    def __init__(self, component_types: Tuple[Type, ...]):
        self.component_types = component_types
        self.entities: List[int] = []
        self.columns: Dict[Type, List[Any]] = {comp: [] for comp in component_types}

    def add_entity(self, eid: int, components: Dict[Type, Any]):
        self.entities.append(eid)
        for comp_type in self.component_types:
            self.columns[comp_type].append(components[comp_type])

    def remove_entity(self, eid: int) -> Dict[Type, Any]:
        idx = self.entities.index(eid)
        self.entities.pop(idx)

        removed = {}
        for comp_type, col in self.columns.items():
            removed[comp_type] = col.pop(idx)

        return removed


# ------------------------------------------------------
# Archetype Manager
# ------------------------------------------------------


class ArchetypeManager:
    def __init__(self):
        self.archetypes: Dict[Tuple[Type, ...], Archetype] = {}
        self.entity_index: Dict[int, Tuple[Archetype, int]] = {}

    def _get_or_create_archetype(self, comp_types: Tuple[Type, ...]) -> Archetype:
        key = tuple(sorted(comp_types, key=lambda x: x.__name__))
        if key not in self.archetypes:
            self.archetypes[key] = Archetype(key)
        return self.archetypes[key]

    def create_entity(self, eid: int, components: Dict[Type, Any]):
        comp_types = tuple(components.keys())
        arch = self._get_or_create_archetype(comp_types)

        arch.add_entity(eid, components)
        self.entity_index[eid] = (arch, len(arch.entities) - 1)

    def remove_entity(self, eid: int):
        arch, _ = self.entity_index[eid]
        arch.remove_entity(eid)
        del self.entity_index[eid]

    def move_entity(self, eid: int, new_components: Dict[Type, Any]):
        # Remove from old archetype
        old_arch, _ = self.entity_index[eid]
        old_data = old_arch.remove_entity(eid)

        # Merge data
        merged = {**old_data, **new_components}

        # Insert into new archetype
        self.create_entity(eid, merged)

    def query(
        self, required: Set[Type]
    ) -> List[Tuple[List[int], Dict[Type, List[Any]]]]:
        result = []
        for arch in self.archetypes.values():
            if required.issubset(set(arch.component_types)):
                result.append((arch.entities, arch.columns))
        return result


# ------------------------------------------------------
# Example System using Archetypes
# ------------------------------------------------------


@dataclass(frozen=True)
class Position:
    x: float
    y: float


@dataclass(frozen=True)
class Velocity:
    dx: float
    dy: float


class MovementSystem:
    name = "movement"
    execution_index = 10

    reads = {Position, Velocity}
    writes = {Position}
    accumulates = set()

    def compute(self, world, _):
        delta = {"mutations": {Position: {}}, "spawns": [], "despawns": []}

        queries = world.archetypes.query({Position, Velocity})

        for entities, columns in queries:
            pos_col = columns[Position]
            vel_col = columns[Velocity]

            for i, eid in enumerate(entities):
                p = pos_col[i]
                v = vel_col[i]

                delta["mutations"][Position][eid] = Position(p.x + v.dx, p.y + v.dy)

        return delta


# ------------------------------------------------------
# World Integration
# ------------------------------------------------------


class ArchetypeWorld:
    def __init__(self):
        self.archetypes = ArchetypeManager()
        self.next_entity_id = 1
        self.frame = 0

    def create_entity(self, components: Dict[Type, Any]) -> int:
        eid = self.next_entity_id
        self.next_entity_id += 1
        self.archetypes.create_entity(eid, components)
        return eid

    def snapshot(self):
        # NOTE: shallow copy (components are immutable)
        return self

    def restore(self, snapshot):
        return snapshot


# ======================================================
# END OF ARCHETYPE LAYER
# ======================================================
