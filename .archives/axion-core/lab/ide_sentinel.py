"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-IDE-SENTINEL-001`                | The Sovereign ID. |
| **Official Name** | `ide_sentinel.py`                   | The Filename.     |
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
import json
import sys
from pathlib import Path


def check_vscode_settings(workspace_root: Path) -> dict:
    """Check .vscode/settings.json for specific standard requirements."""
    settings_path = workspace_root / ".vscode" / "settings.json"
    results = {"path": str(settings_path), "exists": False, "violations": []}

    if not settings_path.exists():
        results["violations"].append("Missing .vscode/settings.json")
        return results

    results["exists"] = True
    try:
        with open(settings_path, encoding="utf-8") as f:
            # Simple JSON load. For JSON with comments, we'd need a more robust parser.
            # But we assume valid JSON for standard compliance.
            content = f.read()
            # Strip comments (primitive)
            content = "\n".join(
                [
                    line
                    for line in content.splitlines()
                    if not line.strip().startswith("//")
                ]
            )
            settings = json.loads(content)

        if settings.get("editor.tabSize") != 4:
            results["violations"].append("editor.tabSize should be 4")
        if settings.get("editor.insertSpaces") is not True:
            results["violations"].append("editor.insertSpaces should be true")

    except Exception as e:
        results["violations"].append(f"Failed to parse settings.json: {e}")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="IDE Sentinel — Workspace Configuration Auditor"
    )
    parser.add_argument(
        "target", nargs="?", default=".", help="Workspace root directory"
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    print(f"\n>>> IDE SENTINEL SCAN: {root}\n")

    results = check_vscode_settings(root)

    print("=" * 60)
    print("  IDE SENTINEL — CONFIGURATION REPORT".center(60))
    print("=" * 60)
    print(f"  Settings Path: {results['path']}")
    print(f"  Status:        {'OK' if not results['violations'] else 'FAILED'}")
    print("-" * 60)

    if results["violations"]:
        for violation in results["violations"]:
            print(f"  [!] {violation}")
    else:
        print("  [PASS] All core workspace settings conform to Synarche standards.")

    print("=" * 60)

    if results["violations"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
