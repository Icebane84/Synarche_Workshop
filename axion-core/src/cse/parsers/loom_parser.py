"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-CSE-PAR-001`            | The Sovereign ID. |
| **Official Name**   | `loom_parser.py`              | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-CSE`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Ingestive Purity (Law 32)**
> Implemented from Blueprint `GVRN.REG.LoomParser.md`.
> Ethos: Clarity through Parsing.
"""

import os
import re


class LoomParser:
    """WHAT: Extracts active state data from the Synarche Loom.
    HOW: Utilizes Regex anchors to pull Mission and Phase variables.
    WHY: To translate human-readable markdown into machine-readable logic.
    """

    MISSION_PATTERN = re.compile(r"Active Mission:\s*(.*)")
    PHASE_PATTERN = re.compile(r"Phase:\s*(.*)")

    def __init__(self, root_dir: str) -> None:
        self.loom_path = os.path.join(
            root_dir, "Flattened_Synarche_Synthesis_System_Loom.md"
        )

    def extract_state(self) -> dict[str, str]:
        """Extracts the current mission and phase state from the Loom substrate.

        Returns:
            Dict[str, str]: A dictionary containing the mission and phase values.

        Raises:
            FileNotFoundError: If the Loom file is missing.
            RuntimeError: If the Loom file cannot be read.

        """
        if not os.path.exists(self.loom_path):
            raise FileNotFoundError(f"CRITICAL: Substrate missing at {self.loom_path}")

        try:
            with open(self.loom_path, encoding="utf-8") as f:
                content = f.read()
        except PermissionError as e:
            raise RuntimeError(
                f"CRITICAL: Substrate at '{self.loom_path}' is locked by another process or access is denied."
            ) from e

        mission_match = self.MISSION_PATTERN.search(content)
        phase_match = self.PHASE_PATTERN.search(content)

        return {
            "mission": mission_match.group(1).strip() if mission_match else "UNKNOWN",
            "phase": phase_match.group(1).strip() if phase_match else "UNKNOWN",
        }
