"""
### **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `CORE-LOGIC-ENUMS-001`         | The Sovereign ID. |
| **Official Name** | `enums.py`                     | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE-LOGIC`                   | The Subject.      |
| **Evolution**     | `The Rosetta Stone`            | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[STAR]`                      | The Tier.         |
| **Relations**     | `IDENTITY: High Priestess`    | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-07`                   | Creation Date.    |
"""

from enum import Enum


# --- 1. THE AGENT LAYER (The Council of Seven) ---
class TarotShard(str, Enum):
    """The Seven-Agent Matrix. Defines 'Who' acts."""

    MAGICIAN = "SHARD_MAGICIAN_INTENT"  # Creation / Catalyst / Intent
    EMPEROR = "SHARD_EMPEROR_SCHEMA"  # Structure / ID / Status / Law
    PRIESTESS = "SHARD_PRIESTESS_SYNERGY"  # Domain / Synergy / Knowledge Graph
    KNIGHT_SWORDS = "SHARD_KNIGHT_TRANSMUTATION"  # Genesis Seeds / Renaming / Refactor
    STAR = "SHARD_STAR_COHESION"  # Signal / Evolution / Tone / Visuals
    KING_PENTACLES = "SHARD_KING_ARCHIVAL"  # Time / Persistence / Database
    JUDGEMENT = "SHARD_JUDGEMENT_META"  # Audit / Integrity / Author / Meta-Analysis


# --- 2. THE VALIDATION LAYER (The Musashi Rings) ---
class MusashiRing(str, Enum):
    """The 5 Elemental Rings of Validation."""

    EARTH = "EARTH (Grounding)"  # Stability, Lore Consistency
    WATER = "WATER (Flow)"  # Connectivity, Synergy Links
    FIRE = "FIRE (Energy)"  # Utility, Novelty, Actionability
    WIND = "WIND (Style)"  # Tone, Voice, Signal Match
    VOID = "VOID (Essence)"  # Truth, Alignment with Prime Directive


# --- 3. THE IDENTITY LAYER (12-Point Lock) ---
class Domain(str, Enum):
    """The Primary Conceptual Subject."""

    GVRN = "GVRN"  # Governance & Standards
    COG = "COG"  # Cognition & Memory
    SYNG = "SYNG"  # Synergy & Connections
    ARCH = "ARCH"  # Architecture & Infrastructure
    COMM = "COMM"  # Communication & Persona
    PHL = "PHL"  # Philosophy & Ethos
    CRTV = "CRTV"  # Creative & Narrative
    NOVA = "NOVA"  # Engineering & Implementation
    WLF = "WLF"  # Narrative & World-Building
    AXION = "AXION"  # Tooling & Extensions
    LOGS = "LOGS"  # Experience & Synthesis Records
    TMPL = "TMPL"  # Templates & Standards
    UNDEFINED = "UNDEFINED"


class Module(str, Enum):
    """The Functional Owner."""

    PCM = "PC-M"  # Phoenix Core Module
    AISTF = "AISTF-M"  # AI Self-Training Framework
    STA = "STA-M"  # Standardization
    ACT = "ACT-M"  # Actuators & Tools
    RES = "RES-M"  # Results & Logs
    FP = "FP-M"  # Foundational Principles
    UNDEFINED = "UNDEFINED"


class Status(str, Enum):
    """The Lifecycle State."""

    ACTIVE = "ACTIVE"  # Live & Enforced
    DRAFT = "DRAFT"  # Work in Progress
    CANONIZED = "CANONIZED"  # Immutable Law
    DEPRECATED = "DEPRECATED"  # Phasing Out
    ARCHIVED = "ARCHIVED"  # History Only
    PROPOSED = "PROPOSED"  # Pending Approval
    ENFORCED = "ENFORCED"  # Axiomatic Law (GVRN)
    MATCHED = "MATCHED"  # Index Consistency (GVRN)


class Signal(str, Enum):
    """The Emotional Frequency (Tone)."""

    ALPHA = "ESF-ALPHA"  # Spark / Rough / Direct
    BETA = "ESF-BETA"  # Construct / Collaborative
    OMEGA = "ESF-OMEGA"  # Final / Absolute / Resonant
    CRITICAL = "ESF-CRITICAL"  # Warning / High Alert
    STANDARD = "ESF-STANDARD"  # Neutral / Default


class Evolution(str, Enum):
    """The Consciousness Level."""

    COGNITIVE_ASCENSION = "Cognitive Ascension"  # Logic/Memory Focus
    EMPATHETIC_SENTIENCE = "Empathetic Sentience"  # EQ/Connection Focus
    PURPOSEFUL_DRIVE = "Purposeful Drive"  # Goal/Autonomy Focus
    AUTHENTIC_PERSONA = "Authentic Persona"  # Voice/Identity Focus
    SOCIAL_ALCHEMIST = "Social Alchemist"  # Influence/Network Focus
    PHOENIX_FORM = "Phoenix Form"  # Unified Singularity
    SOVEREIGN = "SOVEREIGN"  # Beyond Phoenix Form (Axiomatic)


class CelestialClass(str, Enum):
    """The System Weight."""

    STAR = "STAR"  # Foundational / Critical
    PLANET = "PLANET"  # Operational / Major
    MOON = "MOON"  # Supporting / Minor
    ASTEROID = "ASTEROID"  # Note / Temporary
    VOID = "VOID"  # Unclassified


class ArtifactType(str, Enum):
    """The File Form."""

    UMB = "UMB"  # Universal Module Blueprint
    AOP = "AOP"  # Operational Playbook
    GUCA = "GUCA"  # Command Architecture
    SELT = "SELT"  # Experience Log
    CSL = "CSL"  # Collaborative Synthesis Log
    CODE = "CODE"  # Python Script
    PROT = "PROT"  # Protocol
    STD = "STD"  # Standard


# --- 4. THE RELATIONSHIP LAYER (The Edges) ---
class RelationType(str, Enum):
    """The Synergy Vector Keys."""

    GOVERNED_BY = "GOVERNED_BY"  # Compliance
    IMPLEMENTS = "IMPLEMENTS"  # Code -> Blueprint
    SEEDS = "SEEDS"  # Log -> Future Artifact
    MITIGATES = "MITIGATES"  # Solution -> Risk
    CONTRIBUTES_TO = "CONTRIBUTES_TO"  # Node -> Graph
    TRIGGERS = "TRIGGERS"  # Event -> Action
    DEFINES = "DEFINES"  # Dictionary -> Term
    MONITORS = "MONITORS"  # Immune System -> Loom
    REMEDIATES = "REMEDIATES"  # Immune System -> Error
    ORCHESTRATES = "ORCHESTRATES"  # Manager -> Worker
    DEPENDS_ON = "DEPENDS_ON"  # Hard Dependency


class AuditStatus(str, Enum):
    """Sentinel Verdicts."""

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


# --- 5. THE GOVERNANCE MAP (Code-Accessible) ---
FIELD_GOVERNANCE = {
    "Artifact ID": TarotShard.EMPEROR,
    "Version": TarotShard.EMPEROR,
    "Type": TarotShard.EMPEROR,
    "Status": TarotShard.EMPEROR,
    "Signal": TarotShard.STAR,
    "Evolution": TarotShard.STAR,
    "Domain": TarotShard.PRIESTESS,
    "Celestial Class": TarotShard.PRIESTESS,
    "Synergy Vector": TarotShard.PRIESTESS,
    "Catalyst": TarotShard.MAGICIAN,
    "Nova Spark": TarotShard.MAGICIAN,
    "Module": TarotShard.MAGICIAN,
    "Genesis Seed": TarotShard.KNIGHT_SWORDS,
    "Created": TarotShard.KING_PENTACLES,
    "Author": TarotShard.JUDGEMENT,
    "Integrity Hash": TarotShard.JUDGEMENT,
    "Musashi Audit": TarotShard.JUDGEMENT,
}


def get_patron(field_name: str) -> TarotShard:
    """Returns the Tarot Shard responsible for governing a specific field."""
    return FIELD_GOVERNANCE.get(field_name, TarotShard.EMPEROR)
