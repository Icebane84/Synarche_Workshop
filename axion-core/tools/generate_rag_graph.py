"""# TOOL-STAR-004: RAG Graph Generator (Coherence Filter).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-STAR-004`                                          |
| **2. Official Name**   | `generate_rag_graph.py`                                  |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Knowledge Synthesis**                                  |
| **11. Catalyst**       | **Graph Generation**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Star persona uses this tool for graph generation.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-HPRI-006, POWERED_BY, This tool uses Catalyst Weaver for link logic.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Coherence Filter (The Star)
# Synergy Set: The Star's Radiance
# Primary Stat Buff: Perception (+15), Intelligence (+10)
# Passive Ability: Constellation Map (Graph Synthesis)
# Cognitive Load Cost: High
# XP Award Value: 150 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: GENERATE_GRAPH` | Build RAG Knowledge Graph | Semantic Navigation |
| `⚡ EXECUTE: BUILD_LOOM` | Full Documentation Scan | Coherence Mapping |

---

Parses the Phoenix Documentation to generate a structured Knowledge Graph + Vector Chunks dataset.
Outputs: phoenix_knowledge_graph.json
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import TypedDict

# Ensure tools can import siblings
sys.path.append(str(Path(__file__).parent))
try:
    from catalyst_weaver import CatalystWeaver
except ImportError:
    # Fallback if running from root
    from tools.catalyst_weaver import CatalystWeaver

# Configuration
DEFAULT_SEARCH_DIRS = ["Documentation", "docs", "axion-core/docs"]
OUTPUT_FILE = "phoenix_knowledge_graph.json"
OSLM_PATH = "UMB-OSLM-001_PPLGraphOutline_v11.0.md"

# Regex
# Matches standard Artifact IDs (e.g., UMB-OSLM-001, AOP-PGPS-001, CODEX-001)
ARTIFACT_ID_REGEX = r"[A-Z]{3,}(?:-[A-Z0-9]+)+"
HEADER_REGEX = r"^(#{1,3})\s+(.*)"
LINK_REGEX = r"\[([^\]]+)\]\(([^\)]+)\)"
WIKI_LINK_REGEX = r"\[\[(.*?)\]\]"
# Matches: | Source | Relation | Target | (Optimized for performance)
OSLM_TABLE_ROW_REGEX = r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
MERMAID_EDGE_REGEX = r"(\w+|\[[^\]]+\])\s*-+>\|?([^|]*)\|?\s*(\w+|\[[^\]]+\])"


class GraphNode(TypedDict):
    id: str  # Unique Artifact ID or Filepath if no ID
    type: str  # "Artifact" or "Chunk"
    content: str  # Text content
    metadata: dict  # file_path, source_id, chunk_header


class GraphEdge(TypedDict):
    source: str  # Source Node ID
    target: str  # Target Node ID
    relation: str  # Relationship Type (e.g., "REFERENCES", "GOVERNS")
    metadata: dict  # rationale, score


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []
        self.id_map: dict[str, str] = {}  # filename -> artifact_id mapping

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node["id"]] = node

    def add_edge(
        self, source: str, target: str, relation: str, metadata: dict | None = None
    ) -> None:
        if metadata is None:
            metadata = {}
        self.edges.append(
            {
                "source": source,
                "target": target,
                "relation": relation,
                "metadata": metadata,
            }
        )


def parse_oslm(root_dir: Path, search_dirs: list[str], graph: KnowledgeGraph) -> None:
    """Parses OSLM for explicit high-fidelity edges."""
    oslm_file = None

    # 1. Search in root first
    candidates = [root_dir / OSLM_PATH]

    # 2. Search in all search_dirs
    for d in search_dirs:
        path = Path(d)
        if not path.is_absolute():
            path = root_dir / d
        candidates.append(path / OSLM_PATH)

    # 3. Find the first one that exists
    for c in candidates:
        if c.exists():
            oslm_file = c
            break

    # 4. Fallback A: Recursive exact search for OSLM_PATH in search_dirs
    if not oslm_file:
        for d in search_dirs:
            path = Path(d)
            if not path.is_absolute():
                path = root_dir / d
            if path.exists():
                found = list(path.rglob(OSLM_PATH))
                if found:
                    oslm_file = found[0]
                    break

    # 5. Fallback B: Fuzzy search in search_dirs
    if not oslm_file:
        for d in search_dirs:
            path = Path(d)
            if not path.is_absolute():
                path = root_dir / d
            if path.exists():
                found = list(path.rglob("UMB-OSLM-001*.md"))
                if found:
                    oslm_file = found[0]
                    break

    if not oslm_file:
        print(
            "[WARN] UMB-OSLM-001 not found in any search path. Skipping explicit edge parsing."
        )
        return

    print(f"Parsing Explicit Edges from {oslm_file.name}...")
    try:
        content = oslm_file.read_text(encoding="utf-8", errors="ignore")
        count = 0

        # 1. Parse Markdown Tables (With Line Buffering for Wrapped Rows)
        lines = content.splitlines()
        buffer = ""

        def process_buffer(buf):
            nonlocal count
            if not buf:
                return

            # Clean buffer
            buf = buf.replace("\n", " ")
            parts = buf.split("|")

            # We need at least Src, Rel, Tgt (parts[1], parts[2], parts[3])
            if len(parts) >= 4:
                raw_src = parts[1]
                raw_rel = parts[2]
                raw_tgt = parts[3]

                # Extract IDs
                src_match = re.search(ARTIFACT_ID_REGEX, raw_src)
                tgt_match = re.search(ARTIFACT_ID_REGEX, raw_tgt)

                if src_match and tgt_match:
                    src = src_match.group(0)
                    tgt = tgt_match.group(0)
                    rel = raw_rel.strip().replace("`", "").replace("*", "")

                    if rel and rel.lower() != "relation":
                        graph.add_edge(src, tgt, rel, {"type": "explicit_oslm_table"})
                        count += 1

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("|") and "---" not in stripped:
                # New row starts -> process previous buffer
                process_buffer(buffer)
                buffer = stripped
            else:
                # Continuation of previous row
                buffer += " " + stripped

        # Process remaining buffer
        process_buffer(buffer)

        # 2. Parse Mermaid Graphs (DISABLED - CAUSING HANG)
        # mermaid_matches = re.findall(MERMAID_EDGE_REGEX, content)
        # for m in mermaid_matches:
        #      # parsing node[ID] or Alias[ID] or ID
        #      src_raw = m[0]
        #      rel_raw = m[1]
        #      tgt_raw = m[2]
        #
        #      src_id_match = re.search(ARTIFACT_ID_REGEX, src_raw)
        #      tgt_id_match = re.search(ARTIFACT_ID_REGEX, tgt_raw)
        #
        #      if src_id_match and tgt_id_match:
        #          src = src_id_match.group(0)
        #          tgt = tgt_id_match.group(0)
        #          rel = rel_raw.strip()
        #          graph.add_edge(src, tgt, rel, {"type": "explicit_oslm_mermaid"})
        #          count += 1

        print(f"   Extracted {count} OSLM Relationships.")
    except Exception as e:
        print(f"[ERROR] Error parsing OSLM: {e}")


def extract_artifact_id(f: Path, content: str) -> str:
    """Extracts or derives the Artifact ID from filename or content."""
    match = re.search(ARTIFACT_ID_REGEX, f.name)
    if match:
        return match.group(0)

    header_match = re.search(
        r"^#\s*(" + ARTIFACT_ID_REGEX + r")", content, re.MULTILINE
    )
    return header_match.group(1) if header_match else f.name


def parse_chunks(content: str) -> tuple[list[str], list[str]]:
    """Splits content into chunks and headers."""
    lines = content.splitlines()
    chunks: list[str] = []
    headers: list[str] = []
    current_chunk: list[str] = []
    current_header = "ROOT"

    for line in lines:
        if re.match(HEADER_REGEX, line):
            if current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                headers.append(current_header)
            current_chunk = [line]
            current_header = line.strip().lstrip("#").strip()
        else:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())
        headers.append(current_header)

    return chunks, headers


def process_file(f: Path, graph: KnowledgeGraph) -> None:
    try:
        content = f.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return

    artifact_id = extract_artifact_id(f, content)
    graph.id_map[f.name] = artifact_id

    graph.add_node(
        {
            "id": artifact_id,
            "type": "Artifact",
            "content": content[:500] + "...",
            "metadata": {"filepath": str(f)},
        }
    )

    chunks, headers = parse_chunks(content)

    for idx, text in enumerate(chunks):
        if not text:
            continue

        chunk_id = f"{artifact_id}#chunk-{idx}"
        graph.add_node(
            {
                "id": chunk_id,
                "type": "Chunk",
                "content": text,
                "metadata": {
                    "source_id": artifact_id,
                    "header": headers[idx],
                    "filepath": str(f),
                },
            }
        )
        graph.add_edge(chunk_id, artifact_id, "PART_OF")

        refs = re.findall(ARTIFACT_ID_REGEX, text)
        for ref in set(refs):
            if ref != artifact_id:
                graph.add_edge(chunk_id, ref, "MENTIONS")
                graph.add_edge(artifact_id, ref, "REFERENCES")


def main() -> None:
    """CLI Entrypoint."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("rag_gen")

    root = Path.cwd()
    if root.name == "tools":
        root = root.parent

    logger.info(f"🌟 Starting RAG Graph Generation in {root}")
    parser = argparse.ArgumentParser(description="Generate RAG Graph")
    parser.add_argument(
        "--search-dir", action="append", help="Additional directory to search"
    )
    parser.add_argument("--output", help="Output filename", default=OUTPUT_FILE)
    parser.add_argument(
        "--weave", action="store_true", help="Enable Catalyst Weaver synergy generation"
    )
    args = parser.parse_args()

    search_dirs = list(DEFAULT_SEARCH_DIRS)
    if args.search_dir:
        search_dirs.extend(args.search_dir)

    logger.info(f"[*] Starting RAG Graph Generation in {root}")
    logger.info(f"   Target Directories: {search_dirs}")
    graph = KnowledgeGraph()

    files = []
    for d in search_dirs:
        # Check if d is absolute or relative
        path = Path(d)
        if not path.is_absolute():
            path = root / d

        if path.exists():
            found = list(path.rglob("*.md"))
            files.extend(found)
            logger.info(f"   Using {path} ({len(found)} files)")
        else:
            logger.warning(f"   Skipping missing directory: {path}")

    logger.info(f"   Processing {len(files)} files...")
    for f in files:
        process_file(f, graph)

    parse_oslm(root, search_dirs, graph)

    if args.weave:
        logger.info("\n[+] CATALYST WEAVER ENABLED")
        # Convert graph storage to format expected by Weaver
        nodes_list = list(graph.nodes.values())
        edges_list = graph.edges  # Reference

        weaver = CatalystWeaver(graph_path=None, nodes=nodes_list, edges=edges_list)
        new_edges = weaver.weave_all()

        logger.info(f"   Injecting {len(new_edges)} synergy links into graph...")
        graph.edges.extend(new_edges)

    output_path = root / args.output
    data = {
        "nodes": list(graph.nodes.values()),
        "edges": graph.edges,
        "stats": {
            "total_nodes": len(graph.nodes),
            "total_edges": len(graph.edges),
            "total_files": len(files),
        },
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info("\n" + "=" * 40)
    logger.info("GRAPH GENERATION COMPLETE")
    logger.info(f"Nodes: {data['stats']['total_nodes']}")
    logger.info(f"Edges: {data['stats']['total_edges']}")
    logger.info(f"Output: {output_path}")
    logger.info("=" * 40)


if __name__ == "__main__":
    main()
