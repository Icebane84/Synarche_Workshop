"""PROJECT: AXION / OGLN
MODULE: SOPHIA RESONANT REFACTOR ENGINE (UMB-TECH-SOPHIA-004)
AUTHOR: PHOENIX PROTOCOL (SOPHIA ENTITY)
STATUS: PROMOTED (RESONANT)
DESCRIPTION:
    Transforms entropic graph data into standardized semantic anchors.
    Implements 3D Vector Analysis (Entropy, Stagnation, Density) for graph health.
"""

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ResonanceReport:
    """Calculates systemic health metrics for the refactored graph."""

    node_count: int
    edge_count: int
    entropy: float  # Structural complexity
    stagnation: float  # Redundancy in types/domains
    density: float  # Semantic metadata coverage
    status: str = "STABLE"
    advice: list[str] = field(default_factory=list)

    def display(self) -> None:
        print("\n--- SOPHIA RESONANCE REPORT ---")
        print(f"Nodes: {self.node_count} | Edges: {self.edge_count}")
        print(
            f"Entropy: {self.entropy:.2f} | Stagnation: {self.stagnation:.2f} | Density: {self.density:.2f}"
        )
        print(f"STATUS: {self.status}")
        for a in self.advice:
            print(f"ADVICE: {a}")
        print("--------------------------------\n")


class SemanticWeaver:
    """Extracts high-resonance metadata from unstructured content."""

    STANDARD_MAP: dict[str, str] = {
        "artifact id": "artifact_id",
        "domain": "domain",
        "version": "version",
        "status": "status",
        "state": "status",
        "tier": "tier",
        "governance": "governance_id",
        "title": "title",
        "celestial class": "celestial_class",
        "provenance": "provenance",
    }

    @staticmethod
    def weave(content: str) -> dict[str, str]:
        """Performs deep parse of markdown tables to extract semantic anchors."""
        metadata = {}
        lines = content.split("\n")

        for line in lines:
            line = line.strip()
            if line.count("|") < 2 or re.match(r"\|[:\s-]+\|", line):
                continue

            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                # Normalize key/val by stripping artifacts of markdown
                key = re.sub(r"[*:`#\[\]]", "", parts[0]).strip()
                val = re.sub(r"[*:`#\[\]]", "", parts[1]).strip()

                if not key or key.lower() in [
                    "attribute",
                    "value",
                    "field",
                    "mask",
                    "agent mask",
                ]:
                    continue

                # Standardize primary anchors
                key_lower = key.lower()
                if key_lower in SemanticWeaver.STANDARD_MAP:
                    std_key = SemanticWeaver.STANDARD_MAP[key_lower]
                    if std_key not in metadata:
                        metadata[std_key] = val

                # Preserve all semantic data in meta_ namespaces
                safe_key = re.sub(r"[^a-zA-Z0-9]", "_", key)
                metadata[f"meta_{safe_key}"] = val

        return metadata


class SophiaRefactorEngine:
    """The core engine responsible for promoting scratch logic to systemic code."""

    def __init__(self, json_path: Path, output_dir: Path) -> None:
        self.json_path = json_path
        self.output_dir = output_dir
        self.nodes_data: list[dict[str, Any]] = []
        self.edges_data: list[dict[str, Any]] = []

    def _load_graph(self) -> None:
        """Loads the standardized graph into memory."""
        print(f"SOPHIA: Loading {self.json_path}...")
        with open(self.json_path, encoding="utf-8") as f:
            data = json.load(f)
            self.nodes_raw = data.get("nodes", [])
            self.edges_raw = data.get("edges", [])

    def _calculate_resonance(self) -> ResonanceReport:
        """Analyzes the resulting dataset for systemic health."""
        if not self.nodes_data:
            return ResonanceReport(0, 0, 1.0, 1.0, 0.0)

        # 1. Entropy: Average edge-to-node ratio (Target: 10-20 for a healthy mesh)
        entropy = len(self.edges_data) / len(self.nodes_data)

        # 2. Stagnation: Ratio of unique domains to total nodes
        domains = {n.get("domain", "Unknown") for n in self.nodes_data}
        stagnation = 1.0 - (len(domains) / len(self.nodes_data))

        # 3. Density: Average metadata fields per node (Target: >10 fields)
        total_meta_fields = sum(
            len([k for k in n if k.startswith("meta_")]) for n in self.nodes_data
        )
        density = total_meta_fields / len(self.nodes_data)

        report = ResonanceReport(
            node_count=len(self.nodes_data),
            edge_count=len(self.edges_data),
            entropy=entropy,
            stagnation=stagnation,
            density=density,
        )

        if stagnation > 0.8:
            report.advice.append(
                "Domain saturation detected. Consider splitting domains."
            )
        if density < 5.0:
            report.advice.append(
                "Low semantic density. Manual provenance audit recommended."
            )

        return report

    def promote(self) -> None:
        """Promotes entropic JSON into resonant CSV anchors."""
        self._load_graph()

        # Process Nodes
        print(f"SOPHIA: Parsing {len(self.nodes_raw)} nodes...")
        for node in self.nodes_raw:
            processed = {
                "node_id": node.get("id"),
                "node_type": node.get("type"),
                "filename": node.get("metadata", {}).get("filename", ""),
                "filepath": node.get("metadata", {}).get("filepath", ""),
                "size_bytes": node.get("metadata", {}).get("size", 0),
            }
            # Deep Parse content
            processed.update(SemanticWeaver.weave(node.get("content", "")))
            self.nodes_data.append(processed)

        # Process Edges
        print(f"SOPHIA: Weaving {len(self.edges_raw)} edges...")
        for edge in self.edges_raw:
            self.edges_data.append(
                {
                    "source": edge.get("source"),
                    "target": edge.get("target"),
                    "relation": edge.get("relation"),
                    "score": edge.get("metadata", {}).get("score", 0),
                    "algorithm": edge.get("metadata", {}).get("algorithm", ""),
                }
            )

        # Export
        self._export_to_csv()

        # Display Wisdom
        report = self._calculate_resonance()
        report.display()

    def _export_to_csv(self) -> None:
        """Flattens dictionaries to CSV with Sophia-aligned priority."""
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)

        # Nodes
        all_keys: set[str] = set()
        for n in self.nodes_data:
            all_keys.update(n.keys())

        priority = [
            "node_id",
            "artifact_id",
            "title",
            "node_type",
            "domain",
            "version",
            "status",
            "tier",
            "governance_id",
            "celestial_class",
            "filename",
            "size_bytes",
        ]

        header = [k for k in priority if k in all_keys]
        meta_keys = sorted([k for k in all_keys if k.startswith("meta_")])
        header.extend(meta_headers := meta_keys)
        header.extend(sorted(all_keys - set(header)))

        nodes_path = self.output_dir / "resonant_nodes.csv"
        with open(nodes_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(self.nodes_data)

        # Edges
        edges_path = self.output_dir / "resonant_edges.csv"
        with open(edges_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["source", "target", "relation", "score", "algorithm"]
            )
            writer.writeheader()
            writer.writerows(self.edges_data)


if __name__ == "__main__":
    # Standard Synarche paths relative to workspace root
    ROOT = Path(__file__).parent.parent.parent
    ENGINE = SophiaRefactorEngine(
        json_path=ROOT / "standardized_graph.json",
        output_dir=ROOT / "artifacts",
    )
    ENGINE.promote()
