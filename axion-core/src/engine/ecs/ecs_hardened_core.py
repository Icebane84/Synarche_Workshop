"""Artifact ID: CORE-FDE-ECS-006
Ethos: Type-Safety is Non-Negotiable; State is Immutable.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Set, Type


# 1. IMMUTABLE COMPONENTS (Zero-Copy Safe)
@dataclass(frozen=True)
class Position:
    x: float
    y: float


@dataclass(frozen=True)
class Velocity:
    dx: float
    dy: float


# 2. HARDENED COMPONENT STORE
class ComponentStore:
    def __init__(self):
        # Keys are actual Class Types, NOT strings
        self._stores: Dict[Type, Dict[int, Any]] = {}

    def add_component(self, entity_id: int, comp_type: Type, data: Any):
        if comp_type not in self._stores:
            self._stores[comp_type] = {}
        self._stores[comp_type][entity_id] = data

    def get_store(self, comp_type: Type) -> Dict[int, Any]:
        return self._stores.get(comp_type, {})

    def snapshot(self) -> Dict[Type, Dict[int, Any]]:
        # Fast Shallow Copy: Because components are frozen, we only copy the dict structure.
        # This eliminates the massive O(N) deepcopy bottleneck per frame.
        return {comp_type: store.copy() for comp_type, store in self._stores.items()}

    def restore(self, snapshot: Dict[Type, Dict[int, Any]]):
        self._stores = {
            comp_type: store.copy() for comp_type, store in snapshot.items()
        }


# 3. PURE SYSTEM WITH STRUCTURAL DELTAS
class MovementSystem:
    name = "movement"

    def query(self, world) -> List[int]:
        # Note: In Phase 7, this O(N) intersection will be replaced by cached Archetypes
        pos_keys = world.components.get_store(Position).keys()
        vel_keys = world.components.get_store(Velocity).keys()
        return list(set(pos_keys) & set(vel_keys))

    def compute(self, world, entities: List[int]) -> Dict[str, Any]:
        pos_store = world.components.get_store(Position)
        vel_store = world.components.get_store(Velocity)

        # Expanded Delta Schema
        delta = {
            "mutations": {Position: {}},
            "spawns": [],  # Example: [{"components": {Position: ..., Velocity: ...}}]
            "despawns": [],  # Example: [entity_id_1, entity_id_2]
        }

        for eid in entities:
            p = pos_store[eid]
            v = vel_store[eid]

            # We instantiate a NEW frozen dataclass instead of mutating
            delta["mutations"][Position][eid] = Position(p.x + v.dx, p.y + v.dy)

        return delta


# 4. DETERMINISTIC ECS COMMIT LAYER
def apply_ecs_delta(world, delta: Dict[str, Any], seen_mutations: Set[tuple]):
    comps = world.components

    # Process Despawns First
    for eid in delta.get("despawns", []):
        for store in comps._stores.values():
            store.pop(eid, None)

    # Process Spawns
    for spawn_data in delta.get("spawns", []):
        new_eid = world.registry.create()
        for comp_type, comp_data in spawn_data.get("components", {}).items():
            comps.add_component(new_eid, comp_type, comp_data)

    # Process Mutations (with strict collision detection)
    for comp_type, updates in delta.get("mutations", {}).items():
        store = comps._stores.setdefault(comp_type, {})

        for eid, new_value in updates.items():
            collision_key = (comp_type, eid)
            if collision_key in seen_mutations:
                raise RuntimeError(
                    f"Collision: Multiple systems mutating {comp_type.__name__} on Entity {eid}"
                )

            seen_mutations.add(collision_key)
            store[eid] = new_value
