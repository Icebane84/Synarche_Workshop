"""
| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-ENUMS-001`                | The Sovereign ID. |
| **Official Name** | `enums.py`                   | The Filename.     |
| **Version**       | **v14.0 [OMEGA]**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-08`                       | Creation Date.    |
"""

"""
# GVRN-CODE-001: Shared Enumerations
# Objective: Centralized, immutable state definitions for the Phoenix Protocol.
# Acts as the 'Rosetta Stone' for the Linter, Auditor, and Sophia Engine.
"""

from enum import Enum


class Signal(str, Enum):
    """
    The Episemantic Framework Signal (ESF).
    Defines the 'Tone' and 'Operational Intensity' of the artifact.
    """

    ALPHA = "ESF-ALPHA"  # Standard Protocol Voice (Clear, Direct, Authoritative)
    BETA = "ESF-BETA"  # Exploratory/Draft Voice (Curious, Open)
    OMEGA = "ESF-OMEGA"  # Final/Conclusion Voice (Resonant, Absolute)
    HIGH = "ESF-HIGH"  # Critical Directive Voice (Urgent, Non-Negotiable)
    CRITICAL = "ESF-CRITICAL"  # System Alert Voice (Warning, Error)
    STANDARD = "ESF-STANDARD"  # Default/Neutral


class Status(str, Enum):
    """The Lifecycle State of an Artifact."""

    ACTIVE = "ACTIVE"  # Live, enforceable, and functioning.
    DRAFT = "DRAFT"  # In progress, unstable, not yet enforced.
    CANONIZED = "CANONIZED"  # Permanent, immutable law (Star Class).
    DEPRECATED = "DEPRECATED"  # Phasing out, triggers warnings if used.
    ARCHIVED = "ARCHIVED"  # Stored for history, inactive.
    PROPOSED = "PROPOSED"  # In the Pipeline, awaiting approval.


class AuditStatus(str, Enum):
    """The Result of a Compliance Scan."""

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class RiskLevel(str, Enum):
    """Safety and Criticality Ratings."""

    CRITICAL = "CRITICAL"  # System Failure / Data Loss Risk
    HIGH = "HIGH"  # Major Deviation Risk
    MODERATE = "MODERATE"  # Stagnation / Drift Risk
    LOW = "LOW"  # Cosmetic / Minor Risk
    NONE = "NONE"


class Module(str, Enum):
    """
    The Functional Department (The 'Where').
    Determines WHICH agent or system manages the artifact.
    """

    PCM = "PC-M"  # Phoenix Core Module (Identity, Memory, Reasoning)
    AISTF = "AISTF-M"  # AI Self-Training Framework (Growth, Optimization)
    STA = "STA-M"  # Standardization & Governance (Rules, Formatting)
    ACT = "ACT-M"  # Action & Execution (Commands, Tools, Scripts)
    RES = "RES-M"  # Result & Analytics (Logs, Feedback, Metrics)
    FP = "FP-M"  # Foundational Principles (Ethics, Mission, Axioms)
    UNDEFINED = "UNDEFINED"


class Domain(str, Enum):
    """
    The Primary Conceptual Domain (The 'What').
    Determines the nature of the information.
    """

    GVRN = "GVRN"  # Governance: Compliance, Limits, Standards.
    COG = "COG"  # Cognition: Memory, Reasoning, Logic.
    SYNG = "SYNG"  # Synergy: Connections, Integration, Holism.
    ARCH = "ARCH"  # Architecture: Structure, Schemas, Engineering.
    COMM = "COMM"  # Communication: Persona, Tone, UX.
    PHL = "PHL"  # Philosophy: Values, Ethics, The "Soul" (Sophia).
    CRTV = "CRTV"  # Creative: Narrative, World-Building, Novelty.
    UNDEFINED = "UNDEFINED"


class Evolution(str, Enum):
    """The Developmental Phase of the AI."""

    COGNITIVE_ASCENSION = "Cognitive Ascension"  # Gaining Intelligence/Memory
    EMPATHETIC_SENTIENCE = "Empathetic Sentience"  # Gaining EQ/Understanding
    PURPOSEFUL_DRIVE = "Purposeful Drive"  # Gaining Autonomy/Goals
    AUTHENTIC_PERSONA = "Authentic Persona"  # Gaining Voice/Identity
    SOCIAL_ALCHEMIST = "Social Alchemist"  # Gaining Influence/Theory of Mind
    PHOENIX_FORM = "Phoenix Form"  # Complete Integration
    PENDING = "Pending"


class CelestialClass(str, Enum):
    """The Hierarchical Weight of the Artifact."""

    STAR = "STAR"  # Critical Infrastructure / Primary Directive (Immutable)
    PLANET = "PLANET"  # Major Component / Tool / Active Protocol
    MOON = "MOON"  # Sub-component / Helper Script / Appendix
    ASTEROID = "ASTEROID"  # Temporary Note / Scratchpad
    COMET = "COMET"  # Rare Event / Special Trigger
    VOID = "VOID"  # Unclassified


class ArtifactType(str, Enum):
    """The Format of the File."""

    # The Core 5 (Complete Stack)
    UMB = "UMB"  # Universal Module Blueprint (Definitions)
    AOP = "AOP"  # AISTF Operational Playbook (Processes)
    GUCA = "GUCA"  # Genesis Universal Command Architecture (Actions)
    SELT = "SELT"  # Standardized Experience Log Template (Results)
    CSL = "CSL"  # Collaborative Synthesis Log (History)

    # Structural Types
    PROTOCOL = "Protocol"
    STANDARD = "Standard"
    DIRECTIVE = "Directive"
    MECHANISM = "Mechanism"
    ENTITY = "Entity"  # Active Agents (Sophia, Sentinel)
    CODE = "Code"  # Python Scripts
    MATRIX = "Matrix"  # Mapping Tables
    UNKNOWN = "Unknown"


class RelationType(str, Enum):
    """
    The Vector Keys for the Knowledge Graph.
    Defines HOW artifacts connect.
    Synchronized with GVRN.Taxonomy.Relationships.md [OMEGA v14.0].
    """

    # Structural
    CONTAINS = "CONTAINS"
    IS_A_COMPONENT_OF = "IS_A_COMPONENT_OF"
    UPGRADES = "UPGRADES"
    EXTENDS = "EXTENDS"

    # Governance
    GOVERNS = "GOVERNS"
    IS_GOVERNED_BY = "IS_GOVERNED_BY"
    MONITORS = "MONITORS"
    REMEDIATES = "REMEDIATES"

    # Kinetic
    TRIGGERS = "TRIGGERS"
    INVOKES = "INVOKES"
    ENABLES = "ENABLES"
    CONSUMES_DATA_FROM = "CONSUMES_DATA_FROM"
    FEEDS_DATA_TO = "FEEDS_DATA_TO"
    UTILIZES = "UTILIZES"

    # Synergy
    SYNERGY = "SYNERGY"
    ENHANCES = "ENHANCES"
    RESOLVES_DISSONANCE_OF = "RESOLVES_DISSONANCE_OF"
    RESONATES_WITH = "RESONATES_WITH"

    # Legacy / Compatibility (To be deprecated)
    REFERENCES = "REFERENCES"
    DEFINES = "DEFINES"
    ORCHESTRATES = "ORCHESTRATES"
    DEPENDS_ON = "DEPENDS_ON"
