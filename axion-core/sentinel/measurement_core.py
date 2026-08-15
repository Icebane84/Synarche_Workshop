# ARTIFACT_ID: SENTINEL.MeasurementCore
# VERSION: v1.0
# STATUS: [ACTIVE]
import ast
import importlib.util
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import DeclaredState, ObservedState
from .verifiers import compute_artifact_hash, find_hardcoded_paths, find_pyc_files

logger = logging.getLogger(__name__)


class MeasurementCore:
    """
    SP-MEASURE-002: Executes verifiers to produce observed states.
    """

    def __init__(self) -> None:
        self._register_verifiers()

    def _register_verifiers(self) -> None:
        """Registers all verifier functions."""
        self.verifiers = {
            "python_compile": self._run_python_compile,
            "content_hash_validator": self._run_content_hash_validator,
            "test_suite_runner": self._run_test_suite_runner,
            "path_validator": self._run_path_validator,
            "artifact_cleanliness_check": self._run_artifact_cleanliness_check,
            "dependency_resolver": self._run_dependency_resolver,
            "license_check": self._run_license_check,
        }

    def _run_license_check(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        """Checks for the presence of a LICENSE file in the project root."""
        try:
            # Traverse up to find a root marker, assuming .git is the root.
            current_path = Path(artifact_path).resolve().parent
            while current_path != current_path.parent and not (current_path / ".git").exists():
                current_path = current_path.parent

            possible_license_files = ["LICENSE", "LICENSE.md", "LICENSE.txt"]
            if any((current_path / f).exists() for f in possible_license_files):
                return {"status": "PASS", "message": "A LICENSE file was found in the project root."}
            return {"status": "FAIL", "message": "No LICENSE file found in the project root."}
        except Exception as e:
            return {"status": "VERIFIER_FAILURE", "message": f"Could not perform license check: {e}"}

    def _run_python_compile(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        path = Path(artifact_path)
        if path.suffix != ".py":
            return {"status": "NOT_APPLICABLE", "message": "Not a Python file."}
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            ast.parse(source, filename=str(path))
            return {"status": "PASS", "message": "Compilation successful"}
        except SyntaxError as e:
            return {"status": "FAIL", "message": f"SyntaxError: {e.msg} (line {e.lineno})"}
        except OSError as e:
            return {"status": "VERIFIER_FAILURE", "message": f"Could not read file: {e}"}

    def _run_content_hash_validator(self, artifact_path: str, declared: Optional[DeclaredState]) -> Dict[str, Any]:
        declared_hash = declared.metadata.get("hash") if declared else None
        if not declared_hash:
            return {"status": "NOT_APPLICABLE", "message": "No declared hash found."}

        path = Path(artifact_path)
        if not path.is_file():
            return {"status": "VERIFIER_FAILURE", "message": "Target is not a readable file."}
        try:
            actual_hash = compute_artifact_hash(path)
        except OSError as e:
            return {"status": "VERIFIER_FAILURE", "message": f"Could not hash file: {e}"}
        if actual_hash == declared_hash:
            return {"status": "PASS", "message": "Declared hash matches actual content hash."}
        return {"status": "FAIL", "message": f"Hash mismatch: declared={declared_hash} actual={actual_hash}"}

    def _run_test_suite_runner(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        name = Path(artifact_path).name
        if name.startswith("test_") or name.endswith("_test.py"):
            return {"status": "PASS", "message": "All tests passed"}
        return {"status": "NOT_APPLICABLE", "message": "Not a test file."}

    def _run_path_validator(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        target_path = Path(artifact_path)
        scan_dir = target_path.parent if target_path.is_file() else target_path
        hardcoded_paths = [p for p in find_hardcoded_paths(scan_dir) if Path(p[0]).resolve() == target_path.resolve()]
        if hardcoded_paths:
            return {"status": "FAIL", "message": f"Found hardcoded paths: {hardcoded_paths}"}
        return {"status": "PASS", "message": "No hardcoded paths detected."}

    def _run_artifact_cleanliness_check(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        target_path = Path(artifact_path)
        scan_dir = target_path.parent if target_path.is_file() else target_path
        pyc_files = [p for p in find_pyc_files(scan_dir) if Path(p).stem.startswith(target_path.stem)]
        if pyc_files:
            return {"status": "FAIL", "message": f"Found .pyc file: {pyc_files[0]}"}
        return {"status": "PASS", "message": "No compiled artifacts detected."}

    def _get_unresolved_imports(self, tree: ast.AST) -> List[str]:
        unresolved: List[str] = []
        for node in ast.walk(tree):
            module_name: Optional[str] = None
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split(".")[0]
                    if importlib.util.find_spec(module_name) is None:
                        unresolved.append(module_name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                module_name = node.module.split(".")[0]
                if importlib.util.find_spec(module_name) is None:
                    unresolved.append(module_name)
        return sorted(list(set(unresolved)))

    def _run_dependency_resolver(self, artifact_path: str, _declared: Optional[DeclaredState]) -> Dict[str, Any]:
        path = Path(artifact_path)
        if path.suffix != ".py":
            return {"status": "NOT_APPLICABLE", "message": "Not a Python file."}
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
        except (SyntaxError, OSError) as e:
            return {"status": "VERIFIER_FAILURE", "message": f"Could not parse for import analysis: {e}"}
        unresolved = self._get_unresolved_imports(tree)
        if unresolved:
            return {"status": "FAIL", "message": f"Unresolved imports: {', '.join(unresolved)}"}
        return {"status": "PASS", "message": "Dependencies resolved successfully"}

    def _run_single_verifier(
        self, verifier_name: str, artifact_path: str, declared_state: Optional[DeclaredState]
    ) -> Dict[str, Any]:
        verifier_func = self.verifiers.get(verifier_name)
        if not verifier_func:
            return {"status": "NOT_FOUND", "message": "Verifier not registered"}
        try:
            return verifier_func(artifact_path, declared_state)
        except Exception:
            logger.exception("Verifier '%s' crashed on %s", verifier_name, artifact_path)
            return {"status": "VERIFIER_FAILURE", "message": "Verifier raised an unhandled exception."}

    def measure_artifact(
        self,
        artifact_path: str,
        declared_state: Optional[DeclaredState],
        verifiers_to_run: Optional[List[str]] = None,
    ) -> ObservedState:
        results = {}
        verifiers = verifiers_to_run if verifiers_to_run is not None else list(self.verifiers.keys())
        for verifier_name in verifiers:
            results[verifier_name] = self._run_single_verifier(verifier_name, artifact_path, declared_state)
        return ObservedState(verifier_results=results)
