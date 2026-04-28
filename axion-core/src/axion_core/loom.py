"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `UMB-LOOM-002`                | The Sovereign ID. |
| **Official Name**   | `loom.py`                     | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `TECH.Integration`            | The Subject.      |
| **Celestial Class** | `[PLANET]`                    | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Cognitive Weaving (Law 02)**
> Purpose: To weave disparate data streams into a cohesive Knowledge Graph.
> Governed By: UMB-GTSF-001
"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import json
import logging
import os
import re
from datetime import datetime

# Setup Logging similar to 'The Void'
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [LOOM] %(message)s")
logger = logging.getLogger("CognitiveLoom")


class CognitiveLoom:
    """
    The Weaver.
    Ingests artifacts, extracts metadata, and identifies semantic edges.
    """

    def __init__(self, workspace_root: str) -> None:
        self.root = workspace_root
        self.tapestry = {
            "nodes": {},
            "edges": [],
            "metadata": {
                "genesis": datetime.now().isoformat(),
                "node_count": 0,
                "edge_density": 0.0,
            },
        }

    def ingest_artifact(self, file_path: str) -> dict | None:
        """
        Reads an artifact and parses it into a MemoryNode structure.
        """
        try:
            abs_path = os.path.abspath(file_path)
            with open(abs_path, encoding="utf-8") as f:
                content = f.read()

            metadata = self._extract_header_metadata(content)

            node_id = metadata.get("Artifact ID", os.path.basename(abs_path))
            node = {
                "id": node_id,
                "path": abs_path,
                "type": self._determine_type(metadata),
                "tier": self._infer_tier(metadata),  # Eidetic Memory Tier
                "metadata": metadata,
                "content_preview": content[:200],
                "links": self._extract_links(content),
                "last_accessed": datetime.now().isoformat(),
                "integrity_hash": hash(content),  # Simple integrity check
            }

            # Weave into Tapestry
            self.tapestry["nodes"][node_id] = node
            self._weave_edges(node_id, node["links"])

            logger.info(f"Ingested Node: {node_id}")
            return node

        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {e}")
            return None

    def _extract_header_metadata(self, content: str) -> dict[str, str]:
        """
        Extracts OGLN v10.0 metadata from the file header or table.
        Supports:
        - Genesis Stamp
        - Key-Value pairs (Blockquote or bolded lines)
        - Table Attributes
        """
        metadata = {}

        # 1. Genesis Stamp
        genesis_match = re.search(r"\*\*Genesis Stamp:?\s*(.*?)\*\*", content, re.IGNORECASE)
        if genesis_match:
            metadata["Genesis"] = genesis_match.group(1).strip()

        # 2. Key-Value Pairs (Blockquote or bolded lines)
        # Matches: > **Key**: Value  OR  **Key**: Value
        kv_matches = re.findall(r"\*\*([A-Za-z0-9\s]+?)\*\*[:\s]+(.*?)(?:\n|$)", content)
        for key, value in kv_matches:
            if key not in metadata:  # Don't overwrite if already found
                metadata[key.strip()] = value.strip()

        # 3. Table Attributes
        # Matches | **Key** | Value | (with optional bolding on key)
        table_matches = re.findall(r"\|\s*\*\*?(.*?)\*\*?\s*\|\s*(.*?)\s*\|", content)
        for key, value in table_matches:
            if key.strip() not in metadata:
                metadata[key.strip()] = value.strip()

        return metadata

    def _determine_type(self, metadata: dict) -> str:
        """Determines the artifact type based on its functional domain."""
        domain = metadata.get("Domain", "UNKNOWN")
        if "PHL" in domain:
            return "Entity"
        if "GVRN" in domain:
            return "Protocol"
        if "TECH" in domain:
            return "Engine"
        return "Artifact"

    def _extract_links(self, content: str) -> list[str]:
        """
        Finds explicit links to other artifacts.
        Matches [ID](path) or specific 'reference' tags.
        """
        # Simple regex for [Text](path) - robust implementation would resolve paths
        links = re.findall(r"\[(.*?)\]\((.*?)\)", content)
        return [
            link[0] for link in links if "http" not in link[1] and hasattr(link, "__getitem__")
        ]  # Internal links only

    def _weave_edges(self, source_id: str, targets: list[str], link_type: str = "references", strength: float = 1.0) -> None:
        """
        Creates weighted edge entries in the Tapestry.
        """
        for target in targets:
            # Check for existing edge to update strength or prevent duplicates
            exists = False
            for edge in self.tapestry["edges"]:
                if edge["source"] == source_id and edge["target"] == target:
                    edge["weight"] = max(edge["weight"], strength)
                    edge["type"] = link_type
                    exists = True
                    break

            if not exists:
                self.tapestry["edges"].append(
                    {
                        "source": source_id,
                        "target": target,
                        "type": link_type,
                        "weight": strength,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

    def _infer_tier(self, metadata: dict) -> str:
        """
        Infers the Memory Tier based on artifact metadata.
        Tiers: Active (Strategic/Current), Retained (Reference), Archival (Historical).
        """
        status = metadata.get("Status", "ACTIVE").upper()
        if "ACTIVE" in status or "PROMPT" in str(metadata):
            return "Active"
        if "CANON" in status or "STANDARD" in status:
            return "Retained"
        return "Archival"

    def export_tapestry(self, output_path: str) -> None:
        """
        Persists the current Knowledge Graph to JSON.
        """
        self.tapestry["metadata"]["node_count"] = len(self.tapestry["nodes"])
        if self.tapestry["metadata"]["node_count"] > 0:
            self.tapestry["metadata"]["edge_density"] = (
                len(self.tapestry["edges"]) / self.tapestry["metadata"]["node_count"]
            )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.tapestry, f, indent=4)
        logger.info(f"Tapestry exported to {output_path}")


if __name__ == "__main__":
    # Self-Test
    loom = CognitiveLoom(".")
    print("Loom Online.")
