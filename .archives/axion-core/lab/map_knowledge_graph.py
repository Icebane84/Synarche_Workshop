"""Block A: Universal Identification & Provenance (UIP-V15)
Artifact ID: LAB-MAP-001
Official Name: map_knowledge_graph.py
Patron Shard: THE_PHOENIX_GESTALT
Version: v15.0 [OMEGA]
Domain: LAB.SYNERGY
Celestial Class: [ASTEROID]
Status: [EXPERIMENTAL]
Integrity Hash: SYN-LAB-MAP-001
Relations: GOVERNED_BY: CORE-CODEX-001.
"""

import argparse
import os
import re


def build_knowledge_graph(workspace_dir: str, output_gv: str) -> None:
    """Crawls markdown files to extract QDL (Quad-Directional Links) and formats into Graphviz .gv."""
    nodes = set()
    edges = []

    # Regex for markdown links pulling out relationships
    # Example: [LINK-CAUSAL]: IPPD_Capability <- QUEST-VOID-REBUILD
    link_pattern = re.compile(
        r"\[LINK-(.*?)\]:\s*([^<>-]+?)\s*(<->|->|<-|\\leftrightarrow|\\rightarrow|\\leftarrow)\s*(.*)"
    )
    # Example: GOVERNED_BY: CORE-CODEX-001
    rel_pattern = re.compile(
        r"(GOVERNED_BY|CONTRIBUTES_TO|UTILIZES|RESONATES|ORCHESTRATES):\s*([A-Za-z0-9_.-]+)"
    )

    for root, dirs, files in os.walk(workspace_dir):
        # Exclude entropy
        dirs[:] = [
            d
            for d in dirs
            if d not in (".git", "node_modules", ".venv", "__pycache__", ".agent")
        ]

        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    current_node = file.replace(".md", "").strip()
                    nodes.add(current_node)

                    # 1. Search for standard block relationships
                    for rel_match in rel_pattern.finditer(content):
                        rel_type = rel_match.group(1).strip()
                        target = rel_match.group(2).strip()
                        # Clean markdown artifacts if any
                        target = target.replace("*", "").replace("]", "")
                        nodes.add(target)
                        edges.append((current_node, target, rel_type))

                    # 2. Search for inline Synergistic Links
                    for edge_match in link_pattern.finditer(content):
                        rel_type = edge_match.group(1).strip()
                        source = edge_match.group(2).strip()
                        direction = edge_match.group(3).strip()
                        target = edge_match.group(4).strip()

                        source = source.replace("\\", "").replace("*", "").strip()
                        target = target.replace("\\", "").replace("*", "").strip()

                        nodes.add(source)
                        nodes.add(target)

                        if "<-" in direction or "leftarrow" in direction:
                            edges.append((target, source, rel_type))
                        elif "->" in direction or "rightarrow" in direction:
                            edges.append((source, target, rel_type))
                        else:  # Bidirectional
                            edges.append((source, target, rel_type + "_BIDIRECT"))
                except Exception as e:
                    print(f"Failed to parse {file}: {e}")

    # Generate GV
    print(f"[LAB] Synthesizing graph with {len(nodes)} nodes and {len(edges)} edges...")
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_gv)), exist_ok=True)
        with open(output_gv, "w", encoding="utf-8") as f:
            f.write("digraph KnowledgeGraph {\\n")
            f.write(
                '  node [shape=box, style=filled, fillcolor="#2b2d42", fontcolor="#8d99ae", fontname="Courier"];\\n'
            )
            f.write(
                '  edge [color="#ef233c", fontcolor="#edf2f4", fontname="Courier", fontsize=10];\\n'
            )
            f.write('  bgcolor="#1a1b26";\\n\\n')

            for s, t, r in edges:
                dir_attr = ""
                if r.endswith("_BIDIRECT"):
                    dir_attr = 'dir="both", '
                    r = r.replace("_BIDIRECT", "")
                # Escape quotes
                s_esc = s.replace('"', "")
                t_esc = t.replace('"', "")
                f.write(f'  "{s_esc}" -> "{t_esc}" [{dir_attr}label="{r}"];\\n')
            f.write("}\\n")
        print(f"[LAB] Visualization matrix locked: {output_gv}")
    except Exception as e:
        print(f"[ERROR] Graph generation failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map Knowledge Graph for OMEGA v15.0")
    parser.add_argument(
        "--dir",
        default=r"c:\\Users\\Chris\\Synarche_Workspace",
        help="Workspace directory to map",
    )
    parser.add_argument(
        "--out",
        default=r"c:\\Users\\Chris\\Synarche_Workspace\\axion-core\\lab\\knowledge_graph.gv",
        help="Output .gv file path",
    )
    args = parser.parse_args()

    print("[LAB] Commencing Multi-Directional Link Crawl...")
    build_knowledge_graph(args.dir, args.out)
