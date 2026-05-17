"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-FIND-UNLINKED-001`                | The Sovereign ID. |
| **Official Name** | `find_unlinked.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import os
import re

SKIP_DIRS = {".git", "node_modules", ".venv"}
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[(?:[^\]]+)\]\(([^)]+\.md)\)")


def find_unlinked(directory: str) -> None:
    """Find all markdown files with zero inbound links."""
    all_files: set[str] = set()
    all_referenced: set[str] = set()

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            all_files.add(f)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
                for match in LINK_RE.finditer(content):
                    ref = match.group(1) or os.path.basename(match.group(2) or "")
                    if ref:
                        all_referenced.add(ref.strip())
            except Exception:
                continue

    orphans = sorted(all_files - all_referenced)

    print("\n" + "=" * 70)
    print("  FIND UNLINKED — VAULT ISLAND DETECTION REPORT".center(70))
    print("=" * 70)
    print(f"  Total Files:     {len(all_files)}")
    print(f"  Referenced:      {len(all_referenced & all_files)}")
    print(f"  Islands (Orphans): {len(orphans)}")
    print("-" * 70)

    for orphan in orphans[:30]:
        print(f"  [ISLAND] {orphan}")

    if len(orphans) > 30:
        print(f"\n  ... and {len(orphans) - 30} more islands.")

    print("=" * 70)

    if not orphans:
        print("\n[OK] No islands found. The vault is fully connected.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Find Unlinked — Vault Island Detector")
    parser.add_argument("target", help="Directory to scan.")
    args = parser.parse_args()
    find_unlinked(os.path.abspath(args.target))


if __name__ == "__main__":
    main()
