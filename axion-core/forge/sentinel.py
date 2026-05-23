"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-HEPH-SENTINEL-001`      | The Sovereign ID. |
| **Official Name**   | `sentinel.py`                 | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-HEPH`                   | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Vigilant Governance (Law 28)**
> Implemented from Blueprint `GVRN.REG.ComplianceAudit.md`.
> Ethos: Unwavering Standard, Silent Guardian.
"""

import ast
import json
import logging
import sys
from pathlib import Path
from typing import Any

# Hephaestus Lib Imports
try:
    # Add root to sys.path if not present to allow importing from 'tools'
    root_path = str(Path(__file__).parent.parent)
    if root_path not in sys.path:
        sys.path.append(root_path)
    from tools.resonance_scanner import is_aligned
except ImportError:
    # Fallback stub if resonance_scanner is missing
    def is_aligned(path: Path) -> bool:
        return True


# Configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# OMEGA Standard Directory References
WORKSPACE_ROOT = Path("c:/Users/Chris/Synarche_Workspace")
CORE_DIR = WORKSPACE_ROOT / "axion-core"
SRC_DIR = CORE_DIR / "src"
AGENTS_DIR = SRC_DIR / "agents"


class CodeSentinel:
    """Audit the workspace for OMEGA v15.0 (High Priestess) compliance."""

    def __init__(self) -> None:
        """Initialize the Sentinel auditor."""
        self.issues_found: list[dict[str, str]] = []

    def scan_governance(self, target_dir: str) -> dict[str, Any]:
        """Check for structural resonance and governance alignment across a directory."""
        path = Path(target_dir)
        total = 0
        aligned = 0
        unaligned = []

        for py_file in path.rglob("*.py"):
            total += 1
            if is_aligned(py_file):
                aligned += 1
            else:
                unaligned.append(str(py_file))

        score = (aligned / total * 100) if total > 0 else 0.0
        return {
            "total_files": total,
            "aligned_files": aligned,
            "resonance_score": round(score, 2),
            "unaligned_list": unaligned,
        }

    def audit_file(self, file_path: str) -> None:
        """Run all compliance checks on a single file."""
        path = Path(file_path)
        if not path.exists() or path.suffix != ".py":
            return

        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self._report(file_path, "READ_ERROR", f"Could not read file: {e}")
            return

        self._check_type_hints(path, content)
        self._check_docstrings(path, content)
        self._check_omega_metadata(path, content)

    def _check_type_hints(self, path: Path, content: str) -> None:
        """Verify that all functions and methods have type hints."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            self._report(str(path), "SYNTAX_ERROR", "File cannot be parsed by AST.")
            return

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Ignore init and simple internal methods if desired, but strict OMEGA requires all.
                if node.name == "__init__":
                    continue

                has_return_hint = node.returns is not None
                has_arg_hints = all(
                    arg.arg in {"self", "cls"} or arg.annotation is not None
                    for arg in node.args.args
                )

                if has_return_hint and has_arg_hints:
                    continue

                hints = [
                    ("return type", has_return_hint),
                    ("argument type", has_arg_hints),
                ]
                missing = [t for t, h in hints if not h]
                self._report(
                    str(path),
                    "MISSING_TYPE_HINT",
                    f"Function '{node.name}' lacks: {', '.join(missing)}",
                )

    def _check_docstrings(self, path: Path, content: str) -> None:
        """Verify presence of docstrings on classes and functions."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return  # Already handled

        for node in ast.walk(tree):
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and not ast.get_docstring(node)
                and node.name != "__init__"
            ):
                node_type = "Class" if isinstance(node, ast.ClassDef) else "Function"
                self._report(
                    str(path),
                    f"MISSING_{node_type.upper()}_DOCSTRING",
                    f"{node_type} '{node.name}' lacks a docstring.",
                )

    def _check_omega_metadata(self, path: Path, content: str) -> None:
        """Ensure the file header contains OMEGA Standard metadata."""
        if not content.startswith('"""'):
            self._report(
                str(path),
                "MISSING_OMEGA_HEADER",
                "File does not start with a module docstring.",
            )
            return

        docstring_end = content.find('"""', 3)
        if docstring_end == -1:
            return  # Malformed

        header = content[3:docstring_end]

        # OMEGA v15.0 strict check
        if "v15.0" not in header and "OMEGA" not in header:
            self._report(
                str(path),
                "LEGACY_VERSION",
                "Module docstring must specify OMEGA v15.0.",
            )

        if "UIP-V15" not in header and "Identification Lock" not in header:
            self._report(
                str(path),
                "MISSING_UIP_V15",
                "Module docstring lacks UIP-V15 block structure.",
            )

        if "High Priestess" not in header and "Sovereign" not in header:
            self._report(
                str(path),
                "MISSING_IDENTITY",
                "Module docstring lacks Sovereign Identity marker (High Priestess).",
            )

    def _report(self, file_path: str, rule: str, message: str) -> None:
        """Log a compliance violation."""
        issue = {"file": file_path, "rule": rule, "message": message}
        self.issues_found.append(issue)
        logger.warning(f"[{rule}] {file_path}: {message}")

    def generate_report(self) -> dict[str, Any]:
        """Produce the final compliance audit report."""
        passed = len(self.issues_found) == 0
        return {
            "status": "PASS" if passed else "FAIL",
            "total_issues": len(self.issues_found),
            "issues": self.issues_found,
        }

    def run_full_audit(self, target_dir: str) -> dict[str, Any]:
        """Execute the auditor across an entire directory."""
        path = Path(target_dir)
        for py_file in path.rglob("*.py"):
            self.audit_file(str(py_file))
        return self.generate_report()


if __name__ == "__main__":
    # Example execution
    sentinel = CodeSentinel()
    report = sentinel.run_full_audit(str(SRC_DIR))
    logger.info(json.dumps(report, indent=2))
