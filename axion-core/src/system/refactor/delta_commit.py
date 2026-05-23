"""Artifact ID: CORE-FDE-ECS-CMT-001
Ethos: Explicit Collision is Better Than Silent Corruption.
"""

from typing import Any, Dict, Set


def apply_ecs_delta(world, delta: Dict[str, Any], seen_mutations: Set[tuple]) -> None:
    """The deterministic bottleneck. Processes structured delta packets
    emitted by parallel systems and safely merges them into the World.
    """
    comps = world.components

    # 1. Process Despawns (Absolute Removal)
    for eid in delta.get("despawns", []):
        for store in comps._stores.values():
            store.pop(eid, None)

    # 2. Process Spawns (Absolute Creation)
    for spawn_data in delta.get("spawns", []):
        new_eid = world.registry.create()
        for comp_type, comp_data in spawn_data.get("components", {}).items():
            comps.add_component(new_eid, comp_type, comp_data)

    # 3. Process Mutations (Fail-Fast Collision Detection)
    for comp_type, updates in delta.get("mutations", {}).items():
        store = comps._stores.setdefault(comp_type, {})

        for eid, new_value in updates.items():
            collision_key = (comp_type, eid)
            if collision_key in seen_mutations:
                raise RuntimeError(
                    f"FDE Violation: Multiple systems mutated {comp_type.__name__} on Entity {eid}"
                )

            seen_mutations.add(collision_key)
            store[eid] = new_value
