"""
artifact_anchor:
  id: GVRN.COMPILER.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Phase 5 & 9: Compilation and Export Engine
# Compiles the canonical Topological Intermediate Representation (IR) and serializes the JSON knowledge graph

import os
import json
import datetime
from .lexicon import ONTOLOGICAL_LEXICON

class TopologyCompiler:
    def __init__(self, target_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.registry = {}

    def register_node(self, artifact_id: str, metadata: dict, rel_path: str):
        """Stores standard metadata node mapping in the compiler registry."""
        node_entry = metadata.copy()
        node_entry["rel_path"] = rel_path.replace("\\", "/")
        self.registry[artifact_id] = node_entry

    def compile_graph_representation(self, errors: list, warnings: list) -> dict:
        """Constructs the canonical Intermediate Representation mapping nodes, edges, and semantic lexicon."""
        graph_nodes = []
        graph_edges = []

        for node_id, data in self.registry.items():
            graph_nodes.append({
                "id": node_id,
                "path": data.get("rel_path"),
                "domain": data.get("domain"),
                "tier": data.get("tier"),
                "state": data.get("state"),
                "ethos": data.get("ethos")
            })
            for rel in data.get("relations", []):
                graph_edges.append({
                    "source": node_id,
                    "target": rel.get("node"),
                    "type": rel.get("type")
                })

        return {
            "metadata": {
                "generated_at": datetime.datetime.now().isoformat(),
                "total_nodes": len(graph_nodes),
                "total_edges": len(graph_edges),
                "referential_integrity_issues": len(errors),
                "circular_loops": len(warnings)
            },
            "nodes": graph_nodes,
            "edges": graph_edges,
            # Embed the Ontological Lexicon directly inside the Intermediate Representation (IR)
            "lexicon": ONTOLOGICAL_LEXICON,
            "diagnostics": {
                "errors": errors,
                "warnings": warnings
            }
        }

    def export_ir_json(self, errors: list, warnings: list) -> str:
        """Serializes and saves the Intermediate Representation graph file to the workspace."""
        graph_model = self.compile_graph_representation(errors, warnings)
        graph_file_path = os.path.join(self.target_dir, "_governance", "tools", "repository_graph.json")
        
        try:
            os.makedirs(os.path.dirname(graph_file_path), exist_ok=True)
            with open(graph_file_path, "w", encoding="utf-8") as f:
                json.dump(graph_model, f, indent=2)
            return graph_file_path
        except Exception as e:
            raise IOError(f"Failed to export Intermediate Representation graph file: {e}")
