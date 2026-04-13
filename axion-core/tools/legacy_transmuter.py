"""
legacy_transmuter.py
Role: The Alchemist (Renaming Engine)
Domain: GVRN
Description: Scans for legacy UMB/AOP artifacts, maps them to Sovereign IDs, renames files, and updates headers.
"""

import csv
import datetime
import os
import re
from pathlib import Path

# --- CONFIGURATION ---
ROOT_DIR = r"c:\Users\Chris\Synarche_Workspace\_governance"
REGISTRY_PATH = r"c:\Users\Chris\Synarche_Workspace\_governance\01_Registries\GVRN.Registry.Redirects.md"
DRY_RUN_OUTPUT = "transmutation_plan.csv"

# --- MAPPING RULES (Heuristics) ---
# Format: "SUBSTRING": ("DOMAIN", "FUNCTION")
MAPPING_TABLE = {
    # GVRN (Governance)
    "SGM": ("GVRN", "Gov.Module"),
    "AUDIT": ("GVRN", "Protocol.Audit"),
    "SENTINEL": ("GVRN", "Sentinel.Scan"),
    "PRESENTATION": ("GVRN", "Protocol.Presentation"),
    "SCAFFOLDING": ("GVRN", "Protocol.Scaffolding"),
    "LATTICE": ("GVRN", "Axiomatic.Lattice"),
    "REGISTRY": ("GVRN", "Registry"),
    "CATALOG": ("GVRN", "Catalog"),
    # SYNG (Synergy)
    "ENGINE": ("SYNG", "Engine"),
    "LOOM": ("SYNG", "Loom"),
    "SYNERGY": ("SYNG", "Synergy"),
    "DNA": ("SYNG", "DNA"),
    # ARCH (Architecture)
    "ARCH": ("ARCH", "Architecture"),
    "SPINE": ("ARCH", "Spine"),
    # COG (Cognition)
    "COG": ("COG", "Cognition"),
    "CONTEXT": ("COG", "Context"),
}


def generate_sovereign_id(filename: str) -> str:
    """
    Generates a Sovereign ID based on filename heuristics.
    Legacy: UMB-SGM-001_StandardizedGovernanceModule_v11.0.md
    Target: GVRN.Gov.Module.md (Basename) -> ID: GVRN.Gov.Module
    """
    name_part = filename
    if "_" in filename:
        name_part = filename.split("_", maxsplit=1)[0]  # UMB-SGM-001

    # Clean Prefix
    clean_name = name_part.replace("UMB-", "").replace("AOP-", "").upper()

    # Heuristic Match
    domain = "GVRN"  # Default
    function = "Legacy.Unknown"

    for key, (dom, func) in MAPPING_TABLE.items():
        if key in clean_name:
            domain = dom
            function = func
            break

    # Fallback to direct translation if no map
    if function == "Legacy.Unknown":
        parts = clean_name.split("-")
        if len(parts) >= 2:
            function = f"{parts[0]}.{parts[1]}"
        else:
            function = clean_name

    return f"{domain}.{function}"


def scan_and_plan(root_dir: str):
    """Scans directory for Legacy files and generates a plan."""
    plan = []
    print(f"Scanning {root_dir}...")

    for root, dirs, files in os.walk(root_dir):
        # Skip Archive
        if "_archive" in root or "99_Archives" in root or ".git" in root:
            continue

        for file in files:
            if not file.endswith(".md"):
                continue

            # Check for Legacy Prefix
            if file.startswith("UMB-") or file.startswith("AOP-") or file.startswith("CODEX-"):
                full_path = Path(root) / file
                legacy_id = file.split("_")[0] if "_" in file else file.replace(".md", "")

                new_id = generate_sovereign_id(file)
                new_filename = f"{new_id}.md"
                new_full_path = Path(root) / new_filename

                plan.append(
                    {
                        "Legacy File": file,
                        "Legacy ID": legacy_id,
                        "New ID": new_id,
                        "New Filename": new_filename,
                        "Path": str(full_path),
                        "New Path": str(new_full_path),
                    }
                )

    return plan


def execute_transmutation(plan):
    """Executes the renaming and registry update."""
    redirects = []

    for item in plan:
        old_path = Path(item["Path"])
        new_path = Path(item["New Path"])

        if not old_path.exists():
            print(f"Skipping (Not Found): {old_path}")
            continue

        print(f"Renaming: {item['Legacy File']} -> {item['New Filename']}")

        try:
            # 1. Rename File
            os.rename(old_path, new_path)

            # 2. Update Header (Naive Regex Replace for now, can be improved)
            with open(new_path, encoding="utf-8") as f:
                content = f.read()

            # update artifact id in line
            # Assuming standard UIP table format or similar
            # For this batch, strictly file renaming is safer, header update helps but might be fragile specific to each file.
            # We will do a generic replace of the Artifact ID if found.

            new_content = re.sub(
                r"\|\s*\*\*Artifact ID\*\*\s*\|\s*`.*?`", f"| **Artifact ID** | `{item['New ID']}`", content
            )

            # Update Version to v13.0 [ASCENDED] if not present? Maybe too aggressive.
            # Let's just update the ID for now.

            with open(new_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            redirects.append(
                f"| {datetime.date.today()} | `{item['Legacy ID']}` | `{item['New ID']}` | {item['New ID'].split('.')[0]} | [TRANSMUTED] |"
            )

        except Exception as e:
            print(f"Error processing {old_path}: {e}")

    # 3. Append to Registry
    if redirects:
        with open(REGISTRY_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(redirects))
        print(f"Updated Redirect Registry with {len(redirects)} entries.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Execute the transmutation")
    args = parser.parse_args()

    plan_data = scan_and_plan(ROOT_DIR)

    # Save Plan to CSV
    keys = ["Legacy File", "Legacy ID", "New ID", "New Filename", "Path", "New Path"]
    with open(DRY_RUN_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(plan_data)

    print(f"Generated Plan: {len(plan_data)} items. Saved to {DRY_RUN_OUTPUT}")

    if args.execute:
        print("EXECUTING BATCH FORGE...")
        execute_transmutation(plan_data)
    else:
        print("Dry Run Complete. Use --execute to apply.")
