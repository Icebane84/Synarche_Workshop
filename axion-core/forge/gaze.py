"""CORE-HEPH-GAZE-001 (gaze.py)
Status: [CANONIZED]
Genesis Stamp: 2026-03-07.

**The Spirit Bomb Axiom: Architectural Calculus (Law 28)**
> Implemented from Blueprint `GVRN.REG.DependencyGraph.md`.
> Ethos: Omniscient Sight, Structural Cohesion.
"""

import ast
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

# Hephaestus Lib Imports
from weaver import CatalystWeaver

# Configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class GazeDependencyMapper:
    """Map and visualize the architectural dependency graph of the workspace."""

    def __init__(self) -> None:
        """Initialize the Gaze mapper and semantic weaver."""
        self.nodes: set[str] = set()
        self.edges: list[dict[str, str]] = []
        self.imports_by_file: dict[str, list[str]] = defaultdict(list)
        self.weaver = CatalystWeaver()

    def trace_semantic_web(self, artifact_a: dict, artifact_b: dict) -> Any:
        """Calculate the semantic synergy between two artifacts."""
        return self.weaver.weave(artifact_a, artifact_b)

    def scan_directory(self, target_dir: str) -> None:
        """Scan a directory to build the global dependency map."""
        path = Path(target_dir)
        for py_file in path.rglob("*.py"):
            self._process_file(py_file)

    def _process_file(self, file_path: Path) -> None:
        """Extract import relationships from a single Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=str(file_path))
        except Exception as e:
            logger.warning(f"Gaze failed to parse {file_path}: {e}")
            return

        module_name = file_path.stem
        self.nodes.add(module_name)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._add_edge(module_name, alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._add_edge(module_name, node.module)

    def _add_edge(self, source: str, target: str) -> None:
        """Register a dependency edge."""
        target_base = target.split(".")[0]

        self.nodes.add(target_base)
        self.edges.append({"source": source, "target": target_base})
        self.imports_by_file[source].append(target)

    def export_graph_json(self) -> str:
        """Export the mapped graph securely to standard JSON format."""
        graph_data = {
            "nodes": [{"id": node} for node in sorted(list(self.nodes))],
            "links": self.edges,
            "raw_imports": dict(self.imports_by_file),
        }
        return json.dumps(graph_data, indent=2)


if __name__ == "__main__":
    gaze = GazeDependencyMapper()
    target_path = Path("c:/Users/Chris/Synarche_Workspace/axion-core/src")
    gaze.scan_directory(str(target_path))
    print(gaze.export_graph_json())
