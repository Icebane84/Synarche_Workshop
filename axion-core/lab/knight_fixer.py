"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-KNIGHT-FIXER-001`                | The Sovereign ID. |
| **Official Name** | `knight_fixer.py`                   | The Filename.     |
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

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def fix_file(filepath: str, dry_run: bool = False) -> bool:
    """Apply automated fixes to a single Python file. Returns True if changed."""
    try:
        with open(filepath, encoding="utf-8") as fh:
            original = fh.read()
    except Exception:
        return False

    # Normalize CRLF to LF
    fixed = original.replace("\r\n", "\n")

    # Strip trailing whitespace from each line
    fixed = "\n".join(line.rstrip() for line in fixed.split("\n"))

    # Collapse 3+ consecutive blank lines to 2
    fixed = re.sub(r"\n{3,}", "\n\n", fixed)

    # Ensure exactly one newline at end of file
    fixed = fixed.rstrip("\n") + "\n"

    if fixed == original:
        return False

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(fixed)

    return True


def knight_fixer(target: str, dry_run: bool = False) -> None:
    """Run the Knight Fixer across a file or directory."""
    mode = "[DRY RUN]" if dry_run else "[LIVE FIX]"
    print(f"\n>>> KNIGHT FIXER {mode}: {target}\n")

    targets = []
    if os.path.isfile(target):
        targets = [target]
    else:
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.endswith(".py"):
                    targets.append(os.path.join(root, f))

    fixed_count = 0
    for filepath in targets:
        if fix_file(filepath, dry_run=dry_run):
            fixed_count += 1
            print(f"  [FIXED] {os.path.basename(filepath)}")

    print("\n" + "=" * 60)
    print(f"  Files Scanned:  {len(targets)}")
    print(f"  Files Fixed:    {fixed_count}")
    if dry_run:
        print("  Mode: DRY RUN — No files were written.")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Knight Fixer — Automated Code Cleanup")
    parser.add_argument("target", help="File or directory to fix.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing.")
    args = parser.parse_args()
    knight_fixer(os.path.abspath(args.target), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
