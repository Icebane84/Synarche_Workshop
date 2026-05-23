"""# UMB-OSLM-GPS-001: The OSLM Navigator (System Spine).

# I. Universal Identification & Provenance (The Vector Signature)
| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `UMB-OSLM-GPS-001` |
| **2. Official Name** | `oslm_gps.py` |
| **3. Version** | **v15.0 [OMEGA]** |
| **4. Provenance** | **Reforged: 2026-04-28** |
| **5. Domain** | `ARCH` |
| **6. Evolution** | **Purposeful Drive** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. Status (State)** | `[ACTIVE]` |
| **10. Ethos** | **Guardian of Connectivity** |
| **11. Integrity Hash** | `[UIP-V15-LOCK]` |

---

### **I.B. Axiom Reference**
> "To navigate the spine is to master the system." — Axiom of Navigation
"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

# Default path to the OSLM artifact.
# Ideally this would be dynamic, but for now we hardcode the known location or take it as an arg.
DEFAULT_OSLM_PATH = r"c:\Users\Chris\Synarche_Workspace\_governance\UMB-OSLM-001_OmniLogSynergisticLinksMatrix_v7.0.md"


MIN_TABLE_COLUMNS = 3


class OSLMGPS:
    """The OSLM GPS (Global Positioning System) for the Phoenix Protocol Library.

    It reads the OSLM Markdown file, parses the relational tables, and
    provides methods to query connections ("Traverse the Spine").
    """

    def __init__(self, oslm_path: str = DEFAULT_OSLM_PATH) -> None:
        """Initialize the OSLM GPS.

        Args:
            oslm_path: Absolute path to the UMB-OSLM-001 markdown file.

        """
        self.oslm_path = oslm_path
        self.graph: dict[str, list[dict[str, str]]] = (
            {}
        )  # Adjacency list: Source -> [{Target, Relation, Score}]
        self.nodes: set[str] = set()
        self._load_matrix()

    def _load_matrix(self) -> None:
        """Parses the OSLM Markdown file to populate the graph."""
        if not os.path.exists(self.oslm_path):
            logger.critical(f"CRITICAL: OSLM Artifact not found at {self.oslm_path}")
            return

        try:
            with open(self.oslm_path, encoding="utf-8") as f:
                content = f.read()

            # Split by pipe to parse table columns efficiently
            lines = content.split("\n")

            for line in lines:
                stripped = line.strip()
                if not stripped.startswith("|"):
                    continue

                # Skip header separators (e.g. |:---|:---|)
                if "---" in stripped:
                    continue

                # Parse row via split
                # Format: | Source | Target | Relation | ...
                parts = [p.strip() for p in stripped.split("|")]

                # Filter out empty strings typical of markdown tables (start/end pipes)
                valid_parts = [p for p in parts if p]

                if len(valid_parts) >= MIN_TABLE_COLUMNS:
                    source_raw = valid_parts[0]
                    target_raw = valid_parts[1]
                    relation_raw = valid_parts[2]

                    # Clean up artifact IDs
                    source = self._clean_id(source_raw)
                    target = self._clean_id(target_raw)
                    relation = self._clean_id(relation_raw)

                    if source and target:
                        self._add_edge(source, target, relation)

        except Exception:
            logger.exception("ERROR: Failed to parse OSLM")

    def _clean_id(self, raw_text: str) -> str:
        """Removes markdown formatting (*, `) to get the raw ID."""
        return raw_text.replace("*", "").replace("`", "").strip()

    def _add_edge(self, source: str, target: str, relation: str) -> None:
        """Adds a directed edge to the graph."""
        self.nodes.add(source)
        self.nodes.add(target)

        if source not in self.graph:
            self.graph[source] = []

        self.graph[source].append({"target": target, "relation": relation})

    def traverse_links(self, start_node: str) -> list[dict[str, str]]:
        """Traverses all immediate links from a given node.

        Args:
            start_node: The Artifact ID to start from (e.g. 'UMB-CSE-001').

        Returns:
            List of dictionaries containing edge details.

        """
        return self.graph.get(start_node, [])

    def find_path(self, start_node: str, end_node: str) -> list[str] | None:
        """Finds a path between two nodes using BFS.

        Args:
            start_node: Source Artifact ID.
            end_node: Target Artifact ID.

        Returns:
            List of Artifact IDs representing the path, or None if no path found.

        """
        if start_node not in self.graph:
            return None

        queue = [(start_node, [start_node])]
        visited = set()

        while queue:
            vertex, path = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)

                if vertex == end_node:
                    return path

                for edge in self.graph.get(vertex, []):
                    neighbor = edge["target"]
                    if neighbor not in visited:
                        queue.append((neighbor, [*path, neighbor]))
        return None

    def get_all_nodes(self) -> list[str]:
        """Returns a sorted list of all known nodes in the matrix."""
        return list(self.nodes)
