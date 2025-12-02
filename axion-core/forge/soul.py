"""CORE-HEPH-SOUL-001 (soul.py)
Status: [CANONIZED]
Genesis Stamp: 2026-03-07.

**The Spirit Bomb Axiom: Architectural Empathy (Law 28)**
> Implemented from Blueprint `GVRN.REG.ImpactAnalysis.md`.
> Ethos: Empathy for the Engine, Blast Radius Awareness.
"""

import ast
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

# Hephaestus Lib Imports
# Stub for missing emotion_analyzer
class EmotionAnalyzer:
    def detect_emotions(self, text: str) -> dict[str, float]:
        return {"coherence": 0.9, "entropy": 0.1}


# Configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# OMEGA Standard Directory References
WORKSPACE_ROOT = Path("c:/Users/Chris/Synarche_Workspace")
CORE_DIR = WORKSPACE_ROOT / "axion-core"
SRC_DIR = CORE_DIR / "src"
AGENTS_DIR = SRC_DIR / "agents"
TOOLS_DIR = CORE_DIR / "tools"
UMB_DIR = CORE_DIR / "umbrella"


class SoulImpactAnalyzer:
    """Analyze the impact of modifying a specific node across the workspace."""

    def __init__(self) -> None:
        """Initialize the blast radius analyzer and emotion engine."""
        self.dependency_graph: dict[str, set[str]] = defaultdict(set)
        self.reverse_dependency_graph: dict[str, set[str]] = defaultdict(set)
        self.known_symbols: dict[str, str] = {}
        self.emotion_engine = EmotionAnalyzer()

    def calculate_narrative_resonance(self, text: str) -> dict[str, float]:
        """Detect the emotional tone and resonance of the provided text."""
        return self.emotion_engine.detect_emotions(text)

    def map_domain(self, target_directory: str) -> None:
        """Scan a directory and build the dependency graph mapping."""
        target_path = Path(target_directory)
        if not target_path.exists():
            logger.error(f"Target directory {target_path} does not exist.")
            return

        for py_file in target_path.rglob("*.py"):
            self._analyze_file(py_file)

    def _analyze_file(self, file_path: Path) -> None:
        """Parse a single Python file to extract its imports and defined symbols."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            logger.warning(f"SyntaxError parsing {file_path}. Skipping.")
            return
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
            return

        module_name = self._get_module_name(file_path)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.known_symbols[node.name] = module_name
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.dependency_graph[module_name].add(alias.name)
                    self.reverse_dependency_graph[alias.name].add(module_name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                self.dependency_graph[module_name].add(node.module)
                self.reverse_dependency_graph[node.module].add(module_name)
                for alias in node.names:
                    full_name = f"{node.module}.{alias.name}"
                    self.dependency_graph[module_name].add(full_name)
                    self.reverse_dependency_graph[full_name].add(module_name)

    def _get_module_name(self, file_path: Path) -> str:
        """Construct a module-like name from a file path relative to the workspace."""
        try:
            rel_path = file_path.relative_to(WORKSPACE_ROOT)
            return rel_path.with_suffix("").as_posix().replace("/", ".")
        except ValueError:
            return file_path.stem

    def calculate_blast_radius(self, target_node: str) -> dict[str, Any]:
        """Calculate the cascading impact of modifying the target node."""
        affected_modules: set[str] = set()
        queue = [target_node]
        visited: set[str] = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            affected_modules.add(current)

            # Find all modules that depend on 'current'
            implicating_modules = self.reverse_dependency_graph.get(current, set())
            queue.extend([m for m in implicating_modules if m not in visited])

            # Also check if the node is a symbol known to be in a specific module
            if current in self.known_symbols:
                parent_module = self.known_symbols[current]
                if parent_module not in visited:
                    queue.append(parent_module)

        return {
            "target": target_node,
            "blast_radius_size": len(affected_modules),
            "affected_modules": sorted(list(affected_modules)),
            "risk_level": self._assess_risk(len(affected_modules)),
        }

    def _assess_risk(self, radius_size: int) -> str:
        """Assign a risk category based on the number of affected modules."""
        if radius_size == 0:
            return "NO_IMPACT"
        elif radius_size <= 3:
            return "LOW"
        elif radius_size <= 10:
            return "MEDIUM"
        else:
            return "HIGH (Requires Architectural Review)"


if __name__ == "__main__":
    # Example standalone execution for testing the "Soul" mechanic
    analyzer = SoulImpactAnalyzer()
    analyzer.map_domain(str(CORE_DIR))

    # Example check
    test_node = "axion-core.src.hephaestus.soul"
    result = analyzer.calculate_blast_radius(test_node)

    print(json.dumps(result, indent=2))
