# ecs/entity_registry.py


class EntityRegistry:
    def __init__(self):
        self._next_id = 1
        self._archetypes = {}  # signature -> Archetype
        self._entity_index = {}  # eid -> (signature, row)

    def create(self):
        eid = self._next_id
        self._next_id += 1
        return eid

    def snapshot(self):
        return self._next_id

    def restore(self, val):
        self._next_id = val
