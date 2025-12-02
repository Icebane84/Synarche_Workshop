"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-LINT-ARTIFACT-001`                | The Sovereign ID. |
| **Official Name** | `lint_artifact.py`                   | The Filename.     |
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
from security import execute_safe
import sys
from pathlib import Path


def lint_python(file_path: Path) -> bool:
    """Run Ruff on a Python file."""
    print(f"  >>> Linting Python: {file_path}")
    try:
        # Check if ruff is installed
        result = execute_safe(["ruff", "check", str(file_path)], check=False, capture_output=True, text=True)
        if result.returncode == 0:
            print("  [PASS] No issues found by Ruff.")
            return True
        else:
            print("  [FAIL] Ruff found issues:")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("  [WARN] Ruff not found. Skipping Python lint.")
        return True


def lint_markdown(file_path: Path) -> bool:
    """Run Markdownlint on a Markdown file (basic structural check)."""
    print(f"  >>> Linting Markdown: {file_path}")
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
            if not content.startswith("#"):
                print("  [FAIL] Markdown file does not start with a h1 header.")
                return False
            else:
                print("  [PASS] Basic structural check passed.")
                return True
    except Exception as e:
        print(f"  [ERROR] Failed to read file: {e}")
        return False


def process_target(target: Path) -> bool:
    """Recursively processes a file or directory."""
    if not target.exists():
        print(f"  [ERROR] Path not found: {target}")
        return False

    success = True
    if target.is_file():
        if target.suffix == ".py":
            success &= lint_python(target)
        elif target.suffix == ".md":
            success &= lint_markdown(target)
    elif target.is_dir():
        for item in target.rglob("*"):
            if item.is_file() and not any(p in item.parts for p in [".git", "node_modules", "__pycache__"]):
                if item.suffix == ".py":
                    success &= lint_python(item)
                elif item.suffix == ".md":
                    success &= lint_markdown(item)
    return success


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint Artifact — Static Analysis Auditor")
    parser.add_argument("target", help="File or directory to lint")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    print(f"\n>>> LINT ARTIFACT: {target}\n")

    print("=" * 60)
    print("  LINT ARTIFACT — SITE INSPECTION".center(60))
    print("=" * 60)

    success = process_target(target)

    print("=" * 60)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
