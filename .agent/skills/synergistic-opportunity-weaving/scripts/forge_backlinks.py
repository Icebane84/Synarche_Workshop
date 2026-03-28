"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-FORGE-BACKLINKS-001`                | The Sovereign ID. |
| **Official Name** | `forge_backlinks.py`                   | The Filename.     |
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
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[([^\]]+)\]\(([^)]+\.md)\)")


def extract_links(content: str) -> set[str]:
    """Extract all internal markdown links from content."""
    links = set()
    for match in LINK_RE.finditer(content):
        # Wiki-style [[link]] or Markdown [text](file.md)
        target = match.group(1) or os.path.basename(match.group(3) or "")
        if target:
            links.add(target.strip())
    return links


def forge_backlinks(directory: str) -> None:
    """Scan vault and detect missing backlinks."""
    nodes: dict[str, dict] = {}

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
            except Exception:
                continue
            nodes[f] = {"path": path, "links": extract_links(content)}

    missing = []
    for fname, data in nodes.items():
        for link in data["links"]:
            if link in nodes and fname not in nodes[link]["links"]:
                missing.append((fname, link))

    print("\n" + "=" * 70)
    print("  FORGE BACKLINKS — MISSING RECIPROCAL LINK REPORT".center(70))
    print("=" * 70)
    print(f"  Files Scanned: {len(nodes)}")
    print(f"  Missing Backlinks: {len(missing)}")
    print("-" * 70)

    for src, target in missing[:25]:
        print(f"  [{src}] links to [{target}] — but [{target}] does not link back.")

    if len(missing) > 25:
        print(f"\n  ... and {len(missing) - 25} more.")

    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Forge Backlinks — Reciprocal Link Auditor"
    )
    parser.add_argument("target", help="Directory to scan.")
    args = parser.parse_args()
    forge_backlinks(os.path.abspath(args.target))


if __name__ == "__main__":
    main()
