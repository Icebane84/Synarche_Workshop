import json
import os
import shutil
from datetime import datetime

# --- CONFIGURATION ---
WORKSPACE_ROOT = r"c:\Users\Chris\Synarche_Workspace\axion-core"
DOCS_ROOT = r"c:\Users\Chris\_Desktop_Vault\Phoenix\Documentation"
TOOLS_ROOT = os.path.join(WORKSPACE_ROOT, "tools")

# Input Paths (Priority ordered: last one overwrites previous for generic fields)
INPUT_GRAPHS = [
    r"c:\Users\Chris\Synarche_Workspace\axion-core\woven_graph.json",
    r"c:\Users\Chris\Synarche_Workspace\axion-core\standardized_graph.json",
    r"c:\Users\Chris\Synarche_Workspace\axion-core\verified_graph.json",
    # Phoenix Knowledge Graphs (Legacy/Backup)
    r"c:\Users\Chris\Synarche_Workspace\axion-core\phoenix_knowledge_graph.json",
    r"c:\Users\Chris\_Desktop_Vault\Phoenix\Documentation\_archive\phoenix_knowledge_graph.json",
]

# PRS Logic (The Master Index)
PRS_PATH = r"c:\Users\Chris\Synarche_Workspace\axion-core\PRS-001.json"

# Output Paths
DEFINITIVE_GRAPH_PATH = os.path.join(WORKSPACE_ROOT, "definitive_graph.json")


def load_json(path):
    if not os.path.exists(path):
        print(f"Warning: File not found {path}")
        return {"nodes": [], "edges": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {"nodes": [], "edges": []}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {path}")


def merge_nodes(master_nodes, new_nodes, priority="low"):
    """
    Merges new_nodes into master_nodes dict (keyed by ID).
    priority: 'low' means master preserves existing data if conflict.
              'high' means new_nodes overwrite master.
    """
    for node in new_nodes:
        nid = node.get("id")
        if not nid:
            continue

        if nid not in master_nodes:
            master_nodes[nid] = node
        else:
            # Merge logic
            existing = master_nodes[nid]

            # If priority is high, overwrite top-level keys
            if priority == "high":
                existing.update(node)
            else:
                # If priority is low, only add missing keys
                for k, v in node.items():
                    if k not in existing:
                        existing[k] = v

            # Merge metadata deeply if possible? For now, shallow merge of dicts
            if "metadata" in node and "metadata" in existing:
                # Always enrich metadata, never lose it
                existing["metadata"].update(node["metadata"])

    return master_nodes


def execute_consolidation():
    print("--- Starting Graph Consolidation ---")

    # 1. Base Tapestry from Woven/Standardized/Verified
    all_nodes = {}
    all_edges = []

    # Load and merge generally (later files overwrite earlier ones in INPUT_GRAPHS list)
    # We want Verified to be the "Truth" for content/structure
    for path in INPUT_GRAPHS:
        print(f"Loading: {os.path.basename(path)}")
        data = load_json(path)

        # Merge Nodes (High priority because list is sorted by reliability)
        merge_nodes(all_nodes, data.get("nodes", []), priority="high")

        # Collect Edges (we will dedupe later)
        all_edges.extend(data.get("edges", []))

    print(f"Base consolidation complete. {len(all_nodes)} nodes loaded.")

    # 2. Integrate PRS-001 (The Rosetta Stone)
    # PRS has a schema: { "cognitive_loom": { "nodes": [...] } }
    # We want PRS to be the authority on metadata, tags, and definitions.
    if os.path.exists(PRS_PATH):
        print(f"Loading PRS-001: {os.path.basename(PRS_PATH)}")
        prs_data = load_json(PRS_PATH)
        prs_nodes = prs_data.get("cognitive_loom", {}).get("nodes", [])

        for p_node in prs_nodes:
            nid = p_node.get("id")
            if not nid:
                continue

            # If node exists in our graph, update it with PRS specific fields
            if nid in all_nodes:
                target = all_nodes[nid]
                # Enforce PRS labels/names
                if "label" in p_node:
                    target["label"] = p_node["label"]
                if "definition" in p_node:
                    target["definition"] = p_node["definition"]
                if "tags" in p_node:
                    target["tags"] = p_node["tags"]
                if "type" in p_node:
                    target["type"] = p_node["type"]  # e.g. [PLANET] vs Artifact

                # Check for location/filepath mismatch
                # We defer to existing filepath if valid, but store PRS location as referenced_location
                if "location" in p_node:
                    target["metadata"] = target.get("metadata", {})
                    target["metadata"]["prs_location"] = p_node["location"]

            else:
                # If it exists in PRS but not in our scanned graphs, ADD IT
                # This ensures we don't lose abstract nodes defined only in the Registry
                all_nodes[nid] = p_node

    # 3. Deduplicate Edges
    unique_edges = set()
    final_edges = []
    for edge in all_edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if not src or not tgt:
            continue

        # Create a unique key
        key = (src, tgt, edge.get("relation", "link"))
        if key not in unique_edges:
            unique_edges.add(key)
            final_edges.append(edge)

    # 4. Construct Definitive Graph
    definitive_graph = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator": "definitive_graph_builder.py",
            "node_count": len(all_nodes),
            "edge_count": len(final_edges),
        },
        "nodes": list(all_nodes.values()),
        "edges": final_edges,
    }

    # 5. Save Definitive Graph
    save_json(DEFINITIVE_GRAPH_PATH, definitive_graph)

    # 6. Update PRS-001 with this new definitive set
    # We need to map our definitive nodes back to the PRS schema
    print("Updating PRS-001...")

    new_prs_nodes = []
    for nid, node in all_nodes.items():
        # Construct PRS node object
        prs_node = {
            "id": nid,
            "label": node.get("label", node.get("id")),  # Fallback to ID
            "type": node.get("type", "Artifact"),
            "definition": node.get("definition", "Imported from Definitive Graph"),
            "tags": node.get("tags", []),
            "location": node.get("metadata", {}).get("filepath", node.get("location", "")),
            "referenced_ids": [],  # We could extract this from edges if needed, but keeping it simple
        }
        new_prs_nodes.append(prs_node)

    # Load original PRS to preserve top-level metadata
    current_prs = load_json(PRS_PATH)
    if "cognitive_loom" not in current_prs:
        current_prs["cognitive_loom"] = {}

    current_prs["cognitive_loom"]["nodes"] = new_prs_nodes
    current_prs["last_updated"] = datetime.now().isoformat()

    save_json(PRS_PATH, current_prs)

    print("SUCCESS: Definitive Graph Created and PRS-001 Updated.")
    print("Automated Synergistic Linking Complete.")


if __name__ == "__main__":
    execute_consolidation()
