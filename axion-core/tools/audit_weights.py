"""
# TOOL-SENT-009: Gravity Weight Auditor (Sentinel Suite)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-009`                                          |
| **2. Official Name**   | `audit_weights.py`                                       |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[SATURN]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Structural Weighting**                                 |
| **11. Catalyst**       | **Gravity Hub Analysis**                                 |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this for graph weight auditing.
GVRN-SYNERGY-001, GOVERNS, This tool audits the structural density of the Matrix.
UMB-AM-001, PROTOCOL, Follows the Alignment Matrix protocol.

---
"""

import json
import os
import sys


def audit_weights(graph_path):
    print(f"Loading Knowledge Graph from: {graph_path}")

    if not os.path.exists(graph_path):
        print(f"ERROR: Graph file not found at {graph_path}")
        return

    with open(graph_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Handle different graph formats (Axion graph vs Standard)
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    print(f"Graph Loaded. Nodes: {len(nodes)} | Edges: {len(edges)}")

    # 1. Calculate Node Degrees
    node_degree = {}
    in_degree = {}
    out_degree = {}

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")

        # Total Degree
        node_degree[src] = node_degree.get(src, 0) + 1
        node_degree[tgt] = node_degree.get(tgt, 0) + 1

        # Directed Degree
        out_degree[src] = out_degree.get(src, 0) + 1
        in_degree[tgt] = in_degree.get(tgt, 0) + 1

    # 2. Identify Hubs ("High Gravity")
    sorted_nodes = sorted(node_degree.items(), key=lambda x: x[1], reverse=True)
    top_hubs = sorted_nodes[:10]

    # 3. Identify Variance (Simulation)
    # We define "Variance" here as the disparity between In-Degree and Out-Degree
    # implying a node is a "Source" (High In) or "Sink" (High Out)

    variance_report = []
    # Use list of all unique nodes found in edges + nodes list
    all_node_ids = set([n.get("id") for n in nodes] + list(node_degree.keys()))

    for node_id in all_node_ids:
        i = in_degree.get(node_id, 0)
        o = out_degree.get(node_id, 0)
        # Variance score = absolute difference
        diff = abs(i - o)
        if diff > 2:  # Threshold
            variance_report.append((node_id, i, o, diff))

    sorted_variance = sorted(variance_report, key=lambda x: x[3], reverse=True)

    # 4. Generate Report
    report_lines = []
    report_lines.append("# WEIGHT AUDIT REPORT (UMB-AM-001)")
    report_lines.append(f"**Date:** 2026-01-21")
    report_lines.append(f"**Graph Source:** `{os.path.basename(graph_path)}`")
    report_lines.append(f"**Metrics:** Nodes `{len(nodes)}` | Edges `{len(edges)}`")
    report_lines.append("---")

    report_lines.append("## I. Gravity Hubs (Top Connected)")
    report_lines.append(
        "Nodes with the highest aggregate link count (In + Out). These are the 'Heavy' nodes in the network."
    )
    report_lines.append("| Node ID | Degree (Weight) |")
    report_lines.append("| :--- | :--- |")
    for nid, degree in top_hubs:
        report_lines.append(f"| `{nid}` | **{degree}** |")

    report_lines.append("\n## II. Variance / Divergence Analysis")
    report_lines.append(
        "Nodes with high disparity between Incoming (References) and Outgoing (Citations). High variance suggests a 'Source of Truth' (High In) or a 'Connector' (High Out)."
    )
    report_lines.append("| Node ID | In | Out | Variance |")
    report_lines.append("| :--- | :--- | :--- | :--- |")
    for nid, i, o, diff in sorted_variance[:15]:
        report_lines.append(f"| `{nid}` | {i} | {o} | **{diff}** |")

    report_lines.append("\n## III. Conclusion")
    report_lines.append(f"Audit Complete. Found {len(sorted_variance)} nodes with significant variance (>2).")
    report_lines.append("RECOMMENDATION: `CMD: REINFORCE` top hubs.")

    report_content = "\n".join(report_lines)

    output_path = "WEIGHT_AUDIT_REPORT.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Audit complete. Report generated at: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "standardized_graph.json"
    audit_weights(path)
