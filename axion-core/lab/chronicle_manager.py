"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-CHRONICLE-MANAGER-001`                | The Sovereign ID. |
| **Official Name** | `chronicle_manager.py`                   | The Filename.     |
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
from datetime import datetime

SKIP_DIRS = {".git", "node_modules", ".venv"}


def extract_title(content: str, filename: str) -> str:
    """Extract the first H1 heading from markdown content."""
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else filename


def chronicle_manager(directory: str, limit: int = 20) -> None:
    """List all chronicle entries in the target CSL directory."""
    print(f"\n>>> CHRONICLE MANAGER: {directory}\n")

    entries = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files, reverse=True):
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(path)
                modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                with open(path, encoding="utf-8") as fh:
                    content = fh.read(1000)
                title = extract_title(content, f)
                entries.append((modified, f, title))
            except Exception:
                continue

    entries.sort(reverse=True)

    print("=" * 80)
    print("  CHRONICLE — SYNTHESIS LOG INDEX".center(80))
    print("=" * 80)
    print(f"  {'DATE':<12} {'FILE':<40} {'TITLE'}")
    print("-" * 80)

    for date_str, fname, title in entries[:limit]:
        short_title = title if len(title) <= 30 else title[:27] + "..."
        short_file = fname if len(fname) <= 38 else fname[:35] + "..."
        print(f"  {date_str:<12} {short_file:<40} {short_title}")

    print("=" * 80)
    print(f"\n  Total Entries: {len(entries)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chronicle Manager — CSL Index Viewer")
    parser.add_argument("target", help="Directory containing chronicle .md files.")
    parser.add_argument("--limit", type=int, default=20, help="Max entries to display (default: 20).")
    args = parser.parse_args()
    chronicle_manager(os.path.abspath(args.target), limit=args.limit)


if __name__ == "__main__":
    main()
