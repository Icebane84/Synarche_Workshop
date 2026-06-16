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
import os
import re
import sys
from pathlib import Path
from typing import TypedDict

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


class Issue(TypedDict):
    file: str
    rule: str
    message: str


class CacheEntry(TypedDict):
    mtime: float
    issues: list[Issue]


class ScanResult(TypedDict):
    total_files: int
    aligned_files: int
    resonance_score: float
    unaligned_list: list[str]


class AuditReport(TypedDict):
    status: str
    total_issues: int
    issues: list[Issue]


class CodeSentinel:
    """Audit the workspace for OMEGA v15.0 (High Priestess) compliance."""

    def __init__(self, use_cache: bool = True, flush_cache: bool = False) -> None:
        """Initialize the Sentinel auditor."""
        self.issues_found: list[Issue] = []
        self.use_cache = use_cache
        self.flush_cache = flush_cache
        self.cache_file = CORE_DIR / ".sentinel_cache.json"
        self.cache_data: dict[str, CacheEntry] = self._load_cache()

    def _load_cache(self) -> dict[str, CacheEntry]:
        """Load the compliance cache from disk."""
        if self.flush_cache:
            return {}
        if self.use_cache and self.cache_file.exists():
            try:
                with open(self.cache_file, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                # FORTIFY: Corrupted cache detected. Eradicate it to ensure a clean slate.
                try:
                    self.cache_file.unlink()
                except OSError:
                    pass
                return {}
        return {}

    def _save_cache(self) -> None:
        """Flush the compliance cache to disk."""
        if self.use_cache:
            try:
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    json.dump(self.cache_data, f, indent=2)
            except Exception:
                pass

    def scan_governance(self, target_dir: str) -> ScanResult:
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

        mtime = os.path.getmtime(path)
        path_str = str(path)

        # Check cache before doing heavy AST parsing
        if self.use_cache and path_str in self.cache_data:
            cached_entry = self.cache_data[path_str]
            if cached_entry.get("mtime") == mtime:
                self.issues_found.extend(cached_entry.get("issues", []))
                return

        start_issue_count = len(self.issues_found)

        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self._report(file_path, "READ_ERROR", f"Could not read file: {e}")
            self._update_cache_entry(path_str, mtime, start_issue_count)
            return

        self._check_type_hints(path, content)
        self._check_docstrings(path, content)
        self._check_omega_metadata(path, content)
        self._check_exception_handling(path, content)
        self._check_print_statements(path, content)
        self._check_function_complexity(path, content)
        self._check_naming_conventions(path, content)
        self._check_unused_symbols(path, content)
        self._check_duplicates(path, content)
        self._check_mutable_defaults(path, content)
        self._check_import_consistency(path, content)
        self._check_assert_statements(path, content)
        self._check_inheritance_limits(path, content)
        self._check_boolean_traps(path, content)
        self._check_class_complexity(path, content)
        self._check_too_many_returns(path, content)
        self._check_deep_nesting(path, content)
        self._check_secrets_and_short_vars(path, content)
        self._check_pathlib_usage(path, content)
        self._check_security_risks(path, content)
        self._check_global_mutable_state(path, content)
        self._check_frozen_dataclasses(path, content)
        self._check_mutable_class_vars(path, content)

        self._update_cache_entry(path_str, mtime, start_issue_count)

    def _update_cache_entry(self, path_str: str, mtime: float, start_index: int) -> None:
        """Update the cache memory with newly found issues."""
        if self.use_cache:
            self.cache_data[path_str] = {"mtime": mtime, "issues": self.issues_found[start_index:]}

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
                has_arg_hints = all(arg.arg in {"self", "cls"} or arg.annotation is not None for arg in node.args.args)

                if has_return_hint and has_arg_hints:
                    continue

                hints = [
                    ("return type", has_return_hint),
                    ("argument type", has_arg_hints),
                ]
                missing = [t for t, h in hints if not h]
                error_code = (
                    "MISSING_ASYNC_TYPE_HINT" if isinstance(node, ast.AsyncFunctionDef) else "MISSING_TYPE_HINT"
                )
                func_type = "Async function" if isinstance(node, ast.AsyncFunctionDef) else "Function"
                self._report(
                    str(path),
                    error_code,
                    f"{func_type} '{node.name}' lacks: {', '.join(missing)}",
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

    def _check_exception_handling(self, path: Path, content: str) -> None:
        """Ensure no bare 'except:' or silently swallowed exceptions exist."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                is_broad = False
                if node.type is None:
                    self._report(str(path), "BARE_EXCEPT", "Bare 'except:' block found. Catch specific exceptions.")
                    is_broad = True
                elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
                    is_broad = True
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        self._report(
                            str(path), "SWALLOWED_EXCEPTION", "Silently swallowed generic 'Exception' with 'pass'."
                        )

                # Check if broad exceptions are properly logged or re-raised
                if is_broad:
                    has_log_or_raise = False
                    for child in ast.walk(node):
                        if isinstance(child, ast.Raise):
                            has_log_or_raise = True
                            break
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute) and child.func.attr in {
                                "error",
                                "exception",
                                "warning",
                                "critical",
                                "log",
                            }:
                                has_log_or_raise = True
                                break
                            if isinstance(child.func, ast.Name) and child.func.id == "print":
                                has_log_or_raise = True
                                break

                    if not has_log_or_raise:
                        self._report(
                            str(path),
                            "UNLOGGED_BROAD_EXCEPTION",
                            "Broad exception caught but neither logged nor re-raised.",
                        )

    def _check_print_statements(self, path: Path, content: str) -> None:
        """Ensure 'print()' is not used, enforcing centralized logging."""
        # Allow naked prints in CLI tools and entrypoint scripts
        if "tools" in path.parts or path.name in ("cli.py", "__main__.py"):
            return

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    self._report(
                        str(path),
                        "FORBIDDEN_PRINT",
                        f"Naked print() call detected on line {node.lineno}. Use logger instead.",
                    )

    def _check_function_complexity(self, path: Path, content: str) -> None:
        """Enforce maximum function length and cyclomatic complexity."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # 1. Check Function Length
                if hasattr(node, "end_lineno") and node.end_lineno and node.lineno:
                    func_length = node.end_lineno - node.lineno
                    if func_length > 100:
                        self._report(
                            str(path),
                            "FUNCTION_TOO_LONG",
                            f"Function '{node.name}' is {func_length} lines long (Max: 100). Consider refactoring.",
                        )

                # 2. Check Cyclomatic Complexity (Proxy)
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With, ast.BoolOp)):
                        complexity += 1

                if complexity > 15:
                    self._report(
                        str(path),
                        "FUNCTION_TOO_COMPLEX",
                        f"Function '{node.name}' has a complexity of {complexity} (Max: 15). Consider refactoring.",
                    )

    def _check_naming_conventions(self, path: Path, content: str) -> None:
        """Enforce PascalCase for classes and snake_case for functions/variables."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        pascal_case = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
        snake_case = re.compile(r"^_{0,2}[a-z][a-z0-9_]*_{0,2}$")
        constant_case = re.compile(r"^_{0,2}[A-Z][A-Z0-9_]*_{0,2}$")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not pascal_case.match(node.name):
                    self._report(str(path), "INVALID_CLASS_NAME", f"Class '{node.name}' should be PascalCase.")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not (snake_case.match(node.name) or (node.name.startswith("__") and node.name.endswith("__"))):
                    self._report(str(path), "INVALID_FUNCTION_NAME", f"Function '{node.name}' should be snake_case.")

                # Check method/function arguments
                all_args = node.args.args + node.args.kwonlyargs + getattr(node.args, "posonlyargs", [])
                for arg in all_args:
                    if not snake_case.match(arg.arg):
                        self._report(
                            str(path),
                            "INVALID_ARGUMENT_NAME",
                            f"Argument '{arg.arg}' in '{node.name}' should be snake_case.",
                        )
                if node.args.vararg and not snake_case.match(node.args.vararg.arg):
                    self._report(
                        str(path),
                        "INVALID_ARGUMENT_NAME",
                        f"Argument '*{node.args.vararg.arg}' in '{node.name}' should be snake_case.",
                    )
                if node.args.kwarg and not snake_case.match(node.args.kwarg.arg):
                    self._report(
                        str(path),
                        "INVALID_ARGUMENT_NAME",
                        f"Argument '**{node.args.kwarg.arg}' in '{node.name}' should be snake_case.",
                    )

            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        if not (snake_case.match(target.id) or constant_case.match(target.id)):
                            self._report(
                                str(path),
                                "INVALID_VARIABLE_NAME",
                                f"Variable '{target.id}' should be snake_case or UPPER_SNAKE_CASE.",
                            )

    def _check_unused_symbols(self, path: Path, content: str) -> None:
        """Detect completely unused imports and local variables (basic AST check)."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        imported_names = {}
        loaded_names = set()

        def _extract_string_types(annotation_node: ast.AST) -> None:
            for child in ast.walk(annotation_node):
                if isinstance(child, ast.Constant) and isinstance(child.value, str):
                    loaded_names.update(re.findall(r"[a-zA-Z_]\w*", child.value))

        # Global pass for imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names[alias.asname or alias.name] = node.lineno
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                loaded_names.add(node.id)
            elif isinstance(node, ast.arg) and node.annotation:
                _extract_string_types(node.annotation)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns:
                _extract_string_types(node.returns)
            elif isinstance(node, ast.AnnAssign) and node.annotation:
                _extract_string_types(node.annotation)

        for name, lineno in imported_names.items():
            if name not in loaded_names and name != "__all__":
                self._report(str(path), "UNUSED_IMPORT", f"Import '{name}' on line {lineno} appears unused.")

        # Local pass for variables
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                local_stores = {}
                local_loads = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.Name):
                        if isinstance(child.ctx, ast.Store):
                            local_stores[child.id] = child.lineno
                        elif isinstance(child.ctx, ast.Load):
                            local_loads.add(child.id)

                for name, lineno in local_stores.items():
                    if name not in local_loads and not name.startswith("_"):
                        self._report(
                            str(path),
                            "UNUSED_LOCAL",
                            f"Local variable '{name}' on line {lineno} in '{node.name}' appears unused.",
                        )

    def _check_duplicates(self, path: Path, content: str) -> None:
        """Detect duplicate dictionary keys and duplicate function arguments."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                seen_keys = set()
                for key in node.keys:
                    if key is None:
                        continue  # Skip dictionary unpacking e.g., {**kwargs}
                    if isinstance(key, ast.Constant):
                        if key.value in seen_keys:
                            self._report(
                                str(path),
                                "DUPLICATE_DICT_KEY",
                                f"Duplicate dictionary key '{key.value}' found on line {key.lineno}.",
                            )
                        seen_keys.add(key.value)

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                seen_args = set()
                all_args = node.args.args + node.args.kwonlyargs + getattr(node.args, "posonlyargs", [])
                if node.args.vararg:
                    all_args.append(node.args.vararg)
                if node.args.kwarg:
                    all_args.append(node.args.kwarg)
                for arg in all_args:
                    if arg.arg in seen_args:
                        self._report(
                            str(path),
                            "DUPLICATE_ARGUMENT",
                            f"Duplicate argument '{arg.arg}' in function '{node.name}' on line {node.lineno}.",
                        )
                    seen_args.add(arg.arg)

    def _check_mutable_defaults(self, path: Path, content: str) -> None:
        """Detect mutable default arguments (like [] or {}) in functions."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defaults = node.args.defaults + [d for d in node.args.kw_defaults if d is not None]
                for default in defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        self._report(
                            str(path),
                            "MUTABLE_DEFAULT",
                            f"Function '{node.name}' uses a mutable default argument on line {node.lineno}. Use 'None' instead.",
                        )

    def _check_import_consistency(self, path: Path, content: str) -> None:
        """Detect useless import aliases and excessively deep relative imports."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname == alias.name:
                        self._report(
                            str(path),
                            "USELESS_ALIAS",
                            f"Useless alias 'import {alias.name} as {alias.asname}' on line {node.lineno}.",
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.level is not None and node.level > 2:
                    self._report(
                        str(path),
                        "DEEP_RELATIVE_IMPORT",
                        f"Deep relative import (level {node.level}) on line {node.lineno}. Use absolute imports instead.",
                    )
                for alias in node.names:
                    if alias.asname == alias.name:
                        self._report(
                            str(path),
                            "USELESS_ALIAS",
                            f"Useless alias 'from {node.module or '.'} import {alias.name} as {alias.asname}' on line {node.lineno}.",
                        )

    def _check_assert_statements(self, path: Path, content: str) -> None:
        """Flag the use of 'assert' outside of test files."""
        # Heuristic for test files/directories
        if path.name.startswith("test_") or path.name.endswith("_test.py") or "tests" in path.parts:
            return

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                self._report(
                    str(path),
                    "FORBIDDEN_ASSERT",
                    f"'assert' statement used on line {node.lineno} outside of a test file. Use proper error handling.",
                )

    def _check_inheritance_limits(self, path: Path, content: str) -> None:
        """Limit the number of direct base classes (multiple inheritance) to prevent deep coupling."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        MAX_BASES = 3
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if len(node.bases) > MAX_BASES:
                    self._report(
                        str(path),
                        "EXCESSIVE_INHERITANCE",
                        f"Class '{node.name}' has {len(node.bases)} base classes (Max: {MAX_BASES}). Favor composition over inheritance.",
                    )

    def _check_boolean_traps(self, path: Path, content: str) -> None:
        """Flag boolean trap arguments (e.g., func(True)) in function calls."""
        # Heuristic to ignore test files, where positional booleans (like assertEqual) are common
        if path.name.startswith("test_") or path.name.endswith("_test.py") or "tests" in path.parts:
            return

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # We only flag positional arguments, not keyword arguments (node.keywords)
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, bool):
                        self._report(
                            str(path),
                            "BOOLEAN_TRAP",
                            f"Boolean trap detected on line {node.lineno}. Use keyword arguments (e.g., param=True) instead of passing raw booleans.",
                        )

    def _check_class_complexity(self, path: Path, content: str) -> None:
        """Flag classes that define too many methods (preventing 'God Objects')."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        MAX_METHODS = 15
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = sum(
                    1 for child in node.body if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
                if method_count > MAX_METHODS:
                    self._report(
                        str(path),
                        "TOO_MANY_METHODS",
                        f"Class '{node.name}' has {method_count} methods (Max: {MAX_METHODS}). Consider refactoring into smaller, composable units.",
                    )

    def _check_too_many_returns(self, path: Path, content: str) -> None:
        """Flag functions that return tuples with 4 or more elements."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Return) and node.value:
                if isinstance(node.value, ast.Tuple) and len(node.value.elts) >= 4:
                    self._report(
                        str(path),
                        "TOO_MANY_RETURN_VALUES",
                        f"Return statement on line {node.lineno} returns {len(node.value.elts)} variables. Use a dataclass or NamedTuple instead.",
                    )

    def _check_deep_nesting(self, path: Path, content: str) -> None:
        """Flag excessively deep control flow nesting (>= 4 levels)."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        def check_depth(node: ast.AST, current_depth: int) -> None:
            if current_depth >= 4:
                self._report(
                    str(path),
                    "DEEP_NESTING",
                    f"Control flow nesting too deep ({current_depth} levels) on line {getattr(node, 'lineno', '?')}. Extract into helper functions.",
                )
                return

            for child in ast.iter_child_nodes(node):
                next_depth = current_depth
                is_control_flow = isinstance(
                    child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith)
                )

                # Avoid treating 'elif' as an additional nesting level
                is_elif = False
                if isinstance(child, ast.If) and isinstance(node, ast.If):
                    if len(node.orelse) == 1 and node.orelse[0] is child:
                        is_elif = True

                if is_control_flow and not is_elif:
                    next_depth += 1

                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    next_depth = 0  # Reset depth for new scope

                check_depth(child, next_depth)

        for node in tree.body:
            check_depth(node, 0)

    def _check_secrets_and_short_vars(self, path: Path, content: str) -> None:
        """Flag hardcoded secrets and overly short variable names."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        secret_keywords = {"secret", "key", "token", "password", "pwd", "auth", "credential"}
        # Whitelist common short variable names to prevent false positives
        allowed_short = {
            "id",
            "db",
            "os",
            "re",
            "fs",
            "k",
            "v",
            "i",
            "j",
            "x",
            "y",
            "z",
            "e",
            "df",
            "pd",
            "np",
            "ax",
            "op",
            "fn",
            "pi",
            "_",
            "f",
            "c",
            "d",
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        var_lower = var_name.lower()
                        lineno = getattr(node, "lineno", "?")

                        # Short variable check
                        if len(var_name) < 3 and var_name not in allowed_short:
                            self._report(
                                str(path),
                                "SHORT_VARIABLE_NAME",
                                f"Variable '{var_name}' on line {lineno} is too short (< 3 chars). Use descriptive names.",
                            )

                        # Hardcoded secret check
                        if any(kw in var_lower for kw in secret_keywords):
                            value_node = node.value
                            if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
                                val = value_node.value
                                if len(val) > 0 and val.lower() not in {
                                    "",
                                    "placeholder",
                                    "todo",
                                    "your_token_here",
                                    "secure_token",
                                    "xxx",
                                }:
                                    self._report(
                                        str(path),
                                        "HARDCODED_SECRET",
                                        f"Potential hardcoded secret assigned to '{var_name}' on line {lineno}. Use environment variables or secret managers.",
                                    )

    def _check_pathlib_usage(self, path: Path, content: str) -> None:
        """Enforce the use of pathlib.Path over os.path."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            lineno = getattr(node, "lineno", "?")
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id == "os" and node.attr == "path":
                    self._report(
                        str(path),
                        "LEGACY_OS_PATH",
                        f"Usage of 'os.path' detected on line {lineno}. Refactor to use 'pathlib.Path'.",
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module == "os.path" or (node.module == "os" and any(a.name == "path" for a in node.names)):
                    self._report(
                        str(path),
                        "LEGACY_OS_PATH_IMPORT",
                        f"Import of 'os.path' detected on line {lineno}. Refactor to use 'pathlib.Path'.",
                    )

    def _check_security_risks(self, path: Path, content: str) -> None:
        """Flag dangerous built-ins like eval() and exec()."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"eval", "exec"}:
                    self._report(
                        str(path),
                        "SECURITY_RISK",
                        f"Use of dangerous built-in '{node.func.id}()' detected on line {node.lineno}. This violates zero-entropy security protocols.",
                    )

    def _check_global_mutable_state(self, path: Path, content: str) -> None:
        """Flag module-level mutable state (lists, dicts, sets)."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        # We only check the top-level body for module-level variables
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = node.value
                if isinstance(value, (ast.List, ast.Dict, ast.Set)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    for target in targets:
                        if isinstance(target, ast.Name):
                            if target.id == "__all__":
                                continue
                            self._report(
                                str(path),
                                "GLOBAL_MUTABLE_STATE",
                                f"Global mutable state '{target.id}' defined on line {getattr(node, 'lineno', '?')}. Use immutable types (tuple, frozenset) or encapsulate in a class.",
                            )

    def _check_frozen_dataclasses(self, path: Path, content: str) -> None:
        """Ensure all @dataclass definitions are frozen by default."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    is_dataclass = False
                    is_frozen = False

                    if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                        is_dataclass = True
                    elif isinstance(decorator, ast.Call) and getattr(decorator.func, "id", "") == "dataclass":
                        is_dataclass = True
                        for keyword in decorator.keywords:
                            if (
                                keyword.arg == "frozen"
                                and isinstance(keyword.value, ast.Constant)
                                and keyword.value.value is True
                            ):
                                is_frozen = True

                    if is_dataclass and not is_frozen:
                        self._report(
                            str(path),
                            "UNFROZEN_DATACLASS",
                            f"Dataclass '{node.name}' on line {node.lineno} is not frozen. Use '@dataclass(frozen=True)'.",
                        )

    def _check_mutable_class_vars(self, path: Path, content: str) -> None:
        """Flag mutable class variables to prevent shared ghost state across instances."""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.Assign, ast.AnnAssign)):
                        value = child.value
                        if isinstance(value, (ast.List, ast.Dict, ast.Set)):
                            targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                            for target in targets:
                                if isinstance(target, ast.Name):
                                    self._report(
                                        str(path),
                                        "MUTABLE_CLASS_VAR",
                                        f"Mutable class variable '{target.id}' defined in class '{node.name}' on line {getattr(child, 'lineno', '?')}. Use instance variables instead.",
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

        # Parse AST to gather all consecutive module-level docstrings
        try:
            tree = ast.parse(content)
            header_parts = []
            for node in tree.body:
                if (
                    isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    header_parts.append(node.value.value)
                else:
                    break
            header = "\n".join(header_parts)
        except SyntaxError:
            header = content[:4000]  # Fallback range for malformed syntax

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

    def generate_report(self) -> AuditReport:
        """Produce the final compliance audit report."""
        passed = len(self.issues_found) == 0
        return {
            "status": "PASS" if passed else "FAIL",
            "total_issues": len(self.issues_found),
            "issues": self.issues_found,
        }

    def run_full_audit(self, target_dir: str) -> AuditReport:
        """Execute the auditor across an entire directory."""
        path = Path(target_dir)
        for py_file in path.rglob("*.py"):
            self.audit_file(str(py_file))
        self._save_cache()
        return self.generate_report()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CodeSentinel Compliance Auditor")
    parser.add_argument("--target", default=str(SRC_DIR), help="Directory to scan")
    parser.add_argument("--flush-cache", action="store_true", help="Flush the cache before scanning")
    args = parser.parse_args()

    sentinel = CodeSentinel(flush_cache=args.flush_cache)
    report = sentinel.run_full_audit(args.target)
    print(json.dumps(report, indent=2))
    if report["status"] == "FAIL":
        sys.exit(1)
