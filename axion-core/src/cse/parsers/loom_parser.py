import os
import re


class LoomParser:
    """
    WHAT: Extracts active state data from the Synarche Loom.
    HOW: Utilizes Regex anchors to pull Mission and Phase variables.
    WHY: To translate human-readable markdown into machine-readable logic.
    """

    MISSION_PATTERN = re.compile(r"Active Mission:\s*(.*)")
    PHASE_PATTERN = re.compile(r"Phase:\s*(.*)")

    def __init__(self, root_dir: str):
        self.loom_path = os.path.join(root_dir, "Flattened_Synarche_Synthesis_System_Loom.md")

    def extract_state(self) -> dict[str, str]:
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
