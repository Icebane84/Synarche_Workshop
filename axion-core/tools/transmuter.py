"""HEPHAESTUS-TOOL-005: The Transmuter
Domain: ACT | State: ACTIVE | Version: v1.0
Objective: Migrate legacy artifact names (UMB/AOP) to Sovereign Standard (Context-First).
Synergy Link: DEPENDS_ON -> src/logic/enums.py.
"""

import argparse
import csv
import os
import re
from pathlib import Path

# Constants
GOVERNANCE_ROOT = r"C:\Users\Chris\Synarche_Workspace\_governance"
IGNORE_DIRS = [".git", ".obsidian", "Archive", "Template"]

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
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.proposals = []
        self.redirects = []

    def scan_and_plan(self):
        """Walk the directory and generate renaming proposals."""
        print(f"🔮 Scanning {GOVERNANCE_ROOT} for legacy artifacts...")

        for root, dirs, files in os.walk(GOVERNANCE_ROOT):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if not file.endswith(".md"):
                    continue

                self.analyze_file(os.path.join(root, file))

        self.save_plan()

    def analyze_file(self, file_path: str):
        """Analyze a single file and propose a new name."""
        filename = os.path.basename(file_path)

        # Regex to capture Legacy components: PREFIX-SUB-ID_Name_ver.md
        # e.g., UMB-SGM-001_SystemGovernance_v11.0.md
        match = re.match(r"^([A-Z]+)-([A-Z]+)-(\d{3})_(.*?)_(v.*)\.md$", filename)

        if not match:
            # Try looser match if strict fails (for less standardized files)
            match = re.match(r"^([A-Z]+)-([A-Z]+)-(\d{3})(.*)\.md$", filename)

        if match:
            prefix, sub, id_num, name_part, ver_part = (
                match.groups() if len(match.groups()) == 5 else (*match.groups(), "")
            )

            # Consult the Map
            new_domain, new_func = self.resolve_mapping(prefix, sub)

            # Construct New Name: [DOMAIN].[FUNC].[ID]
            # We keep the numeric ID for continuity, or should we?
            # Creating a clean Sovereign ID.

            # Clean up the name part (remove versions if duplicated, etc)
            name_part.replace("_", ".")

            # Standard: [DOMAIN].[FUNC].001.md (Simple)
            # OR User's Style: GVRN.ID.Standard.md

            # Start with a safe conversion: GVRN.REG.001_Name.md?
            # Let's align with the GVRN.ID.Standard example: [PARENT].[FUNC].[SEQUENCE]
            # BUT the user also uses [PARENT].[NAME] for singular artifacts like GVRN.ID.Standard.

            # Heuristic: If sub is mapped, use it.
            # UMB-SGM-001 -> GVRN.GOV.SGM.md ? No.

            # Let's try to map strictly to the requested standard.
            # GVRN.REG.Master.md

            f"{new_domain}.{new_func}.{sub.title()}"
            # Example: UMB-SGM-001 -> GVRN.GOV.Sgm.md?
            # User example: SYNG.PROT.Link

            # Let's propose a "Reasonable Best Guess"
            new_filename = f"{new_domain}.{new_func}.{name_part.strip('_')}.md"

            # Store Proposal
            self.proposals.append(
                {
                    "original_path": file_path,
                    "original_name": filename,
                    "new_name": new_filename,
                    "new_id": f"{new_domain}.{new_func}.{id_num}",  # Internal ID tracking
                    "confidence": "High",
                }
            )

    def resolve_mapping(self, prefix: str, sub: str):
        """Resolve the (Domain, Function) tuple from legacy prefix/sub."""
        pmap = PREFIX_MAP.get(prefix)
        if not pmap:
            return ("UNCERTAIN", "UNK")

        overrides = pmap.get("overrides", {})
        if sub in overrides:
            return overrides[sub]

        return pmap["default"]

    def save_plan(self):
        """Save proposals to CSV."""
        output_file = Path("renaming_plan.csv")
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["original_name", "new_name", "confidence", "original_path"],
            )
            writer.writeheader()
            for p in self.proposals:
                writer.writerow({k: v for k, v in p.items() if k != "new_id"})

        print(f"\n✨ Plan Generated: {len(self.proposals)} proposed renames.")
        print(f"📄 Review: {output_file.absolute()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transition artifacts to Sovereign Naming."
    )
    parser.add_argument("--dry-run", action="store_true", help="Generate plan only.")
    args = parser.parse_args()

    transmuter = Transmuter(dry_run=args.dry_run)
    transmuter.scan_and_plan()
