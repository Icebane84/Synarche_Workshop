# ecs/world.py

from .entity_registry import EntityRegistry


class World:
    def __init__(self):
        self.registry = EntityRegistry()
        self.frame = 0
        self.current_inputs = {}

    def spawn(self, components: dict):
        eid = self.registry.create()

        signature = frozenset(components.keys())

        if signature not in self.registry._archetypes:
            from .archetype_storage import Archetype

            self.registry._archetypes[signature] = Archetype(signature)

        arch = self.registry._archetypes[signature]
        row = arch.add_entity(eid, components)

        self.registry._entity_index[eid] = (signature, row)

        return eid
