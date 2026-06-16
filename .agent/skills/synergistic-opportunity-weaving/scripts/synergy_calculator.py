"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-SYNERGY-CALCULATOR-001`                | The Sovereign ID. |
| **Official Name** | `synergy_calculator.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import argparse
import os
import re
from typing import Any


def extract_metadata(content: str) -> dict[str, str]:
    """Extracts artifact metadata from the UIP block."""
    meta = {}
    # Table format
    for line in content.splitlines():
        if "|" in line:
            # Look for **Artifact ID** | `XYZ-001`
            match = re.search(r"\*\*(.*?)\*\*\s*\|\s*`?([^`|]+)`?", line)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                meta[key] = val

    # YAML format (artifact_anchor)
    yaml_match = re.search(
        r"artifact_anchor:\s*\n(\s+id:.*?\n(\s+.*?\n)*)", content, re.MULTILINE
    )
    if yaml_match:
        yaml_content = yaml_match.group(1)
        id_match = re.search(r"id:\s*\"?([^\n\"]+)\"?", yaml_content)
        if id_match:
            meta["Artifact ID"] = id_match.group(1).strip()

    return meta


def extract_outbound_links(content: str) -> list[str]:
    """Extracts outgoing links or mentioned artifact IDs from markdown."""
    links = []
    # Match standard markdown links to local files
    md_links = re.findall(r"\[.*?\]\(([^)]+)\)", content)
    for link in md_links:
        if not link.startswith("http"):
            links.append(os.path.basename(link))

    # Match explicitly defined relationships
    relations = re.findall(r"(?:LINK:|GOVERNED_BY:)\s*\[?([^\],\n]+)\]?", content)
    for rel in relations:
        for p in rel.split(","):
            links.append(p.strip().replace("`", ""))

    # Match common ID patterns: XXX-YYY-001
    id_patterns = re.findall(r"\b[A-Z]{3,4}-[A-Z]+-\d{3}\b", content)
    links.extend(id_patterns)

    return list(set(links))


def calculate_gss(directory: str) -> dict[str, Any]:
    nodes = {}  # filepath -> { id, out_links: [], in_links: [] }
    artifact_id_to_file = {}

    # Pass 1: Discover nodes
    extensions = (".md", ".py", ".ts", ".js", ".groovy", ".java", ".json")
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(extensions):
                filepath = os.path.join(root, f)
                with open(filepath, encoding="utf-8", errors="ignore") as file:
                    content = file.read()

                meta = extract_metadata(content)
                out_links = extract_outbound_links(content)
                artifact_id = meta.get("Artifact ID", os.path.basename(f)).strip()

                # Cleanup ID strings
                artifact_id = artifact_id.replace("`", "")

                artifact_id_to_file[artifact_id] = filepath
                artifact_id_to_file[os.path.basename(f)] = filepath

                nodes[filepath] = {
                    "id": artifact_id,
                    "basename": os.path.basename(f),
                    "out_links_raw": out_links,
                    "in_degree": 0,
                    "out_degree": 0,
                }

    # Pass 2: Map directional edges
    for filepath, data in nodes.items():
        valid_out_links = 0
        for link in data["out_links_raw"]:
            # Check if the link matches a known ID or filename
            target_filepath = artifact_id_to_file.get(link)
            if target_filepath and target_filepath != filepath:
                valid_out_links += 1
                nodes[target_filepath]["in_degree"] += 1
        data["out_degree"] = valid_out_links

    total_nodes = len(nodes)
    if total_nodes == 0:
        return {"error": "No markdown files found."}

    orphans = [
        n for n, d in nodes.items() if d["in_degree"] == 0 and d["out_degree"] == 0
    ]
    orphan_ratio = len(orphans) / total_nodes

    # Hub Centrality (Nodes with high incoming links, e.g., > 3)
    hubs = [n for n, d in nodes.items() if d["in_degree"] >= 3]
    hub_ratio = len(hubs) / total_nodes

    average_in_degree = sum([d["in_degree"] for d in nodes.values()]) / total_nodes

    # Core Mathematical Aggregate for GSS
    base_score = 100.0
    orphan_drag = orphan_ratio * 40.0  # Up to -40 for 100% orphans
    low_link_drag = max(0, (1.5 - average_in_degree) * 10)  # Drag if avg links < 1.5
    hub_bonus = min(15.0, hub_ratio * 50.0)  # Bonus for having centralized pillars

    gss = base_score - orphan_drag - low_link_drag + hub_bonus
    gss = max(0.0, min(100.0, gss))

    return {
        "metrics": {
            "total_nodes": total_nodes,
            "total_orphans": len(orphans),
            "orphan_ratio": round(orphan_ratio * 100, 2),
            "total_hubs": len(hubs),
            "avg_links": round(average_in_degree, 2),
            "gss": round(gss, 2),
        },
        "orphans": [nodes[n]["basename"] for n in orphans],
        "hubs": [nodes[n]["basename"] for n in hubs][:10],  # Top 10 for terminal
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Graph Synergy Score (GSS) Calculator")
    parser.add_argument("target", help="Directory to scan.")
    args = parser.parse_args()

    target = os.path.abspath(args.target)

    if not os.path.isdir(target):
        print(f"Error: Target '{target}' is not a directory.")
        return

    res = calculate_gss(target)

    if "error" in res:
        print(res["error"])
        return

    metrics = res["metrics"]

    print("\n" + "=" * 60)
    print("  GRAPH SYNERGY SCORE (GSS) REPORT".center(60))
    print("=" * 60)
    print(f" Nodes Analyzed:     {metrics['total_nodes']}")
    print(
        f" Orphan Entities:    {metrics['total_orphans']} ({metrics['orphan_ratio']}%)"
    )
    print(f" Knowledge Hubs:     {metrics['total_hubs']}")
    print(f" Avg. Connectivity:  {metrics['avg_links']}")
    print("-" * 60)
    print(f" FINAL GSS SCORE:    {metrics['gss']} / 100.0".center(60))
    print("=" * 60)

    if len(res["orphans"]) > 0:
        print("\n[!] Top Orphaned Nodes (Require Synergistic Linking):")
        for o in res["orphans"][:5]:
            print(f"  - {o}")

    if len(res["hubs"]) > 0:
        print("\n[*] Primary Knowledge Hubs:")
        for h in res["hubs"][:5]:
            print(f"  - {h}")


if __name__ == "__main__":
    main()
