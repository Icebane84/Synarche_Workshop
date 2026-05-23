"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.agents.axion.init`          | The Sovereign ID. |
| **Official Name** | `__init__.py`                     | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                 | The Standard.     |
| **Domain**        | `CORE`                            | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

## **[ARTIFACT END]**
"""

from .agent_template import RPGEngine, app
from .config import settings

__all__ = ["RPGEngine", "app", "settings"]

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.agents.axion.init VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 374451432ed01801
