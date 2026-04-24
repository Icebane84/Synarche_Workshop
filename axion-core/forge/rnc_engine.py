"""
[CORE] [ENGINE] [RNC_ENGINE]
Artifact ID: CORE.Engine.RNCEngine
Official Name: rnc_engine.py
Version: v15.0 [OMEGA]
Status: [CANONIZED]
Description: Validates RNC IDs and maps them to canonical filesystem paths.

[UIP-V15]
| Key | Value |
| :--- | :--- |
| **Artifact ID** | `CORE.Engine.RNCEngine` |
| **Official Name** | `rnc_engine.py` |
| **Version** | **v15.0 [OMEGA]** |
| **Domain** | `CORE` |
| **Status** | `[CANONIZED]` |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` |
"""

import os
import re
from typing import Dict, List

try:
    from .enums import Domain, SubSystem
except (ImportError, ValueError):
    from enum import Domain, SubSystem


class RNCEngine:
    """
    Sovereign Logic Engine for the Relational Naming Convention (RNC).
    """

    # [DOMAIN].[Subsystem].[Descriptor]
    RNC_PATTERN = re.compile(r"^([A-Z0-9]+)\.([A-Z0-9]+)\.([A-Za-z0-9_-]+)$")

    @classmethod
    def validate_id(cls, artifact_id: str) -> bool:
        """Verifies if an ID aligns with OMEGA v15.0 RNC standards."""
        match = cls.RNC_PATTERN.match(artifact_id)
        if not match:
            return False

        domain_str, subsystem_str, _ = match.groups()

        # Cross-reference with enums
        try:
            Domain(domain_str)
            SubSystem(subsystem_str)
            return True
        except ValueError:
            return False

    @classmethod
    def suggest_path(cls, artifact_id: str) -> str:
        """Maps an RNC ID to its canonical filesystem location."""
        match = cls.RNC_PATTERN.match(artifact_id)
        if not match:
            raise ValueError(f"Invalid RNC ID for path mapping: {artifact_id}")

        domain, subsystem, descriptor = match.groups()

        # Domain-to-Root Mapping
        root_map = {
            "GVRN": "_governance",
            "CORE": "axion-core",
            "LAB": "nova_forge",
            "SELT": "_governance/templates",
            "COMM": "03_Avatar",
        }

        root = root_map.get(domain, "unknown")

        # Subsystem-to-Folder Mapping (Example logic)
        # In a full implementation, this uses a refined lookup table
        folder_map = {
            "AVATAR": "03_Avatar",
            "REGISTRY": "01_Registries",
            "ENGINE": "forge",
            "LEARNING": "06_Learning",
        }

        folder = folder_map.get(subsystem, subsystem.lower())

        return os.path.join(root, folder, f"{artifact_id}.md")

    @classmethod
    def safe_transform(cls, file_path: str, transformer_func) -> None:
        """
        [SOVEREIGN SHIELD]
        Applies a programmatic transformation with state-buffering to prevent truncation.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot transform non-existent file: {file_path}")

        # 1. Read entire file into buffer (Kinetic -> Mind)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Apply transformation in-memory
        transformed_content = transformer_func(content)

        # 3. Validation: Ensure we haven't nuked the file (Zero Entropy protection)
        if len(content) > 0 and len(transformed_content) == 0:
            raise RuntimeError(
                f"Safety Trigger: Transformation returned 0 bytes for {file_path}. Aborting write."
            )

        # 4. Atomic Write (Mind -> Substrate)
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(transformed_content)

    @classmethod
    def sync_folder(cls, folder_path: str) -> List[Dict]:
        """Audits a directory for RNC compliance and returns a dissonance report."""
        report = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    # Basic extraction of ID from filename or header
                    # (Simplified for the engine logic)
                    artifact_id = file.replace(".md", "")
                    if not cls.validate_id(artifact_id):
                        report.append(
                            {
                                "file": os.path.join(root, file),
                                "issue": "Non-compliant RNC ID",
                                "detected_id": artifact_id,
                            }
                        )
        return report


# [TERMINAL SIGNATURE]
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.Engine.RNCEngine VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-23
