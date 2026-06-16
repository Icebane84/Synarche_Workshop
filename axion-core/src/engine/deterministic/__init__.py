"""
artifact_anchor:
  id: CORE.INIT.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
"""

"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `ENG-DET-INI-001`             | The Sovereign ID. |
| **Official Name**   | `__init__.py`                 | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `ENG-DET`                     | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: Oracle`            | The Sovereign.    |

**The Spirit Bomb Axiom: Systemic Synthesis (Law 01)**
> Implemented from Blueprint `GVRN.REG.DeterministicEngine.md`.
> Ethos: Clarity through initialization.
"""

from ..ecs.resonance import ResonanceAuditor, ResonanceDomain, ResonanceRegistry
from ..ecs.synergy import SynergyMetrics, SynergySystem
from .clock import FixedClock
from .engine import DeterministicEngine
from .executor import Executor
from .graph import TaskGraph
from .parallel_scheduler import ParallelScheduler
from .scheduler import DeterministicScheduler
from .state import StateManager, StateSnapshot
from .task import Task

__all__ = [
    "DeterministicEngine",
    "DeterministicScheduler",
    "Executor",
    "FixedClock",
    "ParallelScheduler",
    "ResonanceAuditor",
    "ResonanceDomain",
    "ResonanceRegistry",
    "StateManager",
    "StateSnapshot",
    "SynergyMetrics",
    "SynergySystem",
    "Task",
    "TaskGraph",
]
