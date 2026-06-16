"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-DRAGONSLAYER-001`                | The Sovereign ID. |
| **Official Name** | `dragonslayer_audit.py`                   | The Filename.     |
| **Version**       | **v14.0 [OMEGA]**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-01`                       | Creation Date.    |.
"""

import ast
import builtins
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("dragonslayer")


class DragonslayerAuditor(ast.NodeVisitor):
    """The Sword of Truth — Specialized AST-linter for OMEGA."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.issues: list[str] = []
        self.defined_names: set[str] = set()
        self.used_names: set[str] = set()
        self.current_function: str | None = None

    def audit(self) -> bool:
        """Executes the audit on the target file."""
        if not os.path.exists(self.filepath):
            logger.error(f"File {self.filepath} not found.")
            return False

        try:
            with open(self.filepath, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            logger.info(
                f"--- [DRAGONSLAYER AUDIT] INITIATING: {os.path.basename(self.filepath)} ---"
            )
            self.visit(tree)

            # Check for name consistency
            hallucinated_names = (
                self.used_names - self.defined_names - set(dir(builtins))
            )
            for name in hallucinated_names:
                self.issues.append(
                    f"[Hallucination] Name used but not defined or builtin: {name}"
                )

            if self.issues:
                for issue in self.issues:
                    logger.error(f"> {issue}")
                return False
            else:
                logger.info(
                    f"> SUCCESS: {os.path.basename(self.filepath)} is TRUTH-STABLE."
                )
                return True
        except SyntaxError:
            logger.exception(f"Syntax Error in {self.filepath}")
            return False
        except Exception:
            logger.exception(f"Audit failed for {self.filepath}")
            return False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.defined_names.add(node.name)
        self.current_function = node.name

        if (
            len(node.body) == 1
            and isinstance(node.body[0], (ast.Pass, ast.Expr))
            and not (
                isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            )
        ):
            self.issues.append(
                f"[Deceptive Logic] Empty function detected: {node.name}"
            )

        for item in node.body:
            if (
                isinstance(item, ast.Expr)
                and isinstance(item.value, ast.Constant)
                and "[HALLUCINATED:]" in str(item.value.value)
            ):
                self.issues.append(
                    f"[Truth Violation] Hallucination marker found in docstring of {node.name}"
                )

        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.used_names.add(node.func.id)
            if "TODO" in node.func.id or "magic_" in node.func.id:
                self.issues.append(
                    f"[Hallucinated Call] Suspicious name: {node.func.id}"
                )

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if "hallucinated" in node.attr.lower() or "mock_" in node.attr.lower():
            self.issues.append(
                f"[Mock Logic Warning] Possible non-existent attribute access: {node.attr}"
            )
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.defined_names.add(name)
        self.generic_visit(node)


def main() -> None:
    min_args = 2
    if len(sys.argv) < min_args:
        logger.warning(f"Usage: python {sys.argv[0]} <file_path>")
        sys.exit(1)

    filepath = sys.argv[1]
    auditor = DragonslayerAuditor(filepath)
    auditor.audit()


if __name__ == "__main__":
    main()
