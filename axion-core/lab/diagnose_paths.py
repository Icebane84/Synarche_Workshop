"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-DIAGNOSE-PATHS-001`                | The Sovereign ID. |
| **Official Name** | `diagnose_paths.py`                   | The Filename.     |
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
import re
from pathlib import Path

# Regex for paths like file:///c:/path/to/file or C:\path\to\file
PATH_REGEX = re.compile(r"(?:file:///|(?:\b[a-zA-Z]:))(?:\\[\w\s\.-]+|/[\w\s\.-]+)+")


def diagnose_paths(file_path: Path) -> None:
    """Scan a file for paths and check their existence."""
    print(f"\n>>> PATH DIAGNOSTIC: {file_path}\n")

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  [ERROR] Failed to read file: {e}")
        return

    paths = set(PATH_REGEX.findall(content))

    print("=" * 80)
    print("  DIAGNOSE PATHS — REFERENCE AUDIT".center(80))
    print("=" * 80)
    print(f"  {'REFERENCE TYPE':<15} | {'PATH':<50} | {'STATUS':<8}")
    print("-" * 80)

    broken = 0
    for p in sorted(paths):
        # Convert file:/// and URI encoding to normal path
        clean_path = p.replace("file:///", "").replace("%20", " ")
        if clean_path.startswith("/"):
            clean_path = clean_path[1:]  # Handle /C:/

        p_obj = Path(clean_path)
        status = "OK" if p_obj.exists() else "BROKEN"
        if status == "BROKEN":
            broken += 1

        ref_type = "[URI]" if "file:///" in p else "[ABSOLUTE]"
        print(f"  {ref_type:<15} | {p[:50]:<50} | {status:<8}")

    print("-" * 80)
    print(f"  Total Paths Found: {len(paths)}")
    print(f"  Broken Links:     {broken}")
    print("=" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose Paths — Reference Audit Tool")
    parser.add_argument("target", help="File to scan")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Error: {target} not found.")
        return

    diagnose_paths(target)


if __name__ == "__main__":
    main()
