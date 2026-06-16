"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-REFORGE-LIBRARY-001`                | The Sovereign ID. |
| **Official Name** | `reforge_library.py`                   | The Filename.     |
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
import os
from typing import Any

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def audit_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    """Audit a function for typing compliance."""
    issues = []
    for arg in node.args.args:
        if arg.arg in ("self", "cls"):
            continue
        if arg.annotation is None:
            issues.append(f"Arg `{arg.arg}` missing type hint")
    if node.returns is None:
        issues.append("Return type missing")
    return {
        "name": node.name,
        "line": node.lineno,
        "compliant": len(issues) == 0,
        "issues": issues,
    }


def reforge_library(path: str) -> None:
    """Scan all Python files in path and report typing compliance."""
    targets = []
    if os.path.isfile(path):
        targets = [path]
    else:
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if f.endswith(".py"):
                    targets.append(os.path.join(root, f))

    total_funcs = 0
    total_compliant = 0
    violations = []

    for filepath in targets:
        try:
            with open(filepath, encoding="utf-8") as fh:
                content = fh.read()
            tree = ast.parse(content)
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                result = audit_function(node)
                total_funcs += 1
                if result["compliant"]:
                    total_compliant += 1
                else:
                    violations.append(
                        {
                            "file": os.path.basename(filepath),
                            **result,
                        }
                    )

    print("\n" + "=" * 70)
    print("  REFORGE LIBRARY — TYPE COMPLIANCE REPORT".center(70))
    print("=" * 70)
    print(f"  Functions Scanned: {total_funcs}")
    print(f"  Fully Compliant:   {total_compliant}")
    print(f"  Violations:        {len(violations)}")
    compliance_rate = (
        (total_compliant / total_funcs * 100) if total_funcs > 0 else 100.0
    )
    print(f"  Compliance Rate:   {compliance_rate:.1f}%")
    print("-" * 70)

    for v in violations[:20]:
        print(f"\n  [!] {v['file']} :: {v['name']} (L{v['line']})")
        for issue in v["issues"]:
            print(f"      - {issue}")

    if len(violations) > 20:
        print(f"\n  ... and {len(violations) - 20} more violations.")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reforge Library — Type Compliance Auditor"
    )
    parser.add_argument("target", help="File or directory to audit.")
    args = parser.parse_args()
    reforge_library(os.path.abspath(args.target))


if __name__ == "__main__":
    main()
