"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CSE-VAL-001`            | The Sovereign ID. |
| **Official Name**   | `law_validator.py`            | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Law Enforcement (Law 30)**
> Implemented from Blueprint `GVRN.REG.LawValidator.md`.
> Ethos: Truth through Validation.
"""

import json
import os
from typing import Any, Dict, List


class LawValidator:
    """WHAT: Cross-references Loom data against absolute Governance data.
    HOW: Compares ingested dictionary states with task.md.metadata.json.
    WHY: To identify 'Context Drift' and enforce Zero Entropy.
    """

    def __init__(self, root_dir: str):
        self.meta_path = os.path.join(root_dir, "task.md.metadata.json")

    def audit_drift(self, loom_state: Dict[str, Any]) -> List[str]:
        """Audits the current state for drift against the governance metadata.

        Args:
            loom_state (Dict[str, Any]): The current state ingested from the Loom.

        Returns:
            List[str]: A list of findings indicating drift or compliance issues.

        """
        findings = []
        if not os.path.exists(self.meta_path):
            findings.append("CRITICAL: task.md.metadata.json is missing.")
            return findings

        try:
            with open(self.meta_path, encoding="utf-8") as f:
                metadata = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            findings.append(f"CRITICAL: Failed to load metadata: {e!s}")
            return findings

        target_mission = metadata.get("mission_id", "UNDEFINED")

        if loom_state.get("mission") != target_mission:
            findings.append(
                f"MISSION_DRIFT: Loom({loom_state.get('mission')}) != Law({target_mission})"
            )

        return findings
