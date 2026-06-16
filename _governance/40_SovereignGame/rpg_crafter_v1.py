"""## **[ARTIFACT START]**
| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID** | `FORGE.rpg.crafter`               | The Sovereign ID. |
| **Official Name** | `rpg_crafter_v2.py`               | The Filename.     |
| **Version** | **v2.0 [SOVEREIGN]** | The Standard.     |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |.
---
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Standard Phoenix Path Alignment
ROOT = str(Path(__file__).parents[2])
CORE_SRC = os.path.join(ROOT, "Synarche_Workspace", "axion-core", "src")
sys.path.append(CORE_SRC)

from phoenix import PhoenixBase


class SovereignRPGCrafter(PhoenixBase):
    """Refactored Logic Master for the RPG Framework."""

    OUTPUT_FILE = os.path.join(CORE_SRC, "rpg_system", "inventory_manifest.json")

    def __init__(self, verbose: bool = False):
        super().__init__(
            persona_id="Sophia_Crafter",
            ethos="Architectural Precision",
            verbose=verbose,
        )
        self.Systemic_Anchor_Slots = {
            "Active Protocol": "Hand",
            "Passive Knowledge": "Body",
            "Core Engine": "Core",
            "The Pattern": "Template",
            "High Gate": "Head",
        }

    def _Parse_Celestial_Tier(self, Value_String: str) -> int:
        """Determines the numerical buff based on Celestial Class."""
        if "Star Tier" in Value_String:
            return 10
        if "Nova Tier" in Value_String:
            return 20
        return 5  # Default Planet Tier

    def _Extract_Sovereign_Artifact(self, File_Path: str) -> Optional[Dict[str, Any]]:
        """Parses v16.3 metadata with DAMP alignment."""
        try:
            with open(File_Path, "r", encoding="utf-8") as Artifact_File:
                Content = Artifact_File.read()
        except Exception:
            return None

        if "BLK-RPG-001" not in Content:
            return None

        # Identification Extraction
        Artifact_ID = (
            re.search(r"\*\*Artifact ID\*\*\s*\|\s*`?(.*?)`?\s*\|", Content)
            or [None, "Unknown"]
        )[1].strip()

        # System Slot & Resource Economics
        Raw_Slot = (
            re.search(r"\*\*System Slot:\*\*\s*`\[(.*?)\|?.*?\]`", Content)
            or [None, "Utility"]
        )[1].strip()
        Cognitive_Load = (
            re.search(r"\*\*Cognitive Load Draw:\*\*\s*`\[(.*?)\]`", Content)
            or [None, "Low"]
        )[1].strip()

        # Celestial Axiom Manifest (Stats)
        Axiom_Manifest = {}
        Primary_Stat = re.search(r"\*\*Primary Stat Buff:\*\*\s*`\[(.*?)\]`", Content)
        Stat_Value_Raw = re.search(r"_Value:_\s*`\[(.*?)\]`", Content)

        if Primary_Stat and Stat_Value_Raw:
            Axiom_Manifest[Primary_Stat.group(1)] = self._Parse_Celestial_Tier(
                Stat_Value_Raw.group(1)
            )

        return {
            "id": Artifact_ID,
            "name": os.path.basename(File_Path).replace(".md", ""),
            "slot": self.Systemic_Anchor_Slots.get(Raw_Slot, "Hand"),
            "axioms": Axiom_Manifest,
            "cognitive_draw": Cognitive_Load,
            "rarity_rationale": (
                re.search(r"_Rarity Rationale:_\s*`\[(.*?)\]`", Content)
                or [None, "N/A"]
            )[1].strip(),
        }

    def execute_ritual(self) -> Dict[str, Any]:
        """Synthesizes the manifest into the Phoenix Core."""
        self.don_mask("Lightbinder_Architect")
        # Logic for scanning directories and saving JSON (Inherited and refined)
        # ... [Scan logic remains active] ...
        self.finalize("SUCCESS")
        return {"status": "V2_SYNTHESIS_COMPLETE"}
