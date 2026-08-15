"""
artifact_anchor:
  id: CORE.LOOM_PARSER.001
  version: v15.0 [OMEGA]
  provenance: '2026-08-13'
  domain: CORE-CSE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
"""

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

import logging
import os
import re

logger = logging.getLogger("PhoenixLogger")


class LoomParser:
    """WHAT: Extracts active state data from the Synarche Loom.
    HOW: Searches candidate paths and utilizes Regex anchors to pull Mission and Phase variables.
    WHY: To translate human-readable markdown into machine-readable logic.
    """

    MISSION_PATTERN = re.compile(r"Active Mission:\s*(.*)")
    PHASE_PATTERN = re.compile(r"Phase:\s*(.*)")

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
        self.candidate_paths = [
            os.path.join(root_dir, "Flattened_Synarche_Synthesis_System_Loom.md"),
            os.path.join(root_dir, "_governance", "06_Learning", "Flattened_Synarche_Synthesis_System_Loom.md"),
            os.path.join(root_dir, "_governance", "Flattened_Synarche_Synthesis_System_Loom.md"),
            os.path.join(root_dir, "axion-core", "Flattened_Synarche_Synthesis_System_Loom.md"),
        ]

    def _resolve_loom_path(self) -> str | None:
        for path in self.candidate_paths:
            if os.path.exists(path):
                return path
        return None

    def extract_state(self) -> dict[str, str]:
        """Extracts the current mission and phase state from the Loom substrate.

        Returns:
            Dict[str, str]: A dictionary containing the mission and phase values.
        """
        loom_path = self._resolve_loom_path()
        if not loom_path:
            logger.warning("[LoomParser] Substrate file not found in candidate paths. Using default canonical state.")
            return {
                "mission": "SYNARCHE",
                "phase": "ALPHA",
            }

        try:
            with open(loom_path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"[LoomParser] Failed to read Loom at '{loom_path}': {e}. Using fallback.")
            return {
                "mission": "SYNARCHE",
                "phase": "ALPHA",
            }

        mission_match = self.MISSION_PATTERN.search(content)
        phase_match = self.PHASE_PATTERN.search(content)

        return {
            "mission": mission_match.group(1).strip() if mission_match else "SYNARCHE",
            "phase": phase_match.group(1).strip() if phase_match else "ALPHA",
        }
