"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-TRANSMUTER-001`                | The Sovereign ID. |
| **Official Name** | `transmuter.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Ethos**         | **Crystalline Structure**      | Forging crystalline wisdom from entropy. [UEB-GAE-001] |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

"""
HEPHAESTUS-TOOL-005: The Transmuter (Axion Persona)
Domain: ACT | State: ACTIVE | Version: v13.0
Objective: Migrate legacy artifact names (UMB/AOP) to Sovereign Standard (Context-First).
Synergy Link: DEPENDS_ON -> src/logic/enums.py
"""

import argparse
import csv
import logging
import os
import re
from pathlib import Path
from typing import Any

# Configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
GOVERNANCE_ROOT = r"C:\Users\Chris\Synarche_Workspace\_governance"
IGNORE_DIRS = [
    ".git",
    ".obsidian",
    "Archive",
    "Template",
    "99_Archives",
    "00_Codex",
    "templates",
]

# The Rosetta Map (Mapping Logic)
# (Legacy Prefix) -> (Target Domain, Function Tag)
PREFIX_MAP = {
    "UMB": {
        "default": ("GVRN", "REG"),  # UMB usually maps to Registry/Blueprint
        "overrides": {
            "SGM": ("GVRN", "GOV"),  # System Governance Model -> Governance
            "MAP": ("GVRN", "PROT"),  # Musashi Protocol -> Protocol
            "ESF": ("GVRN", "STD"),  # Episemantic Framework -> Standard
            "OSLM": ("GVRN", "REG"),  # Omni-Log -> Registry
            "CSE": ("SYNG", "CORE"),  # Coherent Synthesis Engine -> Core
        },
    },
    "AOP": {
        "default": ("SYNG", "PROT"),  # AOP usually maps to Operational Protocol
        "overrides": {
            "CC": ("COG", "CORE"),  # Crystalline Cognition -> Cognition Core
            "ASL": ("SYNG", "PROT"),  # Synergistic Linking -> Protocol
            "MAR": ("GVRN", "REG"),  # Master Registry -> Registry
        },
    },
    "CODEX": {
        "default": ("CORE", "LAW"),  # Codex -> Law
        "overrides": {},
    },
    "GUCA": {
        "default": (
            "GVRN",
            "ACT",
        ),  # Global Universal Command Arch -> Governance Actuator
        "overrides": {},
    },
    "CMD": {
        "default": ("GVRN", "ACT"),  # Command -> Governance Actuator
        "overrides": {},
    },
    "UEB": {
        "default": (
            "ARCH",
            "BLUE",
        ),  # Universal Ecosystem Blueprint -> Architecture Blueprint
        "overrides": {},
    },
    "SELT": {
        "default": ("GVRN", "LOG"),  # System Event Log -> Governance Log
        "overrides": {},
    },
    "METRIC": {
        "default": ("GVRN", "METRIC"),  # Metric -> Governance Metric
        "overrides": {},
    },
}


class Transmuter:
    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        self.proposals: list[dict[str, Any]] = []
        self.redirects: list[str] = []

    def scan_and_plan(
        self, rationale: str = "Alignment with OMEGA v14.0 Semantic Standards."
    ) -> None:
        """Walk the directory and generate renaming proposals."""
        logger.info(f"[AXION] 🔮 Scanning {GOVERNANCE_ROOT} for legacy artifacts...")

        for root, dirs, files in os.walk(GOVERNANCE_ROOT):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if not file.endswith(".md"):
                    continue

                self.analyze_file(os.path.join(root, file))

        self.save_plan()

    def analyze_file(self, file_path: str) -> None:
        """Analyze a single file and propose a new name."""
        filename = os.path.basename(file_path)

        # Regex to capture Legacy components: PREFIX-SUB-ID_Name_ver.md
        # e.g., UMB-SGM-001_SystemGovernance_v11.0.md
        match = re.match(r"^([A-Z]+)-([A-Z]+)-(\d{3})_(.*?)_(v.*)\.md$", filename)

        if not match:
            # Try looser match if strict fails (for less standardized files)
            match = re.match(r"^([A-Z]+)-([A-Z]+)-(\d{3})(.*)\.md$", filename)

        if match:
            prefix, sub, id_num, name_part, _ = (
                match.groups() if len(match.groups()) == 5 else (*match.groups(), "")
            )

            # Consult the Map
            new_domain, new_func = self.resolve_mapping(prefix, sub)

            # Construct New Name: [DOMAIN].[FUNC].[ID]
            # We keep the numeric ID for continuity
            new_filename = f"{new_domain}.{new_func}.{name_part.strip('_')}.md"

            self.proposals.append(
                {
                    "original_path": file_path,
                    "original_name": filename,
                    "new_name": new_filename,
                    "new_id": f"{new_domain}.{new_func}.{id_num}",  # Internal ID tracking
                    "confidence": "High",
                    "rationale": rationale,
                }
            )

    def resolve_mapping(self, prefix: str, sub: str) -> tuple[str, str]:
        """Resolve the (Domain, Function) tuple from legacy prefix/sub."""
        pmap = PREFIX_MAP.get(prefix)
        if not pmap:
            return ("UNCERTAIN", "UNK")

        overrides = pmap.get("overrides", {})
        if sub in overrides:
            return overrides[sub]  # type: ignore

        return pmap["default"]  # type: ignore

    def save_plan(self) -> None:
        """Save proposals to CSV."""
        output_file = Path("renaming_plan.csv")
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "original_name",
                    "new_name",
                    "confidence",
                    "original_path",
                    "rationale",
                ],
            )
            writer.writeheader()
            for p in self.proposals:
                writer.writerow({k: v for k, v in p.items() if k != "new_id"})

        logger.info(
            f"\n[AXION] ✨ Plan Generated: {len(self.proposals)} proposed renames."
        )
        logger.info(f"[AXION] 📄 Review: {output_file.absolute()}")

    def execute_plan(self, plan_file: str = "renaming_plan.csv") -> None:
        """Execute the renaming plan from the CSV."""
        if not os.path.exists(plan_file):
            logger.error(f"[AXION] ❌ Plan file not found: {plan_file}")
            return

        logger.info("\n=== THE FORGE OF AXION: TRANSMUTATION PROTOCOL ===")
        logger.info(
            '> "Entropy is the enemy. Structure is the shield. Coherence is the sword." — UEB-GOC-001\n'
        )
        logger.info(f"[AXION] 🚀 Initiating Transmutation from: {plan_file}")
        logger.warning("[AXION] ⚠️  WARNING: This will rename files on disk.")

        success_count = 0
        skip_count = 0
        error_count = 0

        with open(plan_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            logger.info(
                f"📋 Found {len(rows)} candidates. Processing High Confidence items..."
            )

            for row in rows:
                original_path = row["original_path"]
                new_name = row["new_name"]
                confidence = row["confidence"]

                if confidence != "High":
                    logger.info(
                        f"⏭️  Skipping (Low Confidence): {row['original_name']}"
                    )
                    skip_count += 1
                    continue

                # Verify file still exists
                if not os.path.exists(original_path):
                    logger.error(f"❌ Error: Source file missing: {original_path}")
                    error_count += 1
                    continue

                # Construct new path
                dir_name = os.path.dirname(original_path)
                new_path = os.path.join(dir_name, new_name)

                # Prevent overwrite
                if os.path.exists(new_path):
                    logger.warning(f"⚠️  Skipping: Target exists: {new_name}")
                    skip_count += 1
                    continue

                try:
                    # RENAME
                    os.rename(original_path, new_path)
                    logger.info(
                        f"[AXION] ✅ Transmuted: {row['original_name']} -> {new_name} (Rationale: {row.get('rationale', 'Alignment')})"
                    )
                    success_count += 1
                except Exception as e:
                    logger.error(
                        f"[AXION] ❌ Failed to rename {row['original_name']}: {e}"
                    )
                    error_count += 1

        logger.info("\n[AXION] ✨ Transmutation Complete.")
        logger.info(f"[AXION] ✅ Success: {success_count}")
        logger.info(f"[AXION] ⏭️  Skipped: {skip_count}")
        logger.info(f"[AXION] ❌ Errors: {error_count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transition artifacts to Sovereign Naming."
    )
    parser.add_argument("--dry-run", action="store_true", help="Generate plan only.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the renaming plan from renaming_plan.csv.",
    )
    parser.add_argument(
        "--rationale",
        help="The Architectural Rationale (The 'Why') for this transmutation.",
    )
    args = parser.parse_args()

    transmuter = Transmuter(dry_run=args.dry_run)
    rationale = (
        args.rationale
        if args.rationale
        else "Alignment with OMEGA v14.0 Semantic Standards."
    )

    if args.execute:
        transmuter.execute_plan()
    else:
        transmuter.scan_and_plan(rationale)


if __name__ == "__main__":
    main()
