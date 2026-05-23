#!/usr/bin/env python3
"""
# TOOL-MAP-001: Knowledge Graph Mapper (The Loom)
# Domain: MAP-M | State: CANONIZED | Criticality: High
# Objective: Visualize the Synarche Synthesis System (SSS) by crawling synergy blocks.
"""

import argparse
import logging
import re
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import networkx as nx

    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    # Define dummy nx if needed or handle logic check later
    # Ideally we need nx for the graph data structure even if not plotting
    # If nx is missing, the whole tool fails. But nx is usually easier to install than mpl.
    # Let's assume nx might be missing too.
    try:
        import networkx as nx
    except ImportError:
        nx = None

# --- Dynamic Import Setup ---
# Add axion-core root to sys.path to allow imports from src
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent  # axion-core
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    from src.logic.enums import RelationType
except ImportError as e:
    print(f"[!] Critical Import Error: {e}")
    # Fallback for standalone debugging if valid path isn't found
    RelationType = None  # Handle gracefully in logic

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("loom")


class KnowledgeLoom:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.graph = nx.MultiDiGraph()
        # Regex to detect the start of a Synergy Block table
        self.synergy_pattern = re.compile(
            r"Synergistic Artifact ID\s*,\s*Relationship Type\s*,\s*Synergistic Impact", re.IGNORECASE
        )

    def scan_artifacts(self):
        """Scans the directory for markdown artifacts and extracts synergy links."""
        logger.info(f"[*] Initializing Loom Crawl in: {self.root_dir}")

        if not self.root_dir.exists():
            logger.error(f"[!] Error: Directory not found: {self.root_dir}")
            return

        count = 0
        for file_path in self.root_dir.rglob("*.md"):
            self._parse_artifact(file_path)
            count += 1

        logger.info(f"[*] Scanned {count} artifacts.")

    def _parse_artifact(self, file_path: Path):
        source_id = file_path.stem
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            lines = content.splitlines()
            in_synergy_table = False

            for line in lines:
                # Detect Table Header
                if self.synergy_pattern.search(line):
                    in_synergy_table = True
                    continue

                # Stop if we hit a new section or empty line after table started?
                # Markdown tables usually end with blank newline, but robust parsing detects content.
                # Here we assume table lines follow header.

                if in_synergy_table and "," in line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        target_id = parts[0].strip().replace("`", "")  # Clean backticks
                        relation = parts[1].strip().upper()

                        # Validate Relation against enums if available
                        if RelationType and relation in RelationType.__members__:
                            self.graph.add_edge(source_id, target_id, relation=relation)
                            logger.debug(f" [OK] Linked: {source_id} --[{relation}]--> {target_id}")
                        elif not RelationType:
                            # Permissive mode if enums fail to load
                            self.graph.add_edge(source_id, target_id, relation=relation)
                            logger.debug(f" [OK] Linked (Unchecked): {source_id} --[{relation}]--> {target_id}")

        except Exception as e:
            logger.warning(f"[!] Failed to parse {file_path.name}: {e}")

    def visualize(self, save_path: Path = None, show: bool = True):
        """Generates a force-directed graph of the knowledge network."""
        if self.graph is None or self.graph.number_of_edges() == 0:
            logger.warning("[!] No edges to visualize.")
            return

        if not VISUALIZATION_AVAILABLE:
            logger.warning("[!] Matplotlib not installed. Visualization skipped.")
            logger.info(f"[*] Graph Stats: {self.graph.number_of_nodes()} Nodes, {self.graph.number_of_edges()} Edges")
            return

        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(self.graph, k=0.6, iterations=50, seed=42)

        # Draw Nodes
        nx.draw_networkx_nodes(self.graph, pos, node_size=2500, node_color="skyblue", alpha=0.8)

        # Draw Edges
        nx.draw_networkx_edges(
            self.graph, pos, width=1.5, alpha=0.6, edge_color="gray", arrowsize=20, connectionstyle="arc3,rad=0.1"
        )

        # Draw Labels
        nx.draw_networkx_labels(self.graph, pos, font_size=9, font_family="sans-serif", font_weight="bold")

        # Draw Edge Labels (Relations) - Simplified for MultiDiGraph
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            if "relation" in data:
                edge_labels[(u, v)] = data["relation"]

        # Only draw a subset or distinct labels to avoid clutter
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=7, label_pos=0.3)

        plt.title(
            f"SSS Knowledge Loom: Architectural Connectivity Map ({self.graph.number_of_nodes()} Nodes, {self.graph.number_of_edges()} Links)",
            fontsize=16,
        )
        plt.axis("off")

        if save_path:
            plt.savefig(save_path, format="png", dpi=300, bbox_inches="tight")
            logger.info(f"[*] Graph saved to: {save_path}")

        if show:
            logger.info("[*] Displaying Graph UI...")
            plt.show()
        else:
            plt.close()


def main():
    parser = argparse.ArgumentParser(description="TOOL-MAP-001: Knowledge Graph Mapper")
    parser.add_argument(
        "--target", "-t", type=str, help="Target directory to scan (default: auto-detect)", default=None
    )
    parser.add_argument("--save", "-s", type=str, help="Path to save the graph image (e.g., graph.png)", default=None)
    parser.add_argument("--no-show", action="store_true", help="Do not display the interactive graph window")
    args = parser.parse_args()

    # Auto-detect target if not provided
    if args.target:
        target_path = Path(args.target).resolve()
    else:
        # Default to Governance/Protocols or Workspace Root relative to script
        # Assuming script is in axion-core/tools/
        # Try to find _governance directory
        workspace_root = PROJECT_ROOT.parent  # Synarche_Workspace
        target_path = workspace_root / "_governance"
        if not target_path.exists():
            target_path = workspace_root  # Fallback to scan everything

    logger.info(f"Target Path: {target_path}")

    loom = KnowledgeLoom(target_path)
    loom.scan_artifacts()

    if len(loom.graph.edges()) > 0:
        save_file = Path(args.save) if args.save else None
        loom.visualize(save_path=save_file, show=not args.no_show)
    else:
        logger.warning("[!] No synergy links found. Ensure artifacts contain valid Synergy Tables.")


if __name__ == "__main__":
    main()
