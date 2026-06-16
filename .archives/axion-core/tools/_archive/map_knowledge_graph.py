#!/usr/bin/env python3
"""# TOOL-MAP-001: Knowledge Graph Mapper (The Loom)
# Domain: MAP-M | State: CANONIZED | Criticality: High
# Objective: Visualize the Synarche Synthesis System (SSS) by crawling synergy blocks.
"""

import os
import re

import matplotlib.pyplot as plt
import networkx as nx
from enums import RelationType


class KnowledgeLoom:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.graph = nx.MultiDiGraph()
        self.synergy_pattern = re.compile(
            r"Synergistic Artifact ID\s*,\s*Relationship Type\s*,\s*Synergistic Impact"
        )

    def scan_artifacts(self):
        """Scans the directory for markdown artifacts and extracts synergy links."""
        print(f"[*] Initializing Loom Crawl in: {self.root_dir}")

        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    self._parse_artifact(os.path.join(root, file))

    def _parse_artifact(self, file_path):
        source_id = os.path.basename(file_path).replace(".md", "")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            # Identify the Synergy Table
            lines = content.splitlines()
            in_synergy_table = False
            for line in lines:
                if "Synergistic Artifact ID" in line:
                    in_synergy_table = True
                    continue

                if in_synergy_table and "," in line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        target_id = parts[0].strip().replace("`", "")  # Clean backticks
                        relation = parts[1].strip().upper()

                        # Validate Relation against enums
                        if relation in RelationType.__members__:
                            self.graph.add_edge(source_id, target_id, relation=relation)
                            print(
                                f" [OK] Linked: {source_id} --[{relation}]--> {target_id}"
                            )

    def visualize(self):
        """Generates a force-directed graph of the knowledge network."""
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)

        # Draw Nodes
        nx.draw_networkx_nodes(
            self.graph, pos, node_size=2000, node_color="skyblue", alpha=0.7
        )

        # Draw Edges
        nx.draw_networkx_edges(
            self.graph, pos, width=1.0, alpha=0.5, edge_color="gray", arrowsize=20
        )

        # Draw Labels
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_family="sans-serif")

        # Draw Edge Labels (Relations)
        edge_labels = nx.get_edge_attributes(self.graph, "relation")
        # Handle MultiGraph labels by simplifying for visualization
        simple_labels = {(u, v): r for (u, v, k), r in edge_labels.items()}
        nx.draw_networkx_edge_labels(
            self.graph, pos, edge_labels=simple_labels, font_size=8
        )

        plt.title("SSS Knowledge Loom: Architectural Connectivity Map", fontsize=15)
        plt.axis("off")
        print("[*] Loom Visualization Generated.")
        plt.show()


if __name__ == "__main__":
    # Define the library path relative to the tool location
    # Standardizing to point to the Library directory in the Vault
    library_path = "c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library"
    if not os.path.exists(library_path):
        library_path = "../Documentation/Library"

    loom = KnowledgeLoom(library_path)
    loom.scan_artifacts()

    if len(loom.graph.edges()) > 0:
        loom.visualize()
    else:
        print(
            "[!] No synergy links found. Ensure artifacts contain valid Synergy Tables."
        )
