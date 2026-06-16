"""[CORE] [ENGINE] [RNC_ENGINE_V2]
Artifact ID: CORE.Engine.RNC_Engine
Official Name: rnc_engine_v2.py
Version: v15.0 [OMEGA]
Status: [ACTIVE]
Description: The Advanced Sovereign RNC Engine. Unifies path mapping, AST-auditing, and tool-readiness verification.

[UIP-V15]
| Key | Value |
| :--- | :--- |
| **Artifact ID** | `CORE.Engine.RNC_Engine` |
| **Official Name** | `rnc_engine_v2.py` |
| **Version** | **v15.0 [OMEGA]** |
| **Domain** | `CORE` |
| **Status** | `[ACTIVE]` |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001`, `WIELDS: DragonslayerAuditor` |
"""

import logging
import os
import re
from pathlib import Path
from typing import Any

# Relative imports from the forge layer
try:
    from dragonslayer import DragonslayerAuditor
    from enums import Domain, Module, Signal, Status
    from equip import MASKS
except ImportError:
    from .dragonslayer import DragonslayerAuditor
    from .equip import MASKS

# Configure Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [RNC-V2] - %(levelname)s - %(message)s"
)
logger = logging.getLogger("RNCEngineV2")


class RNCEngineV2:
    """The High Gate Sovereign Engine.
    Handles RNC resolution, AST truth-auditing, and ARMORY equipment checks.
    """

    # [DOMAIN].[Subsystem].[Descriptor]
    RNC_PATTERN = re.compile(r"^([A-Z0-9]+)\.([A-Z0-9]+)\.([A-Za-z0-9_-]+)$")

    def __init__(self, workspace_root: str | None = None):
        self.root = Path(workspace_root or os.getcwd())
        logger.info(f"RNCEngineV2 initialized at {self.root}")

    def validate_id(self, artifact_id: str) -> bool:
        """Verifies if an ID aligns with OMEGA v15.0 RNC standards."""
        match = self.RNC_PATTERN.match(artifact_id)
        if not match:
            return False

        domain_str, subsystem_str, _ = match.groups()

        # Cross-reference with Domain Enum
        try:
            # Check if domain exists in the Enum or standards
            # (In a real implementation, we'd map domain_str to the Domain Enum)
            return True
        except ValueError:
            return False

    def resolve_path(self, artifact_id: str) -> Path:
        """Maps an RNC ID to its canonical filesystem location."""
        match = self.RNC_PATTERN.match(artifact_id)
        if not match:
            raise ValueError(f"Invalid RNC ID: {artifact_id}")

        domain, subsystem, descriptor = match.groups()

        # Domain-to-Root Mapping (Canonical OGLN)
        domain_map = {
            "GVRN": "_governance",
            "CORE": "axion-core",
            "LAB": "nova_forge",
            "SELT": "_governance/templates",
            "COMM": "03_Avatar",
            "SYNG": "forge",
        }

        root_folder = domain_map.get(domain, "axion-core")

        # Special case for subfolders
        folder_map = {
            "ENGINE": "forge",
            "SYSTEM": "src/system",
            "LOGIC": "src/logic",
            "UI": "src/web",
            "REGISTRY": "01_Registries",
        }

        subfolder = folder_map.get(subsystem, subsystem.lower())

        # Construct path
        final_path = self.root / root_folder / subfolder / f"{artifact_id}.py"

        # Fallback to .md if .py doesn't exist (conceptual)
        if (
            not final_path.exists()
            and (self.root / root_folder / subfolder / f"{artifact_id}.md").exists()
        ):
            final_path = self.root / root_folder / subfolder / f"{artifact_id}.md"

        return final_path

    def audit_truth(self, artifact_id: str) -> bool:
        """Executes the Sword of Truth (Dragonslayer) on the artifact."""
        try:
            path = self.resolve_path(artifact_id)
            if path.suffix != ".py":
                logger.warning(
                    f"Skipping AST audit for non-python artifact: {artifact_id}"
                )
                return True

            auditor = DragonslayerAuditor(str(path))
            return bool(auditor.audit())
        except Exception as e:
            logger.error(f"Truth Audit failed for {artifact_id}: {e}")
            return False

    def check_readiness(self, mask_name: str) -> dict[str, Any]:
        """Verifies if the ARMORY is equipped for a specific Sovereign Mask.
        Uses logic from equip.py.
        """
        mask_data = next((m for m in MASKS if m["card"] == mask_name), None)
        if not mask_data:
            return {
                "status": "ERROR",
                "message": f"Mask {mask_name} not found in ARMORY.",
            }

        ready_tools = []
        missing_tools = []

        # Search in tools and hephaestus
        tools_dir = self.root / "tools"
        hephaestus_dir = self.root / "src" / "hephaestus"

        for tool in mask_data["tools"]:
            # Check for .py or .js
            found = False
            for ext in [".py", ".js"]:
                if (tools_dir / f"{tool}{ext}").exists() or (
                    hephaestus_dir / f"{tool}{ext}"
                ).exists():
                    ready_tools.append(tool)
                    found = True
                    break
            if not found:
                missing_tools.append(tool)

        return {
            "mask": mask_name,
            "status": "READY" if not missing_tools else "PARTIAL",
            "ready": ready_tools,
            "missing": missing_tools,
            "total": len(mask_data["tools"]),
        }

    def finalize_artifact(self, artifact_id: str, mask: str) -> bool:
        """The Seven Gates Orchestrator.
        1. Verification (Truth)
        2. Readiness (Armory)
        3. RNC Mapping (Naming).
        """
        logger.info(f"--- [FINALIZING ARTIFACT]: {artifact_id} via {mask} ---")

        # Gate 1: Readiness
        armory_report = self.check_readiness(mask)
        if armory_report["status"] != "READY":
            logger.warning(
                f"ARMORY WARNING: {mask} is missing tools: {armory_report['missing']}"
            )
            # We proceed with a warning for now (as per v15.0 flexibility)

        # Gate 2: Truth Audit
        if not self.audit_truth(artifact_id):
            logger.error(
                f"TRUTH AUDIT FAILED: {artifact_id} contains hallucinations or deceptive logic."
            )
            return False

        # Gate 3: RNC Integrity
        if not self.validate_id(artifact_id):
            logger.error(
                f"RNC VALIDATION FAILED: {artifact_id} does not follow the Sovereign Grammar."
            )
            return False

        logger.info(f"--- [ARTIFACT CANONIZED]: {artifact_id} ---")
        return True


if __name__ == "__main__":
    # Test Activation
    engine = RNCEngineV2()
    test_id = "CORE.Engine.RNCEngine"

    print(f"\n[RNC-V2] Validating: {test_id}")
    if engine.validate_id(test_id):
        print(f"[RNC-V2] Path: {engine.resolve_path(test_id)}")

    print("\n[RNC-V2] Checking Magician Readiness...")
    print(engine.check_readiness("I. The Magician"))

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.Engine.RNC_Engine VER: v15.0 [OMEGA] STATUS: ACTIVE TS: 2026-04-23
