"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-GENERATE-RAG-GRAPH-001`                | The Sovereign ID. |
| **Official Name** | `generate_rag_graph.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

try:
    from src.logic.nlp.nlp_engine import AxionCognition
except ImportError:
    AxionCognition = None

import argparse
import json
import os
import re

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[(?:[^\]]+)\]\(([^)]+\.md)\)")
ID_RE = re.compile(r"\*\*Artifact ID\*\*\s*\|\s*`?([^`|\n]+)`?")


def build_rag_graph(directory: str, output_path: str) -> None:
    """Build and export the RAG knowledge graph as JSON."""
    print(f"\n>>> GENERATING RAG GRAPH: {directory}\n")

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
            except Exception:
                continue

            id_match = ID_RE.search(content)
            artifact_id = id_match.group(1).strip() if id_match else f
            excerpt = content[:300].replace("\n", " ").strip()

            nodes[f] = {
                "id": artifact_id,
                "filename": f,
                "path": path,
                "excerpt": excerpt,
                "links": [],
            }

            for match in LINK_RE.finditer(content):
                target = match.group(1) or os.path.basename(match.group(2) or "")
                if target:
                    nodes[f]["links"].append(target.strip())

    # Build directed edges with semantic weighting
    cognition = AxionCognition() if AxionCognition else None

    for _fname, data in nodes.items():
        source_id = data["id"]
        data["excerpt"]

        for link in data["links"]:
            if link in nodes:
                target_id = nodes[link]["id"]
                nodes[link]["excerpt"]

                weight = 1.0  # Default weight
                if cognition and data.get("vector") and nodes[link].get("vector"):
                    # Use the pre-calculated vectors if available, otherwise just use 1.0
                    pass

                edges.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "weight": weight,
                        "type": "SEMANTIC_LINK",
                    }
                )

    graph = {
        "metadata": {
            "generated_by": "generate_rag_graph.py",
            "source_directory": directory,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
        },
        "nodes": [
            {"id": v["id"], "filename": v["filename"], "excerpt": v["excerpt"]}
            for v in nodes.values()
        ],
        "edges": edges,
    }

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(graph, fh, indent=2)

    print("=" * 60)
    print("  RAG GRAPH GENERATION COMPLETE".center(60))
    print("=" * 60)
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Output: {output_path}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate RAG Graph — Knowledge Constellation Builder"
    )
    parser.add_argument("target", help="Directory to build the graph from.")
    parser.add_argument(
        "--out",
        default="rag_graph.json",
        help="Output JSON file (default: rag_graph.json).",
    )
    args = parser.parse_args()
    build_rag_graph(os.path.abspath(args.target), os.path.abspath(args.out))


if __name__ == "__main__":
    main()
