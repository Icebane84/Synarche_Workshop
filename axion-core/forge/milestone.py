"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-LOG-REFACTOR-MILESTONE-001`                | The Sovereign ID. |
| **Official Name** | `log_refactor_milestone.py`                   | The Filename.     |
| **Version**       | **v14.0 [OMEGA]**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-08`                       | Creation Date.    |.
"""

import argparse
import os
from datetime import datetime

MILESTONE_TEMPLATE = """\
---

## Milestone: {title}

> **Logged**: {timestamp}
> **Author**: Axion Prime (Master Artificer)
> **Phase**: {phase}

### Summary
{summary}

### Impact
- **Files Modified**: {files}
- **XP Award**: Calculated by AAG
- **Stat Delta**: Coherence (+1)
"""


def log_refactor_milestone(
    chronicle_path: str,
    title: str,
    summary: str,
    phase: str,
    files: str,
) -> None:
    """Append a milestone entry to the target chronicle file."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    entry = MILESTONE_TEMPLATE.format(
        title=title,
        timestamp=timestamp,
        phase=phase,
        summary=summary,
        files=files,
    )

    if not os.path.exists(chronicle_path):
        # Create the chronicle file if it doesn't exist with OMEGA v14.0 Header
        with open(chronicle_path, "w", encoding="utf-8") as fh:
            fh.write("# CHR.Axion.RefactorChronicle\n\n")
            fh.write("> [!IMPORTANT]\n")
            fh.write("> **Standard**: OMEGA v14.0 [CANONIZED]\n")
            fh.write(f"> **Initialization**: {timestamp}\n\n")
            fh.write("## I. The Integrity Gate (CIV-GATE)\n\n")
            fh.write("- [ ] **Compliance Audit**: Standard OMEGA v14.0 linter pass.\n")
            fh.write("- [ ] **Truth Stability**: Dragonslayer Audit pass.\n")
            fh.write("- [ ] **Sentinel Link**: `[PENDING]`\n\n")
            fh.write("## II. Actionable Prompt Packet\n\n")
            fh.write("- **Goal**: Chronicle and canonize all refactoring milestones.\n")
            fh.write(
                "- **Trigger**: Manual execution of `log_refactor_milestone.py`.\n\n"
            )

    with open(chronicle_path, "a", encoding="utf-8") as fh:
        fh.write(entry)

    print(f"\n[OK] Milestone logged to: {chronicle_path}")
    print(f"     Title: {title}")
    print(f"     Phase: {phase}")
    print(f"     Timestamp: {timestamp}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Log Refactor Milestone — Chronicle Appender"
    )
    parser.add_argument("chronicle", help="Path to the chronicle markdown file.")
    parser.add_argument("title", help="Short title for the milestone.")
    parser.add_argument(
        "--summary", default="Milestone completed.", help="Milestone summary text."
    )
    parser.add_argument(
        "--phase", default="N/A", help="Phase label (e.g., 'Phase 27')."
    )
    parser.add_argument(
        "--files", default="N/A", help="Comma-separated list of modified files."
    )
    args = parser.parse_args()

    log_refactor_milestone(
        chronicle_path=os.path.abspath(args.chronicle),
        title=args.title,
        summary=args.summary,
        phase=args.phase,
        files=args.files,
    )


if __name__ == "__main__":
    main()
