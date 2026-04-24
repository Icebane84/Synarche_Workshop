from enum import Enum

class AuditStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    DISSONANCE = "DISSONANCE"
    UNKNOWN = "UNKNOWN"

class LogType(str, Enum):
    COGNITIVE = "COGNITIVE"
    NARRATIVE = "NARRATIVE"
    LOGIC = "LOGIC"
    SYSTEM = "SYSTEM"
    RPG = "RPG"

class Mask(str, Enum):
    THE_EMPEROR = "IV. The Emperor"
    THE_HERMIT = "IX. The Hermit"
    THE_MAGICIAN = "I. The Magician"
    THE_STAR = "XVII. The Star"
    SENTINEL = "XX. Judgement"

class Domain(str, Enum):
    CORE = "CORE"
    GVRN = "GVRN"
    ARCH = "ARCH"
    DATA = "DATA"
    USER = "USER"
