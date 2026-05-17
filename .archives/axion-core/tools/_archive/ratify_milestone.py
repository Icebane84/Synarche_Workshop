#!/usr/bin/env python3
"""
# TOOL-GVRN-009: The Gavel of Law
# Domain: GVRN | Tag: Identity
# Purpose: Ratifies milestones in GVRN-ENTITY-001.md.
"""

import argparse
import re
from pathlib import Path

# Constants
ENTITY_FILE = Path(
    "c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library/GVRN-ENTITY-001_SynarcheEntities_v11.0.md"
)


def ratify_milestone(milestone_id: str):
    """Changes a milestone from UNLOCKED to RATIFIED."""

    if not ENTITY_FILE.exists():
        print(f"Error: {ENTITY_FILE} not found.")
        return

    content = ENTITY_FILE.read_text(encoding="utf-8")

    # Regex to find the milestone line and change its status
    pattern = rf"(\| \*\*{milestone_id}\*\* \| .*? \| .*? \| .*? \| \*\*).*?(\*\*) \|"
    replacement = r"\1RATIFIED\2 |"

    new_content, count = re.subn(pattern, replacement, content)

    if count > 0:
        ENTITY_FILE.write_text(new_content, encoding="utf-8")
        print(f"🏆 MILESTONE {milestone_id} RATIFIED. The Synarche acknowledges your progress.")
    else:
        print(f"❌ Milestone {milestone_id} not found or status already ratified.")


def main():
    parser = argparse.ArgumentParser(description="RATIFY_MILESTONE: Ratify an unlocked milestone.")
    parser.add_argument("--id", required=True, help="The PAM ID of the milestone.")

    args = parser.parse_args()
    ratify_milestone(args.id)


if __name__ == "__main__":
    main()
