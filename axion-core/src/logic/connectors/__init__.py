"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.logic.connectors.init`              | The Sovereign ID. |
| **Official Name** | `src/logic/connectors/__init__.py`        | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

## **[ARTIFACT END]**

Standardizes the exposure of parsing and generation connectors within the Axion Core logic layer.
"""

from .freeplane_parser import FreeplaneParser
from .artifact_generator import ArtifactGenerator

__all__ = ["FreeplaneParser", "ArtifactGenerator"]

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.logic.connectors.init VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28
# ---
