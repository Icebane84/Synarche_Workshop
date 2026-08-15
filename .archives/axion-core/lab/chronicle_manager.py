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
import json
from datetime import datetime
from typing import Optional
SKIP_DIRS = {".git", "node_modules", ".venv", ".obsidian"}


def extract_title(content: str, filename: str) -> str:
    """Extract the first H1 heading from markdown content."""
    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else filename


def _process_entry(path: str, fname: str) -> Optional[dict]:
    """Try to read a markdown file and extract metadata."""
    try:
        mtime = os.path.getmtime(path)
        modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        with open(path, encoding="utf-8") as fh:
            content = fh.read(1000)
        title = extract_title(content, fname)
        return {"date": modified, "file": path, "title": title}
    except Exception:
        return None


def chronicle_manager(directory: str, limit: int = 20, output_file: Optional[str] = None) -> None:
    """List all chronicle entries in the target CSL directory."""
    print(f"\n>>> CHRONICLE MANAGER: {directory}\n")

    entries = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in sorted(files, reverse=True):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(root, fname)
            entry = _process_entry(path, fname)
            if entry:
                entries.append(entry)

    # Sort entries by date (newest first)
    entries.sort(key=lambda x: x["date"], reverse=True)

    # Limit the entries
    limited_entries = entries[:limit]

    if output_file:
        # Write to JSON file
        report = {
            "source_directory": directory,
            "total_entries": len(entries),
            "display_limit": limit,
            "chronicles": limited_entries,
        }
        with open(output_file, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"✅ Chronicle index saved to: {output_file}")
    else:
        # Print to console
        print("=" * 80)
        print("  CHRONICLE — SYNTHESIS LOG INDEX".center(80))
        print("=" * 80)
        print(f"  {'DATE':<12} {'FILE':<40} {'TITLE'}")
        print("-" * 80)

        for entry in limited_entries:
            short_title = entry['title'] if len(entry['title']) <= 30 else entry['title'][:27] + "..."
            short_file = entry['file'] if len(entry['file']) <= 38 else entry['file'][:35] + "..."
            print(f"  {entry['date']:<12} {short_file:<40} {short_title}")

        print("=" * 80)
        print(f"\n  Total Entries: {len(entries)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chronicle Manager — CSL Index Viewer")
    parser.add_argument("target", help="Directory containing chronicle .md files.")
    parser.add_argument(
        "--limit", type=int, default=20, help="Max entries to display (default: 20)."
    )
    parser.add_argument("--output", help="Path to save the JSON output file.")
    args = parser.parse_args()
    chronicle_manager(os.path.abspath(args.target), limit=args.limit, output_file=args.output)


if __name__ == "__main__":
    main()
