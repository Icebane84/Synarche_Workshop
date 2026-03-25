"""
IDENTIFICATION: TOOL-LAB-ID-ALIGN
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24
"""

import argparse
import os
import re
from pathlib import Path

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


class IdentityAligner:
    def __init__(
        self, dry_run: bool = True, log_file: str = None, targets: list[str] = None
    ):
        self.dry_run = dry_run
        self.log_file = log_file
        self.targets = targets or []
        self.stats = {"scanned": 0, "aligned": 0, "skipped": 0, "errors": 0}

    def scan_and_align(self):
        if self.targets:
            print(f"🔮 Scanning {len(self.targets)} specific targets...")
            for target in self.targets:
                if os.path.isfile(target):
                    self.process_file(target)
                elif os.path.isdir(target):
                    self.scan_directory(target)
        else:
            print(f"🔮 Scanning {GOVERNANCE_ROOT} for Identity Drift...")
            self.scan_directory(GOVERNANCE_ROOT)

        self.report()

    def scan_directory(self, directory: str):
        for root, dirs, files in os.walk(directory):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if not file.endswith(".md"):
                    continue

                self.process_file(os.path.join(root, file))

    def process_file(self, filepath: str):
        self.stats["scanned"] += 1
        filename = os.path.basename(filepath)

        # 1. Derive Expected ID from Filename
        # Sovereign Standard: DOMAIN.FUNC.Name.md -> ID: DOMAIN.FUNC.Name
        if not re.match(r"^[A-Z]+\.[A-Z]+\..+\.md$", filename):
            # perform loose check for renamed files
            # If it doesn't look like a Sovereign file, skip it or log it?
            # We only want to fix files that HAVE been renamed to the new standard.
            # print(f"  Start skip: {filename}")
            return

        expected_id = Path(filepath).stem  # Removes .md

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            # 2. Check current Internal ID
            # Regex to find | **Artifact ID** | `OLD-ID` |
            # We handle variations in whitespace and bolding
            id_pattern = r"(\|\s*\**Artifact ID\**\s*\|\s*`?)([^`|\n]+)(`?\s*\|)"
            name_pattern = r"(\|\s*\**Official Name\**\s*\|\s*`?)([^`|\n]+)(`?\s*\|)"

            # Check if alignment is needed
            current_id_match = re.search(id_pattern, content)
            current_name_match = re.search(name_pattern, content)

            current_id = current_id_match.group(2) if current_id_match else "MISSING"
            current_name = (
                current_name_match.group(2) if current_name_match else "MISSING"
            )

            needs_update = False
            if current_id != expected_id:
                needs_update = True

            if current_name != filename:
                needs_update = True

            if not needs_update:
                return

            log_message = f"- **Aligning:** `{filename}`\n  - **ID:** `{current_id}` -> `{expected_id}`\n  - **Name:** `{current_name}` -> `{filename}`"
            print(f"🔧 {log_message.replace(chr(10), ' ')}")

            if self.dry_run:
                print("  [DRY RUN] Would update.")
                self.stats["aligned"] += 1
                return

            # 3. Apply Updates
            new_content = content
            # Update ID
            new_content = re.sub(id_pattern, f"\\1{expected_id}\\3", new_content)
            # Update Name
            new_content = re.sub(name_pattern, f"\\1{filename}\\3", new_content)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            if self.log_file:
                with open(self.log_file, "a", encoding="utf-8") as log:
                    log.write(log_message + "\n")

            print("  ✅ Updated.")
            self.stats["aligned"] += 1

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            self.stats["errors"] += 1

    def report(self):
        print(f"  Scanned: {self.stats['scanned']}")
        print(f"  Aligned: {self.stats['aligned']}")
        print(f"  Errors:  {self.stats['errors']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Align Internal IDs with Filenames.")
    parser.add_argument("--execute", action="store_true", help="Execute the changes.")
    parser.add_argument("--log", help="Path to log file.")
    parser.add_argument(
        "--files", nargs="*", help="Specific files or directories to scan."
    )
    args = parser.parse_args()

    aligner = IdentityAligner(
        dry_run=not args.execute, log_file=args.log, targets=args.files
    )
    aligner.scan_and_align()
