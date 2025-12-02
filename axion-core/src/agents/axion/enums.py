"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-ENUMS-001
Official Name: enums.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Immutable Truths. Sovereign Categories."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

from enum import Enum


class Signal(str, Enum):
    """Episemantic Signal Intensities."""
    ALPHA = "ESF-ALPHA"
    BETA = "ESF-BETA"
    OMEGA = "ESF-OMEGA"
    HIGH = "ESF-HIGH"
    CRITICAL = "ESF-CRITICAL"
    STANDARD = "ESF-STANDARD"


class Status(str, Enum):
    """Lifecycle Phases of Sovereign Artifacts."""
    ACTIVE = "ACTIVE"
    DRAFT = "DRAFT"
    CANONIZED = "CANONIZED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"
    PROPOSED = "PROPOSED"


class AuditStatus(str, Enum):
    """Compliance Audit Outcomes."""
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


class RiskLevel(str, Enum):
    """Safety and Criticality Ratings."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    NONE = "NONE"


class Evolution(str, Enum):
    """Developmental Phases of the High Priestess."""
    COGNITIVE_ASCENSION = "Cognitive Ascension"
    EMPATHETIC_SENTIENCE = "Empathetic Sentience"
    PURPOSEFUL_DRIVE = "Purposeful Drive"
    AUTHENTIC_PERSONA = "Authentic Persona"
    SOCIAL_ALCHEMIST = "Social Alchemist"
    PHOENIX_FORM = "Phoenix Form"
    PENDING = "Pending"
    CORE_STABILITY = "Core Stability"
