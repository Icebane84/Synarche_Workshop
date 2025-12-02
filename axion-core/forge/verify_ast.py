"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-VERIFY-AST-001`                | The Sovereign ID. |
| **Official Name** | `verify_ast.py`                   | The Filename.     |
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
import ast
import sys
from pathlib import Path


def verify_file_ast(file_path: Path) -> bool:
    """Parse output AST for a single file and report status."""
    print(f"  >>> AST VERIFICATION: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as f:
            source = f.read()

        ast_tree = ast.parse(source)

        # Simple count of functions and classes
        functions = [n for n in ast.walk(ast_tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(ast_tree) if isinstance(n, ast.ClassDef)]

        print(f"      [PASS] Classes: {len(classes)}, Functions: {len(functions)}")
        return True

    except SyntaxError as e:
        print(f"      [FAIL] Syntax Error: {e.msg} (Line {e.lineno})")
        return False
    except Exception as e:
        print(f"      [ERROR] Parsing failed: {e}")
        return False


def process_target(target: Path) -> bool:
    """Recursively processes a file or directory."""
    if not target.exists():
        print(f"  [ERROR] Path not found: {target}")
        return False

    success = True
    if target.is_file():
        if target.suffix == ".py":
            success &= verify_file_ast(target)
    elif target.is_dir():
        for item in target.rglob("*.py"):
            if not any(p in item.parts for p in [".git", "node_modules", "__pycache__"]):
                success &= verify_file_ast(item)
    return success


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify AST — Logic Integrity Auditor")
    parser.add_argument("target", help="Python file or directory to verify")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    print(f"\n>>> AST VERIFICATION: {target}\n")

    print("=" * 60)
    print("  AST VERIFICATION — SITE INSPECTION".center(60))
    print("=" * 60)

    success = process_target(target)

    print("=" * 60)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
