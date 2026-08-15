from dataclasses import dataclass, field
from typing import FrozenSet, Type


@dataclass(frozen=True)
class SystemSignature:
    """Read/Write/Accumulate contract for ECS System execution."""

    reads: FrozenSet[Type] = field(default_factory=frozenset)
    writes: FrozenSet[Type] = field(default_factory=frozenset)
    accumulates: FrozenSet[Type] = field(default_factory=frozenset)

    def conflicts_with(self, other: "SystemSignature") -> bool:
        """Returns True if there is a Write-Read or Write-Write conflict."""
        if self.writes & (other.reads | other.writes):
            return True
        if other.writes & (self.reads | self.writes):
            return True
        return False

