"""GVRN.Protocol.Assembler (AOP-DTS-001)
Domain: AOP | State: ACTIVE | Version: v13.0
Objective: Dynamically assemble v13.0 Omega Artifacts from SELT Building Blocks.
"""

import logging
import os
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console
from rich.logging import RichHandler

# Configure Logging (Sentinel Style)
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("Assembler")
console = Console()

# Constants
BLOCKS_DIR = Path(__file__).parent.parent / "templates" / "blocks"
OUTPUT_DIR = Path(os.getcwd())  # Default to current execution dir


class Assembler:
    """The Engine of the Dynamic Template Ecosystem.
    Fetches SELTs -> Injects Vars -> Assembles Artifact.
    """

    def __init__(self, template_dir: Path = BLOCKS_DIR) -> None:
        self.template_dir = template_dir
        if not self.template_dir.exists():
            logger.error(f"❌ Template Directory Not Found: {self.template_dir}")
            raise FileNotFoundError(f"Template directory {self.template_dir} missing.")

        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        logger.info(f"🔧 Assembler Initialized (Source: {self.template_dir})")

    def fetch_selt(self, selt_name: str) -> Template:
        """Retrieves a specific SELT (Structural Element Template)."""
        try:
            return self.env.get_template(f"{selt_name}.md")
        except Exception as e:
            logger.error(f"❌ Failed to fetch SELT: {selt_name}")
            raise e

    def forge_artifact(
        self, context: dict[str, Any], output_path: Path | None = None
    ) -> str:
        """Assembles the Sovereign Artifact using the 6-Block Omega Schema.
        Supports optional blocks via context flags.
        """
        logger.info(f"🔨 Forging Artifact: {context.get('filename', 'Unknown')}")

        # 1. Define the Assembly Sequence (The Lawgiver's Recipe)
        # Base Omega Template
        assembly_sequence = [
            "SELT-HEADER-UIP-001",  # Block A: Identity
            "SELT-ETHOS-IDM-001",  # Block B: Ethos
            "SELT-SPINE-AXIOM",  # Block C: Cognitive Spine
        ]

        # [Injection Point: Content Body]
        # (Handled strictly via list construction below)

        # Optional: RPG Block
        if context.get("include_rpg", False):
            assembly_sequence.append("SELT-RPG-INT-001")

        # Standard Core Sequence continues
        assembly_sequence.append("SELT-GATE-CIV")  # Block D: Integrity Gate
        assembly_sequence.append("SELT-SYNERGY-LOOM")  # Block E: Synergy Loom

        # Optional: Governance Finalization
        if context.get("include_governance", False):
            assembly_sequence.append("SELT-GOVERNANCE-FIN-001")

        # Block F: Omni-Anchor (Always Last)
        assembly_sequence.append("SELT-ANCHOR-OMNI")

        # 2. Render each Block
        assembled_content = []

        for block_name in assembly_sequence:
            # Special Handling for Content Injection
            if block_name == "SELT-GATE-CIV":
                # Inject Content Body BEFORE the Gate (between Spine and Gate)
                content_body = context.get(
                    "content_body", "\n<!-- Content Placeholder -->\n"
                )
                assembled_content.append(content_body)

            # Render the Block
            block_content = self.fetch_selt(block_name).render(context)
            assembled_content.append(block_content)

        # 3. Final Concatenation
        full_artifact = "\n\n".join(assembled_content)

        # 4. Output
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_artifact)
            logger.info(f"✅ Artifact solidified at: {output_path}")

        return full_artifact


if __name__ == "__main__":
    # Test Context
    test_context = {
        "filename": "GVRN.Test.Artifact.md",
        "domain": "GVRN",
        "evolution": "Omega Ascension",
        "signal": "OMEGA",
        "date": "2026-02-04",
        "status": "[ACTIVE]",
        "tags": "Test, Protocol",
        "criticality": "Low",
        "artifact_id": "GVRN.Test.Artifact",
        "legacy_id": "NULL",
        "version": "v13.0 [OMEGA]",
        "celestial_class": "[MOON]",
        "relations": "GOVERNED_BY: CORE-CODEX-001",
        "quote": "A test is but a question demanded of reality.",
        "mandate": "To verify the Assembler Engine.",
        "law": "Integrity above all.",
        "state_mind": "[IDLE]",
        "processor_id": "CPU-001",
        "state_memory": "[ALLOCATED]",
        "loom_cluster": "Cluster-A",
        "state_law": "[COMPLIANT]",
        "codex_law_id": "LAW-001",
        "state_index": "[PENDING]",
        "prs_vertex": "Vertex-Z",
        "state_evolution": "[ACQUIRING]",
        "phoenix_form": "Stage-1",
        "audit_status": "PASS",
        "content_body": "## Test Content\nThis is a generated test artifact.",
        # RPG Hooks
        "include_rpg": True,
        "xp_reward": "500",
        "skill_tree": "System Architecture",
        "achievement_id": "ACH-FORGE-MASTER",
        "quest_giver_id": "GVRN-AI-01",
        # Governance Hooks
        "include_governance": True,
    }

    assembler = Assembler()
    print(assembler.forge_artifact(test_context))
