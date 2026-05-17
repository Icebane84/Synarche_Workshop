#!/usr/bin/env python3
"""
# TOOL-SYN-001: Synarche Driver
# Purpose: Orchestrates the Loom, Weaver, and Resonance Scanner to generate a Synergy Report.
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    from axion_core.loom import CognitiveLoom
    from hephaestus.lib.catalyst_weaver import CatalystWeaver
    from hephaestus.lib.resonance_scanner import scan_directory
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("--- Synarche Driver Active ---")
    print(f"Target Root: {root}")

    # 1. Resonance Scan
    print("\n[1] Running Resonance Scan...")
    total_files, aligned_files, unaligned_paths = scan_directory(Path(root))
    resonance_score = (aligned_files / total_files * 100) if total_files > 0 else 0.0
    print(f"    Resonance Score: {resonance_score:.2f}% ({aligned_files}/{total_files})")

    # 2. Loom Ingestion
    print("\n[2] Spinning the Cognitive Loom...")
    loom = CognitiveLoom(root)

    # Manually walk and ingest since Loom doesn't have a recursive walk init
    count = 0
    for subdir, dirs, files in os.walk(root):
        # Skip hidden/env dirs
        if any(x in subdir for x in [".git", "__pycache__", "node_modules", "venv"]):
            continue

        for file in files:
            if file.endswith(".md") or file.endswith(".py") or file.endswith(".js"):
                loom.ingest_artifact(os.path.join(subdir, file))
                count += 1

    print(f"    Ingested {count} artifacts into the Tapestry.")
    loom.export_tapestry("tapestry.json")

    # 3. Catalyst Weaver (Simulated)
    # The Loom already calls _weave_edges for explicit links.
    # CatalystWeaver is for *implicit* semantic links.
    print("\n[3] Executing Catalyst Weaver (Semantic Scan)...")
    weaver = CatalystWeaver()
    nodes = list(loom.tapestry["nodes"].values())
    semantic_links = 0

    # Naive O(N^2) scan for demo - limit to first 50 nodes to be safe
    limit_nodes = nodes[:50]
    for i in range(len(limit_nodes)):
        for j in range(i + 1, len(limit_nodes)):
            node_a = limit_nodes[i]
            node_b = limit_nodes[j]

            # Adapt node structure for Weaver (expects dict with 'content', 'tags', 'official_name')
            # Loom nodes have 'content_preview' and 'metadata'.
            a_adapter = {
                "id": node_a["id"],
                "content": node_a.get("content_preview", ""),
                "tags": [],  # Loom doesn't extract tags yet?
                "official_name": os.path.basename(node_a["path"]),
            }
            b_adapter = {
                "id": node_b["id"],
                "content": node_b.get("content_preview", ""),
                "tags": [],
                "official_name": os.path.basename(node_b["path"]),
            }

            link = weaver.weave(a_adapter, b_adapter)
            if link:
                # Add to tapestry edges
                loom.tapestry["edges"].append(
                    {
                        "source": link["source"],
                        "target": link["target"],
                        "type": "synergy",
                        "weight": link["synergy_score"],
                        "rationale": link["rationale"],
                    }
                )
                semantic_links += 1

    print(f"    Weaved {semantic_links} new semantic connections.")

    # OUTPUT REPORT DATA
    report_data = {
        "resonance": {"score": resonance_score, "total": total_files, "aligned": aligned_files},
        "loom": {
            "nodes": len(loom.tapestry["nodes"]),
            "edges": len(loom.tapestry["edges"]),
            "semantic_weaves": semantic_links,
        },
    }

    with open("synergy_stats.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print("\n[SUCCESS] Synergy analysis complete. Data saved to synergy_stats.json")


if __name__ == "__main__":
    main()
