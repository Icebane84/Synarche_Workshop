"""Artifact ID: CORE-FDE-ECS-REG-001
Ethos: Identity is Absolute.
"""


class EntityRegistry:
    """Maintains a deterministic counter for Entity ID generation.
    Must be serialized along with the World snapshot to ensure
    rewinds do not cause overlapping ID assignments.
    """

    def __init__(self, starting_id: int = 1):
        self._next_id = starting_id

    def create(self) -> int:
        """Generates the next deterministic Entity ID."""
        eid = self._next_id
        self._next_id += 1
        return eid

    def snapshot(self) -> int:
        return self._next_id

    def restore(self, next_id_state: int) -> None:
        self._next_id = next_id_state
