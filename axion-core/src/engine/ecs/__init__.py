"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-ECS-INI-001`             | The Sovereign ID. |
| **Official Name**   | `__init__.py`                 | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-ECS`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Coherence`        | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Structural Coherence (Law 02)**
> Implemented from Blueprint `GVRN.REG.EcsEngine.md`.
> Ethos: Stability through composition.
"""

from .ecs_scheduler import ECSScheduler, SystemTask
from .entity_registry import EntityRegistry
from .resonance import ResonanceAuditor, ResonanceDomain, ResonanceRegistry
from .synergy import SynergyMetrics, SynergySystem
from .world import World

__all__ = [
    "ECSScheduler",
    "EntityRegistry",
    "ResonanceAuditor",
    "ResonanceDomain",
    "ResonanceRegistry",
    "SynergyMetrics",
    "SynergySystem",
    "SystemTask",
    "World",
]
