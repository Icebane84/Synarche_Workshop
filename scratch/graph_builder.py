#!/usr/bin/env python3
"""
Phoenix Rosetta Stone (PRS-001) Knowledge Graph Ingestion Engine
V-Control: 2026-07-21T08:05:00Z
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

class PRSGraphBuilder:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.nodes_dir = self.root_dir / "nodes"
        self.index_dir = self.root_dir / "index"
        
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        self.validation_errors: List[str] = []

    def extract_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Extracts YAML frontmatter from a Markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not match:
            return {}
        
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            self.validation_errors.append(f"YAML Syntax Error in {file_path}: {e}")
            return {}

    def parse_nodes(self):
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
                "file_path": str(filepath.relative_to(self.root_dir)),
                "raw_edges": frontmatter.get("edges", [])
            }
            print(f"    Indexed [{label}] {node_id} -> {filepath.name}")

    def process_and_validate_edges(self):
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

                self.edges.append({
                    "source": source_id,
                    "target": target_id,
                    "relation": relation,
                    "properties": edge_props
                })

    def export_adjacency_matrix(self):
        """Exports the graph structure to index/adjacency_matrix.json."""
        self.index_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.index_dir / "adjacency_matrix.json"
        
        data = {
            "metadata": {
                "system": "PRS-001 Knowledge Graph",
                "v_control": "2026-07-21T08:05:00Z",
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "errors": len(self.validation_errors)
            },
            "nodes": self.nodes,
            "edges": self.edges,
            "validation_errors": self.validation_errors
        }
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Exported Adjacency Matrix: {out_path}")

    def export_cypher_script(self):
        """Generates Neo4j Cypher import commands for database synchronization."""
        out_path = self.index_dir / "cypher_import.cypher"
        lines = [
            "// Phoenix Rosetta Stone (PRS-001) Neo4j Ingestion Script",
            "// V-Control: 2026-07-21T08:05:00Z\n"
        ]

        # 1. Create Nodes
        for node_id, data in self.nodes.items():
            label = data['label']
            props = {
                "id": data['id'],
                "name": data['name'],
                "canonical_status": data['canonical_status'],
                "file_path": data['file_path']
            }
            props.update(data['properties'])
            
            # Format properties as Cypher string
            prop_str = ", ".join([f"`{k}`: {json.dumps(v)}" for k, v in props.items()])
            lines.append(f"CREATE (:{label} {{{prop_str}}});")

        lines.append("\n// Create Relationships")
        
        # 2. Create Edges
        for edge in self.edges:
            src = edge['source']
            tgt = edge['target']
            rel = edge['relation']
            props = edge['properties']
            
            prop_str = f" {{{', '.join([f'`{k}`: {json.dumps(v)}' for k, v in props.items()])}}}" if props else ""
            lines.append(
                f"MATCH (a {{id: '{src}'}}), (b {{id: '{tgt}'}}) "
                f"CREATE (a)-[:{rel}{prop_str}]->(b);"
            )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"[+] Exported Neo4j Cypher Script: {out_path}")

    def run(self):
        self.parse_nodes()
        self.process_and_validate_edges()
        
        if self.validation_errors:
            print("\n[!] VALIDATION ERRORS DETECTED:")
            for err in self.validation_errors:
                print(f"    - {err}")
        else:
            print("\n[✓] Graph Integrity Verified: Zero Drift Detected.")

        self.export_adjacency_matrix()
        self.export_cypher_script()

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    builder = PRSGraphBuilder(root)
    builder.run()