"""
# TOOL-HPRI-006: The Catalyst Weaver (Synergy Engine)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-006`                                          |
| **2. Official Name**   | `catalyst_weaver.py`                                     |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[STAR]`                                                 |
| **8. Tier**            | **Strategic**                                            |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Synergy**                                              |
| **11. Catalyst**       | **Graph Weaving**                                        |
| **12. Relations**      | `LINK: [UMB-CATALYST-001](../../docs/specs/UMB-CATALYST-001_TheCatalystWeaver_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
UMB-CATALYST-001, DEFINES, This tool implements the Catalyst Weaver spec.
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for weaving.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Synergy Engine (The High Priestess)
# Synergy Set: The Harmonic Weaver
# Primary Stat Buff: Insight (+20), Synergy (+20)
# Passive Ability: The Loom (Auto-Linking)
# Cognitive Load Cost: High
# XP Award Value: 150 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: WEAVE_GRAPH` | Scans for semantic overlaps. | Generates new Synergy Edges. |
| `CMD: WEB_SCAN` | Indexes workspace artifacts. | Updates Knowledge Graph. |
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

# Constants
GRAPH_PATH = "standardized_graph.json"
SYNERGY_THRESHOLD = 0.5
CONCEPT_MIN_LENGTH = 3
MAX_SEMANTIC_SCORE = 0.4
METADATA_SCORE = 0.2
REF_SCORE = 0.2
REF_BOOST = 0.1
STRUCT_SCORE = 0.1
CONCEPT_MATCH_THRESHOLD = 3


class CatalystWeaver:
    def __init__(
        self,
        graph_path: str = GRAPH_PATH,
        nodes: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
    ) -> None:
        self.graph_path = graph_path
        self.nodes = nodes if nodes is not None else []
        self.edges = edges if edges is not None else []

        if not self.nodes and self.graph_path:
            self.load_graph()

    def load_graph(self) -> None:
        if not os.path.exists(self.graph_path):
            return

        try:
            with open(self.graph_path, encoding="utf-8") as f:
                data = json.load(f)
                self.nodes = data.get("nodes", [])
                self.edges = data.get("edges", [])
        except Exception:
            pass

    def get_node_by_id_or_path(self, target: str) -> dict[str, Any] | None:
        # Case 1: Target is an ID
        node = next((n for n in self.nodes if n.get("id") == target), None)
        if node:
            return node

        # Case 2: Target is a path
        # Normalize slashes
        target = target.replace("\\", "/")
        node = next(
            (n for n in self.nodes if n.get("metadata", {}).get("filepath", "").replace("\\", "/") == target), None
        )
        if node:
            return node

        # Case 3: Transient load from disk if path exists
        if os.path.exists(target):
            try:
                content = Path(target).read_text(encoding="utf-8", errors="ignore")
                # Quick extract ID
                match = re.search(r"^#\s*([A-Z]{3,}(?:-[A-Z0-9]+)+)", content, re.MULTILINE)
                artifact_id = match.group(1) if match else Path(target).name

                # Mock node
                return {
                    "id": artifact_id,
                    "type": "Artifact",
                    "content": content,
                    "metadata": {"filepath": str(Path(target).absolute())},
                }
            except Exception:
                pass

        return None

    def calculate_synergy(self, src: dict[str, Any], tgt: dict[str, Any]) -> float:
        src_content = src.get("content", "")
        tgt_content = tgt.get("content", "")

        h_sem = self._calculate_semantic_overlap(src_content, tgt_content)
        h_meta = self._calculate_metadata_alignment(src_content, tgt_content)
        h_ref = self._calculate_explicit_reference(src, tgt)
        h_struct = self._calculate_structural_alignment(src, tgt)

        total_score = min(1.0, h_sem + h_meta + h_ref + h_struct)
        return total_score

    def _calculate_semantic_overlap(self, src_content: str, tgt_content: str) -> float:
        # Extract Capitalized Words > CONCEPT_MIN_LENGTH chars (Heuristic for "Concepts")
        pattern = r"\b[A-Z][a-zA-Z0-9]{" + str(CONCEPT_MIN_LENGTH) + r",}\b"
        src_caps = set(re.findall(pattern, src_content))
        tgt_caps = set(re.findall(pattern, tgt_content))

        if src_caps and tgt_caps:
            intersection = src_caps.intersection(tgt_caps)
            # Let's say if we share > CONCEPT_MATCH_THRESHOLD concepts, it's significant
            if len(intersection) > CONCEPT_MATCH_THRESHOLD:
                return min(MAX_SEMANTIC_SCORE, 0.1 * len(intersection))
        return 0.0

    def _calculate_metadata_alignment(self, src_content: str, tgt_content: str) -> float:
        src_tags = self._extract_tags(src_content)
        tgt_tags = self._extract_tags(tgt_content)

        if src_tags and tgt_tags:
            intersection = set(src_tags).intersection(set(tgt_tags))
            if intersection:
                return METADATA_SCORE  # Flat bonus
        return 0.0

    def _calculate_explicit_reference(self, src: dict[str, Any], tgt: dict[str, Any]) -> float:
        h_ref = 0.0
        tgt_id = tgt.get("id", "")
        src_content = src.get("content", "")

        if tgt_id and tgt_id in src_content:
            h_ref = REF_SCORE
            # Boost if verified link syntax [ID](...)
            if f"[{tgt_id}]" in src_content:
                h_ref += REF_BOOST
        return h_ref

    def _calculate_structural_alignment(self, src: dict[str, Any], tgt: dict[str, Any]) -> float:
        src_path = src.get("metadata", {}).get("filepath", "")
        tgt_path = tgt.get("metadata", {}).get("filepath", "")
        if src_path and tgt_path and os.path.dirname(src_path) == os.path.dirname(tgt_path):
            # Same directory
            return STRUCT_SCORE
        return 0.0

    def _extract_tags(self, content: str) -> list[str]:
        tags = []
        # Pattern 1: **Tags:** tag1, tag2
        match1 = re.search(r"\*\*Tags:\*\*\s*(.*)", content)
        if match1:
            raw = match1.group(1)
            clean = raw.replace("`", "").replace("[", "").replace("]", "").replace("|", "")
            tags.extend([t.strip().lower() for t in clean.split(",") if t.strip()])

        # Pattern 2: Pipe Table | **Tags** | `tag1, tag2` |
        match2 = re.search(r"\|\s*\*\*Tags\*\*\s*\|\s*(.*)\|", content)
        if match2:
            raw = match2.group(1)
            # Remove inner pipes if any (bad formatting)
            raw = raw.split("|")[0]
            clean = raw.replace("`", "").replace("[", "").replace("]", "")
            tags.extend([t.strip().lower() for t in clean.split(",") if t.strip()])

        return tags

    def weave_all(self) -> list[dict[str, Any]]:
        """
        Scans entire graph for missing synergistic links.
        Returns a list of new edge dictionaries.
        """
        new_edges = []

        # O(N^2) complexity - be careful with large graphs.
        # For 800 nodes, 640k comparisons. Check performance.
        # Filter for artifacts only
        artifacts = [n for n in self.nodes if n.get("type") == "Artifact"]

        for i, src in enumerate(artifacts):
            for j, tgt in enumerate(artifacts):
                if i >= j:
                    continue  # Avoid duplicates and self-loops

                score = self.calculate_synergy(src, tgt)
                if score >= SYNERGY_THRESHOLD:
                    new_edges.append(
                        {
                            "source": src.get("id"),
                            "target": tgt.get("id"),
                            "relation": "SYNERGY",
                            "metadata": {"score": score, "algorithm": "catalyst_weaver_v1"},
                        }
                    )

        return new_edges

    def weave(self, target_identifier: str) -> None:
        target_node = self.get_node_by_id_or_path(target_identifier)
        if not target_node:
            return

        synergy_links = []

        for node in self.nodes:
            if node.get("id") == target_node.get("id"):
                continue

            # Skip chunks for high-level weave, compare artifacts only
            if node.get("type") != "Artifact":
                continue

            score = self.calculate_synergy(target_node, node)
            if score >= SYNERGY_THRESHOLD:
                synergy_links.append({"target": node.get("id"), "score": score, "reason": f"S={score:.2f}"})

        # Sort by score
        # Sort by score
        synergy_links.sort(key=lambda x: x["score"], reverse=True)
        return synergy_links

    def save_graph(self) -> None:
        """Saves the current nodes and edges to the graph file."""
        try:
            with open(self.graph_path, "w", encoding="utf-8") as f:
                json.dump({"nodes": self.nodes, "edges": self.edges}, f, indent=2)
            print(f"[INFO] Graph saved to {self.graph_path} ({len(self.nodes)} nodes, {len(self.edges)} edges)")
        except Exception as e:
            print(f"[ERROR] Failed to save graph: {e}")

    def scan(self, target_dir: str) -> None:
        """
        Recursively scans a directory for artifacts and adds them to the graph.
        """
        print(f"[INFO] Scanning {target_dir} for artifacts...")
        target_path = Path(target_dir)
        if not target_path.exists():
            print(f"[ERROR] Path {target_dir} does not exist.")
            return

        new_count = 0
        updated_count = 0

        # Walk through the directory
        for root, _, files in os.walk(target_path):
            for file in files:
                if not file.endswith((".py", ".md", ".ts", ".js", ".yml", ".yaml")):
                    continue

                full_path = Path(root) / file
                try:
                    content = full_path.read_text(encoding="utf-8", errors="ignore")

                    # Check for UIP Header or Artifact ID regex
                    match = re.search(r"Artifact ID.*[:|`]\s*([A-Z]{3,}-[A-Z]{3,}-[0-9]{3,})", content, re.IGNORECASE)
                    if not match:
                        # Fallback: Check for standard header start
                        if not ("# TOOL-" in content or "Artifact ID" in content):
                            continue
                        # If simple header exists but regex missed, use filename as ID fallback or skip
                        artifact_id = file
                    else:
                        artifact_id = match.group(1).strip("` ")

                    # Create/Update Node
                    node_data = {
                        "id": artifact_id,
                        "type": "Artifact",
                        "content": content[:500],  # Store snippet only to save space
                        "metadata": {"filepath": str(full_path.absolute()), "filename": file, "size": len(content)},
                    }

                    # Check if exists
                    existing = next((n for n in self.nodes if n["id"] == artifact_id), None)
                    if existing:
                        existing.update(node_data)
                        updated_count += 1
                    else:
                        self.nodes.append(node_data)
                        new_count += 1

                except Exception as e:
                    # print(f"[WARN] Could not read {file}: {e}")
                    pass

        print(f"[INFO] Scan complete. New: {new_count}, Updated: {updated_count}")
        self.save_graph()


def main() -> None:
    parser = argparse.ArgumentParser(description="The Catalyst Weaver")
    parser = argparse.ArgumentParser(description="The Catalyst Weaver")
    parser.add_argument("command", choices=["weave", "scan", "weave_all"], help="Command to execute")
    parser.add_argument("--target", help="Target file or directory")

    args = parser.parse_args()

    weaver = CatalystWeaver(GRAPH_PATH)

    if args.command == "weave":
        links = weaver.weave(args.target)
        print(f"[INFO] Synergy Report for {args.target}:")
        for link in links:
            print(f"  - LINK: {link['target']} (Score: {link['score']:.2f})")
    elif args.command == "scan":
        weaver.scan(args.target)
    elif args.command == "weave_all":
        print("[INFO] Weaving all nodes...")
        new_edges = weaver.weave_all()
        weaver.edges.extend(new_edges)
        weaver.save_graph()
        print(f"[INFO] Weave complete. Added {len(new_edges)} new edges.")


if __name__ == "__main__":
    main()
