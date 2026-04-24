"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-SOT-SCANNER-001`                | The Sovereign ID. |
| **Official Name** | `sot_scanner.py`                   | The Filename.     |
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


def extract_metadata(content: str) -> dict[str, str]:
    meta = {}
    # Table format
    for line in content.splitlines():
        if "|" in line:
            match = re.search(r"\*\*(.*?)\*\*\s*\|\s*`?([^`|]+)`?", line)
            if match:
                meta[match.group(1).strip()] = match.group(2).strip()
    
    # YAML format (artifact_anchor)
    yaml_match = re.search(r"artifact_anchor:\s*\n(\s+id:.*?\n(\s+.*?\n)*)", content, re.MULTILINE)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        id_match = re.search(r"id:\s*\"?([^\n\"]+)\"?", yaml_content)
        if id_match:
            meta["Artifact ID"] = id_match.group(1).strip()
            
    return meta


def extract_links(content: str) -> list[str]:
    links = []
    # Standard MD files
    md_links = re.findall(r"\[.*?\]\(([^)]+)\)", content)
    links.extend([os.path.basename(l) for l in md_links if not l.startswith("http")])
    # Relationships
    relations = re.findall(r"(?:LINK:|GOVERNED_BY:)\s*\[?([^\],\n]+)\]?", content)
    for r in relations:
        links.extend([p.strip().replace("`", "") for p in r.split(",")])
    # IDs
    id_patterns = re.findall(r"\b[A-Z]{3,4}-[A-Z]+-\d{3}\b", content)
    links.extend(id_patterns)
    return list(set(links))


def extract_keywords(content: str) -> set[str]:
    """Basic keyword extraction for semantic matching."""
    text = re.sub(r"[^A-Za-z0-9\s]", "", content).lower()
    words = text.split()
    # Filter common stop words and focus on likely technical terms (length > 5)
    keywords = {
        w
        for w in words
        if len(w) > 5 and w not in ["should", "system", "project", "python", "script"]
    }
    return keywords


def scan_opportunities(directory: str) -> None:
    nodes = {}
    id_to_file = {}

    # Pass 1: Parse All
    print(">>> Scanning The Loom...")
    extensions = (".md", ".py", ".ts", ".js", ".groovy", ".java", ".json")
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(extensions):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8", errors="ignore") as file:
                    content = file.read()

                meta = extract_metadata(content)
                artifact_id = meta.get("Artifact ID", f).replace("`", "").strip()

                id_to_file[artifact_id] = path
                id_to_file[f] = path

                nodes[path] = {
                    "id": artifact_id,
                    "basename": f,
                    "out_links": extract_links(content),
                    "keywords": extract_keywords(content),
                    "reciprocal_misses": [],
                    "latent_synergies": [],
                }

    # Pass 2: Map non-reciprocal links (One-way bridges)
    # If A links to B, but B does not link to A, it's flagged.
    for path, data in nodes.items():
        for link in data["out_links"]:
            target_path = id_to_file.get(link)
            if target_path and target_path != path:
                target_node = nodes[target_path]
                # See if target points back to us
                if (
                    data["id"] not in target_node["out_links"]
                    and data["basename"] not in target_node["out_links"]
                ):
                    target_node["reciprocal_misses"].append(data["basename"])

    # Pass 3: Latent Synergy Analysis
    # Compare keyword overlap between unconnected nodes
    filepaths = list(nodes.keys())
    for i in range(len(filepaths)):
        for j in range(i + 1, len(filepaths)):
            n1 = nodes[filepaths[i]]
            n2 = nodes[filepaths[j]]

            # Skip if already linked
            if n2["id"] in n1["out_links"] or n1["id"] in n2["out_links"]:
                continue

            intersection = n1["keywords"].intersection(n2["keywords"])
            # Threshold for latent synergy: 25+ shared significant keywords
            if len(intersection) >= 25:
                n1["latent_synergies"].append(n2["basename"])
                n2["latent_synergies"].append(n1["basename"])

    # Report Generation
    print("\n" + "=" * 70)
    print("  SYNERGISTIC OPPORTUNITY TRACKER (SOT) REPORT".center(70))
    print("=" * 70)

    opportunities_found = 0

    # 1. Non-Reciprocal Ties
    print("\n>>> CRITICAL OPPORTUNITY: Unidirectional Bridges (Missing Return Links)\n")
    for path, data in nodes.items():
        if len(data["reciprocal_misses"]) > 0:
            opportunities_found += 1
            print(f"[!] {data['basename']}")
            for miss in data["reciprocal_misses"][:3]:  # Cap output
                print(f"    <- Linked from {miss}, but does not link back.")
            if len(data["reciprocal_misses"]) > 3:
                print(f"    <- ...and {len(data['reciprocal_misses']) - 3} others.")

    # 2. Latent Synergies
    print("\n>>> COGNITIVE OPPORTUNITY: Latent Semantic Synergies (Unlinked Twins)\n")
    for path, data in nodes.items():
        if len(data["latent_synergies"]) > 0:
            opportunities_found += 1
            print(f"[*] {data['basename']}")
            print(
                f"    Should potentially link to: {', '.join(data['latent_synergies'][:2])}"
            )

    if opportunities_found == 0:
        print("\n>>> Zero Opportunities Detected. The Graph is Perfectly Synergistic.")
    else:
        print(f"\n>>> Total Opportunities Flagged: {opportunities_found}")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="UMB-SOT-001 Opportunity Scanner")
    parser.add_argument("target", help="Directory to scan.")
    args = parser.parse_args()

    target = os.path.abspath(args.target)
    if os.path.isdir(target):
        scan_opportunities(target)
    else:
        print(f"Error: {target} is not a directory.")


if __name__ == "__main__":
    main()
