"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-IMPACT-ANALYSIS-001`                | The Sovereign ID. |
| **Official Name** | `impact_analysis.py`                   | The Filename.     |
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
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}


def analyze_impact(query: str, root_dir: Path) -> None:
    """Search for references to a query string across the workspace."""
    print(f"\n>>> IMPACT ANALYSIS: Searching for '{query}' in {root_dir}\n")

    matches = []
    for p in root_dir.glob("**/*"):
        if p.is_dir() and p.name in SKIP_DIRS:
            continue
        if not p.is_file():
            continue
        if p.suffix not in [".md", ".py", ".json", ".ts", ".tsx", ".css"]:
            continue

        try:
            with open(p, encoding="utf-8") as f:
                content = f.read()
                if query in content:
                    matches.append(p)
        except Exception:
            continue

    print("=" * 80)
    print("  IMPACT ANALYSIS — DOWNSTREAM EFFECT REPORT".center(80))
    print("=" * 80)
    print(f"  Target: {query}")
    print(f"  Total Impacted Files: {len(matches)}")
    print("-" * 80)

    for m in matches[:25]:
        print(f"  [IMPACT] {m.relative_to(root_dir)}")

    if len(matches) > 25:
        print(f"\n  ... and {len(matches) - 25} more files.")

    print("=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Impact Analysis — Downstream Effect Auditor"
    )
    parser.add_argument("query", help="File name or Artifact ID to search for")
    parser.add_argument(
        "--root", default=".", help="Root directory to scan (default: current)"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    analyze_impact(args.query, root)


if __name__ == "__main__":
    main()
