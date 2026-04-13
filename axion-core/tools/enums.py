from enum import Enum, auto


class RelationType(Enum):
    """Relational Physics: Defines how artifacts connect."""
    REFERENCES = auto()
    GOVERNED_BY = auto()
    DEFINES = auto()
    SYNERGY = auto()
    IMPLEMENTS = auto()
    HUB = auto()
    CONTAINS = auto()
    ORCHESTRATES = auto()
    POWERED_BY = auto()
    GOVERNS = auto()
    LINK = auto()
    COMPONENT_OF = auto()
    ACCESSED_BY = auto()
    DEFINED_BY = auto()

class ArtifactType(Enum):
    """Artifact Classification."""
    MODULE = auto()
    PROTOCOL = auto()
    LOG = auto()
    REGISTRY = auto()
    BLUEPRINT = auto()
    AXIOM = auto()
    TEMPLATES = auto()
    SCRIPT = auto()

class CelestialClass(Enum):
    """Hierarchical Weight."""
    STAR = auto()
    PLANET = auto()
    MOON = auto()

class Signal(Enum):
    """Episemantic Signal."""
    ALPHA = auto()
    BETA = auto()
    OMEGA = auto()
    HIGH = auto()

class TarotShard(Enum):
    """Seven-Agent Matrix specialized roles."""
    MAGICIAN = auto()
    EMPEROR = auto()
    PRIESTESS = auto()
    KNIGHT_OF_SWORDS = auto()
    STAR = auto()
    KING_OF_PENTACLES = auto()
    JUDGEMENT = auto()
