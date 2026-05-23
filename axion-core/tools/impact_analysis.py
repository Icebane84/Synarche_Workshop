"""# TOOL-SENT-007: The Architect's Gaze (Audit Engine).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-007`                                          |
| **2. Official Name**   | `impact_analysis.py`                                     |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Impact Simulation**                                    |
| **11. Catalyst**       | **Blast Radius Scan**                                    |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for impact analysis.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-STAR-004, FEEDS, The RAG Graph Generator feeds data into this tool.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+15), Foresight (+10)
# Passive Ability: Ripple Sight (Impact Simulation)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: ANALYZE_IMPACT` | BFS Blast Radius Scan | Change Management |
| `⚡ EXECUTE: GAPE_RADIUS` | Direct Dependency Check | Risk Assessment |

---

Systemic Impact Analyzer
Protocol: AOP-ARCH-GAZE-001
Function: Simulates the "ripple effects" of a proposed code change across the Cognitive Loom.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

# --- Configuration ---
# Default paths adjusted for axion-core context
GRAPH_PATH = "tools/phoenix_knowledge_graph.json"
CODE_ROOTS = ["src"]


# --- Color Codes ---
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# --- Types ---
class Node(TypedDict):
    id: str
    type: str
    content: Optional[str]


class Edge(TypedDict):
    source: str
    target: str
    relation: str


class ImpactReport(TypedDict):
    target: str
    impacted_nodes: List[Dict]  # {id, distance, path}
    stats: Dict


# --- Core Logic ---


class ImpactAnalyzer:
    def __init__(self):
        self.graph_nodes: Dict[str, Node] = {}
        self.graph_edges: List[Edge] = []
        self.adjacency: Dict[str, List[Dict]] = {}  # id -> [{target, relation}, ...]

    def load_loom(self, json_path: Path) -> None:
        """Loads the Cognitive Loom (Knowledge Graph)."""
        if not json_path.exists():
            print(
                f"{Colors.FAIL}❌ Critical Error: Knowledge Graph not found at {json_path}{Colors.ENDC}"
            )
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for n in data.get("nodes", []):
                self.add_node(n["id"], n["type"], n.get("content"))

            for e in data.get("edges", []):
                self.add_edge(e["source"], e["target"], e["relation"])

            print(
                f"{Colors.OKGREEN}✔ Loaded Cognitive Loom: {len(self.graph_nodes)} nodes, {len(self.graph_edges)} edges.{Colors.ENDC}"
            )
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error loading graph: {e}{Colors.ENDC}")
            sys.exit(1)

    def _parse_dependencies(
        self, file_path: Path, source_id: str, import_regex: re.Pattern
    ) -> int:
        edge_count = 0
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            matches = import_regex.findall(content)
            for match in matches:
                import_path = match[0] or match[1]

                if import_path.startswith("."):
                    target_name = Path(import_path).name
                    for ext in ["", ".ts", ".tsx", ".js", ".py"]:
                        if f"{target_name}{ext}" in self.graph_nodes:
                            self.add_edge(source_id, f"{target_name}{ext}", "IMPORTS")
                            edge_count += 1
                            break

            artifact_matches = re.findall(
                r"(UMB-[A-Z]+-\d+|AOP-[A-Z]+-\d+|TOOL-[A-Z]+-\d+)", content
            )
            for art_id in set(artifact_matches):
                if art_id in self.graph_nodes:
                    self.add_edge(source_id, art_id, "IMPLEMENTS")
                    edge_count += 1

        except Exception as e:
            print(f"{Colors.WARNING}⚠ Error parsing {file_path.name}: {e}{Colors.ENDC}")

        return edge_count

    def scan_codebase(self, root_paths: List[str]) -> None:
        """Scans code directories to build the Code Dependency Layer."""
        print(f"{Colors.OKBLUE}🔍 Scanning Codebase for Dependencies...{Colors.ENDC}")

        file_count = 0
        edge_count = 0

        # Regex for generic imports
        import_regex = re.compile(
            r'(?:import|export)\s+[\w\s{},*]+\s+from\s+[\'"]([^\'"]+)[\'"]|require\([\'"]([^\'"]+)[\'"]\)'
        )

        for root_str in root_paths:
            root = Path(root_str)
            if not root.exists():
                print(f"{Colors.WARNING}⚠ Code root not found: {root}{Colors.ENDC}")
                continue

            for file_path in root.rglob("*.*"):
                if file_path.suffix not in [".ts", ".tsx", ".js", ".jsx", ".py"]:
                    continue

                source_id = file_path.name
                self.add_node(source_id, "CodeFile", str(file_path))
                file_count += 1

                edge_count += self._parse_dependencies(
                    file_path, source_id, import_regex
                )

        print(
            f"   Scanned {file_count} files, Added {edge_count} code dependency edges."
        )

    def add_node(
        self, node_id: str, node_type: str, content: Optional[str] = ""
    ) -> None:
        if node_id not in self.graph_nodes:
            self.graph_nodes[node_id] = {
                "id": node_id,
                "type": node_type,
                "content": content,
            }

    def add_edge(self, source: str, target: str, relation: str) -> None:
        self.graph_edges.append(
            {"source": source, "target": target, "relation": relation}
        )

        if source not in self.adjacency:
            self.adjacency[source] = []
        if target not in self.adjacency:
            self.adjacency[target] = []

        self.adjacency[source].append(
            {"target": target, "relation": relation, "direction": "outgoing"}
        )
        self.adjacency[target].append(
            {"target": source, "relation": relation, "direction": "incoming"}
        )

    def simulate_impact(
        self, target_id: str, max_depth: int = 2
    ) -> Optional[ImpactReport]:
        """Performs BFS to find blast radius."""
        if target_id not in self.graph_nodes:
            matches = [k for k in self.graph_nodes.keys() if target_id in k]
            if len(matches) == 1:
                target_id = matches[0]
                print(
                    f"{Colors.OKCYAN}Target '{target_id}' found (fuzzy match).{Colors.ENDC}"
                )
            else:
                return None

        impacted = {}
        queue = [(target_id, 0, [])]
        visited = set()

        while queue:
            curr, dist, path = queue.pop(0)

            if curr in visited:
                continue
            visited.add(curr)

            if dist > 0:
                impacted[curr] = {"distance": dist, "path": path}

            if dist < max_depth:
                neighbors = self.adjacency.get(curr, [])
                for edge in neighbors:
                    if edge["direction"] == "incoming":
                        new_path = path + [f"({edge['relation']})"]
                        queue.append((edge["target"], dist + 1, new_path))

        return {
            "target": target_id,
            "impacted_nodes": [{"id": k, **v} for k, v in impacted.items()],
            "stats": {"total_impacted": len(impacted)},
        }

    def print_report(self, report: Optional[ImpactReport]) -> None:
        if not report:
            print(f"{Colors.FAIL}❌ Target not found in Cognitive Loom.{Colors.ENDC}")
            return

        print(f"\n{Colors.HEADER}🔮 The Architect's Gaze: Impact Analysis{Colors.ENDC}")
        print(f"{Colors.BOLD}Target Node:{Colors.ENDC} {report['target']}")
        print(
            f"{Colors.BOLD}Blast Radius:{Colors.ENDC} {len(report['impacted_nodes'])} artifacts/files impacted.\n"
        )

        by_dist = {}
        for node in report["impacted_nodes"]:
            d = node["distance"]
            if d not in by_dist:
                by_dist[d] = []
            by_dist[d].append(node)

        for d in sorted(by_dist.keys()):
            label = "Direct Impact" if d == 1 else f"Ripple Effect (Order {d})"
            color = Colors.FAIL if d == 1 else Colors.WARNING
            print(f"{color}--- {label} ---{Colors.ENDC}")
            for item in by_dist[d]:
                " <- ".join(item["path"]) if item["path"] else ""
                print(f"  • {item['id']}")


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Simulate systemic impact of a change."
    )
    parser.add_argument(
        "--target", required=True, help="Artifact ID or Filename to analyze."
    )
    parser.add_argument(
        "--depth", type=int, default=2, help="Depth of recursive analysis."
    )
    args = parser.parse_args()

    analyzer = ImpactAnalyzer()
    analyzer.load_loom(Path(GRAPH_PATH))
    analyzer.scan_codebase(CODE_ROOTS)

    report = analyzer.simulate_impact(args.target, args.depth)
    analyzer.print_report(report)


if __name__ == "__main__":
    main()
