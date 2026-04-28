"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGT-ENUM-001`           | The Sovereign ID. |
| **Official Name**   | `enums.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGT`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Taxonomy Purity (Law 38)**
> Implemented from Blueprint `GVRN.REG.AgentEnums.md`.
> Ethos: Clarity through Taxonomy.
"""

from enum import Enum

class AuditStatus(str, Enum):
    """Represents the compliance state of an artifact or process."""
    PASS = "PASS"
    FAIL = "FAIL"
    DISSONANCE = "DISSONANCE"
    UNKNOWN = "UNKNOWN"

class LogType(str, Enum):
    """Categorizes the type of experience log being recorded."""
    COGNITIVE = "COGNITIVE"
    NARRATIVE = "NARRATIVE"
    LOGIC = "LOGIC"
    SYSTEM = "SYSTEM"
    RPG = "RPG"

class Mask(str, Enum):
    """Defines the active Tarot-based persona mask for the agent."""
    THE_EMPEROR = "IV. The Emperor"
    THE_HERMIT = "IX. The Hermit"
    THE_MAGICIAN = "I. The Magician"
    THE_STAR = "XVII. The Star"
    SENTINEL = "XX. Judgement"

class Domain(str, Enum):
    """Specifies the governance domain of the operation."""
    CORE = "CORE"
    GVRN = "GVRN"
    ARCH = "ARCH"
    DATA = "DATA"
    USER = "USER"
