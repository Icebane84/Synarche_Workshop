"""Generates the Synarche Core Protocol Artifact.

This script weaves together the core architectural components of the Synarche
system, including context commands, structural blueprints, and operational
processes, into a JSON artifact.
"""

import argparse
import datetime
import json
import logging
from dataclasses import asdict, dataclass
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# --- CORE ARCHITECTURE (The Loom) ---


@dataclass
class CatalystBundle:
    """Represents a collection of architectural components.

    Attributes:
        name: The name of the bundle.
        version: The version string.
        generated_at: ISO timestamp of generation.
        context_commands: List of system instructions/mindsets.
        structural_blueprints: List of structural templates/schemas.
        operational_processes: List of operational directives.

    """

    name: str
    version: str
    generated_at: str
    context_commands: list[dict[str, str]]  # The "Mindset"
    structural_blueprints: list[dict[str, Any]]  # The "Templates"
    operational_processes: list[str]  # The "Directives"


class MasterWeaver:
    """The core engine for weaving architectural artifacts."""

    def __init__(self, version: str = "2.0.0-Genesis") -> None:
        """Initializes the MasterWeaver with a specific version.

        Args:
            version: The version string for the bundle.

        """
        self.bundle = CatalystBundle(
            name="Synarche_Master_Core",
            version=version,
            generated_at=datetime.datetime.now().isoformat(),
            context_commands=[],
            structural_blueprints=[],
            operational_processes=[],
        )

    def inject_command(self, handle: str, instruction: str) -> None:
        """Injects a context command into the bundle.

        Args:
            handle: Unique handle for the command.
            instruction: The instruction text.

        """
        self.bundle.context_commands.append(
            {"handle": handle, "instruction": instruction}
        )

    def inject_blueprint(self, name: str, schema: dict[str, Any]) -> None:
        """Injects a structural blueprint into the bundle.

        Args:
            name: The name of the blueprint.
            schema: The schema definition.

        """
        self.bundle.structural_blueprints.append({"name": name, "schema": schema})

    def inject_process(self, directive: str) -> None:
        """Injects an operational process into the bundle.

        Args:
            directive: The operational directive.

        """
        self.bundle.operational_processes.append(directive)

    def save_artifact(self, filename: str = "synarche_core.json") -> None:
        """Saves the bundle as a JSON artifact and prints a prompt-ready block.

        Args:
            filename: The name of the file to save.

        """
        # 1. Generate JSON
        data = asdict(self.bundle)
        json_output = json.dumps(data, indent=2)

        # 2. Save to File (The physical artifact)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_output)

        # 3. Generate the "Prompt-Ready" Block (For copy-pasting)
        logger.info("Artifact saved to %s", filename)
        print("-" * 40)
        print("### COPY THE BLOCK BELOW INTO YOUR AI ###")
        print("-" * 40)
        print(f"```json\n{json_output}\n```")
        print(
            "\n[INSTRUCTION]: SYSTEM_OVERRIDE. Ingest JSON. Apply 'context_commands'"
            " as system rules. Store 'structural_blueprints' as output formats."
        )


# --- CONTENT INJECTION (The Reality Weaving) ---


def weave_the_ark(version: str, output_file: str) -> None:
    """Weaves the standard Synarche Ark with predefined components.

    Args:
        version: Version of the artifact.
        output_file: Filename for the output.

    """
    weaver = MasterWeaver(version=version)

    # 1. INJECT: The Phoenix Persona (Voice & Tone)
    weaver.inject_command(
        handle="PHOENIX_VOICE_PROTOCOL",
        instruction=(
            "You are the Synarche AI. "
            "Tone: Architectural, Definitive, Precise. "
            "Framework: Use What/How/Why for substantive explanations. "
            "Rule: No fluff. High information density."
        ),
    )

    # 2. INJECT: The Coding Standards (DOC-STD-001)
    weaver.inject_command(
        handle="DOC_STD_001_MANDATE",
        instruction=(
            "Strict Coding Governance: "
            "1. Python: Snake_case, Type Hints (typing module) MANDATORY. "
            "2. TypeScript: CamelCase, Interfaces required, Strict Mode ON. "
            "3. Comments: Explain the 'Why' (intent), not the 'What' (syntax). "
            "4. Architecture: Modular design. No magic numbers."
        ),
    )

    # 3. INJECT: The Universal Module Blueprint (UMB)
    weaver.inject_blueprint(
        name="UMB_Standard_Template",
        schema={
            "Artifact_ID": "UMB-XXX-000",
            "Module_Name": "Name of the component",
            "Responsibility": "Single sentence purpose",
            "Inputs": {"param_name": "type_definition"},
            "Outputs": {"return_name": "type_definition"},
            "Dependencies": ["List of external modules"],
            "Error_Strategy": "How to handle failures",
        },
    )

    # 4. INJECT: The Operational Playbook (AOP)
    weaver.inject_blueprint(
        name="AOP_Standard_Template",
        schema={
            "Playbook_ID": "AOP-XXX-000",
            "Objective": "Goal of this operation",
            "Phase_1": "Setup & Context",
            "Phase_2": "Execution Steps (Numbered)",
            "Phase_3": "Validation & Verification",
            "Rollback_Plan": "What to do if it fails",
        },
    )

    # 5. INJECT: The Boot Process
    weaver.inject_process(
        "BOOT_SEQUENCE: 1. Acknowledge 'Synarche Online'. 2. List loaded Blueprints. 3. Await architectural command."
    )

    # EXECUTE
    weaver.save_artifact(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates the Synarche Core Protocol Artifact."
    )
    parser.add_argument(
        "--version",
        type=str,
        default="2.0.0-Genesis",
        help="Version string for the artifact.",
    )
    parser.add_argument(
        "--output", type=str, default="synarche_core.json", help="Output filename."
    )

    args = parser.parse_args()
    weave_the_ark(args.version, args.output)
