#!/usr/bin/env python3
"""
Phoenix Rosetta Stone (PRS-001) Knowledge Graph Ingestion Engine
Modified for Autobattler Database Generation.
"""
# cspell:ignore Autobattler

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml


class PRSGraphBuilder:
    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)
        # Target the WLF nodes directory
        self.nodes_dir = Path("c:/Users/Chris/Synarche_Workspace/where_light_fades/where_light_fades/nodes")
        # Output directly into the Rosetta Stone React src/data directory
        self.index_dir = self.root_dir / "src" / "data"

        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.validation_errors: List[str] = []

    def extract_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Extracts YAML frontmatter from a Markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    return yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError as e:
                    self.validation_errors.append(f"YAML Syntax Error in {file_path}: {e}")
                    return {}

        return {}

    def parse_nodes(self) -> None:
        """Scans the nodes directory and indexes every valid Node ID."""
        print("[*] Stage 1: Indexing Nodes...")
        if not self.nodes_dir.exists():
            raise FileNotFoundError(f"Directory missing: {self.nodes_dir}")

        for filepath in self.nodes_dir.rglob("*.md"):
            frontmatter = self.extract_frontmatter(filepath)
            node_id = frontmatter.get("id")

            if not node_id:
                continue

            label = frontmatter.get("label", filepath.parent.name.capitalize())

            self.nodes[node_id] = {
                "id": node_id,
                "label": label,
                "name": frontmatter.get("name", filepath.stem),
                "aliases": frontmatter.get("aliases", []),
                "canonical_status": frontmatter.get("canonical_status", "Draft"),
                "properties": frontmatter.get("properties", {}),
                "file_path": str(filepath.relative_to(self.nodes_dir.parent)),
                "raw_edges": frontmatter.get("edges", []),
            }
            print(f"    Indexed [{label}] {node_id} -> {filepath.name}")

    def process_and_validate_edges(self) -> None:
        """Validates all directed edges against indexed node IDs."""
        print("[*] Stage 2: Processing & Validating Edges...")
        for source_id, node_data in self.nodes.items():
            raw_edges = node_data.pop("raw_edges", [])
            for edge in raw_edges:
                target_id = edge.get("target")
                relation = edge.get("relation", "RELATED_TO")
                edge_props = edge.get("properties", {})

                # Integrity Check: Target Must Exist
                if target_id not in self.nodes:
                    self.validation_errors.append(
                        f"DRIFT ERROR: Node '{source_id}' references non-existent target '{target_id}' via '{relation}'"
                    )
                    continue

                self.edges.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "relation": relation,
                        "properties": edge_props,
                    }
                )

    def export_adjacency_matrix(self) -> None:
        """Exports the graph structure to index/adjacency_matrix.json."""
        self.index_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.index_dir / "adjacency_matrix.json"

        data = {
            "metadata": {
                "system": "Ashen Oath Graph Database",
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "errors": len(self.validation_errors),
            },
            "nodes": self.nodes,
            "edges": self.edges,
            "validation_errors": self.validation_errors,
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Exported Adjacency Matrix: {out_path}")

    def run(self) -> None:
        self.parse_nodes()
        self.process_and_validate_edges()

        if self.validation_errors:
            print("\n[!] VALIDATION ERRORS DETECTED:")
            for err in self.validation_errors:
                print(f"    - {err}")
        else:
            print("\n[PASS] Graph Integrity Verified: Zero Drift Detected.")

        self.export_adjacency_matrix()


if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    builder = PRSGraphBuilder(root)
    builder.run()
