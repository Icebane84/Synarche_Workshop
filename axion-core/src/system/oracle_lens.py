#!/usr/bin/env python3

# ==========================================
# 1. PEP 723: INLINE SCRIPT METADATA
# ==========================================
# /// script
# requires-python = ">=3.10"
dependencies = []
#     "rich",
#     "pydantic"
# ]
# ///

# ==========================================
# 2. SYNARCHE SOVEREIGN METADATA (UIP-V15)
# ==========================================
"""
# ARTIFACT ID: SYNG.TOOL.Oracle_Lens_API
# Domain: AXION | State: ACTIVE | Criticality: CORE
# Objective: Parses local Synarche Markdown artifacts into structured SynapseNode and SynergyEdge JSON payloads.
# Relations: IMPLEMENTS: SYNG.SKILL.Oracle_Lens_API
"""

# [OMNI-ARTIFACT-ANCHOR] ID: SYNG.TOOL.Oracle_Lens_API VER: v15.0 [OMEGA] STATUS: ACTIVE TS: 2026-04-22

import json
import logging
import os
import re
import sys
from typing import Any, Dict, List

# ------------------------------------------
# 3. KINETIC EXECUTION LOGIC
# ------------------------------------------


def setup_logger():
    """Initializes Phoenix-Class logging for the script."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    return logging.getLogger("Axion.OracleLens")


log = setup_logger()


class OracleLensParser:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []

        # OMEGA v15.0 Extraction Regex Patterns
        self.re_id = re.compile(r"\|\s*\*\*Artifact ID\*\*\s*\|\s*(?:`?)([^`\|]+)(?:`?)\s*\|")
        self.re_name = re.compile(r"\|\s*\*\*Official Name\*\*\s*\|\s*(?:`?)([^`\|]+)(?:`?)\s*\|")
        self.re_class = re.compile(
            r"\|\s*\*\*Celestial Class\*\*\s*\|\s*(?:`?)(?:\[?)(STAR|PLANET|MOON|ASTEROID|VOID)(?:\]?)(?:`?)\s*\|",
            re.IGNORECASE,
        )

        self.re_coherence = re.compile(r"\|\s*\*\*Coherence\*\*\s*\|\s*(?:`?)([0-9.]+)(?:`?)\s*\|")
        self.re_resonance = re.compile(r"\|\s*\*\*Resonance\*\*\s*\|\s*(?:`?)([0-9.]+)(?:`?)\s*\|")
        self.re_stability = re.compile(r"\|\s*\*\*Stability\*\*\s*\|\s*(?:`?)([^`\|]+)(?:`?)\s*\|")

        # Synergy Table Match: | `Target_ID` | `RELATION_TYPE` | Impact |
        self.re_synergy_row = re.compile(r"\|\s*`([^`]+)`\s*\|\s*`([A-Z_]+)`\s*\|")

    def parse_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Phase 1: Identity Extraction (Block A)
        id_match = self.re_id.search(content)
        if not id_match:
            return  # Skip non-compliant files

        node_id = id_match.group(1).strip()
        name_match = self.re_name.search(content)
        label = name_match.group(1).strip() if name_match else node_id

        class_match = self.re_class.search(content)
        celestial_class = class_match.group(1).upper() if class_match else "ASTEROID"

        # Phase 2: State Vector Extraction (Block B)
        coh_match = self.re_coherence.search(content)
        coherence = float(coh_match.group(1)) if coh_match else 0.5

        res_match = self.re_resonance.search(content)
        resonance = float(res_match.group(1)) if res_match else 0.5

        stab_match = self.re_stability.search(content)
        stability = stab_match.group(1).strip() if stab_match else "Volatile"

        node = {
            "id": node_id,
            "label": label,
            "celestialClass": celestial_class,
            "stateVector": {"coherence": coherence, "resonance": resonance, "stability": stability},
            "superposition": [0, 0, 0],  # To be calculated by the React frontend
            "isFocused": False,
        }
        self.nodes.append(node)

        # Phase 3: Synergy Extraction (Block D)
        # Isolate Block D to prevent false positive table matches
        block_d_start = content.find("Block D: Standardized Synergy Block")
        block_e_start = content.find("Block E: Ethos")

        if block_d_start != -1:
            search_area = content[block_d_start:block_e_start] if block_e_start != -1 else content[block_d_start:]
            synergy_matches = self.re_synergy_row.findall(search_area)

            for target_id, relation_type in synergy_matches:
                # Calculate relational weight based on source coherence
                weight = 1.0 if coherence >= 0.9 else 0.5
                edge = {
                    "id": f"{node_id}->{target_id}",
                    "source": node_id,
                    "target": target_id,
                    "relationType": relation_type,
                    "weight": weight,
                }
                self.edges.append(edge)

    def traverse_and_parse(self):
        log.info(f"Initiating Substrate Sweep in: {self.target_dir}")
        file_count = 0
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".md"):
                    self.parse_file(os.path.join(root, file))
                    file_count += 1

        log.info(f"Sweep Complete. Processed {file_count} files.")
        log.info(f"Extracted Nodes: {len(self.nodes)} | Extracted Edges: {len(self.edges)}")

    def export_json(self, output_path: str):
        payload = {"nodes": self.nodes, "edges": self.edges}
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        log.info(f"Oracle Matrix exported to {output_path}")


def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    governance_dir = os.path.join(workspace_root, "_governance")
    output_file = os.path.join(workspace_root, "axion-core/assets/oracle_matrix.json")

    if not os.path.exists(governance_dir):
        log.error(f"Governance directory not found at {governance_dir}")
        sys.exit(1)

    parser = OracleLensParser(governance_dir)
    parser.traverse_and_parse()
    parser.export_json(output_file)


if __name__ == "__main__":
    main()
