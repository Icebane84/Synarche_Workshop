"""
artifact_anchor:
  id: INFR.FIND_UNLINKED.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: INFRA
  celestial_class: STAR
  tier: COMPUTE
  state: ACTIVE
  ethos: SOVEREIGN_COMPUTE_COMPONENT
  relations: []
"""

"""# TOOL-HPRI-004: The Link Scanner (Priestess's Insight).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-004`                                          |
| **2. Official Name**   | `find_unlinked.py`                                       |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `OSLM`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Tactical**                                             |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Link Discovery**                                       |
| **11. Catalyst**       | **Void Mapping**                                         |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for anomaly detection.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Priestess's Veil
# Primary Stat Buff: Intuition (+10), Perception (+15)
# Passive Ability: The Silver Thread (Anomaly Detection)
# Cognitive Load Cost: Medium
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: FIND_UNLINKED` | Scan for Naked Artifact IDs | Integrity Audit |
| `⚡ EXECUTE: MAP_VOID` | List All Missing Links | Connection Discovery |
"""

import argparse
import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def scan_file(filepath: str, filename: str, targets: list[str]) -> None:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split by lines to give line numbers
    lines = content.split("\n")
    for i, line in enumerate(lines):
        for target in targets:
            if target in line:
                logger.info(f"{filename}:{i + 1}: {line.strip()}")


def main(docs_dir: str, targets: list[str]) -> None:
    logger.info(f"Scanning for {targets}...")
    if not os.path.exists(docs_dir):
        logger.error(f"Docs directory not found: {docs_dir}")
        return

    files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]
    for f in files:
        if f.startswith("UMB-OSLM-001"):
            continue  # Skip registry itself searching for itself
        scan_file(os.path.join(docs_dir, f), f, targets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scanner for unlinked targets in Markdown files.")
    parser.add_argument("--docs-dir", required=True, help="Path to the documentation directory.")
    parser.add_argument("--targets", nargs="+", required=True, help="List of target strings/IDs to search for.")
    args = parser.parse_args()

    main(args.docs_dir, args.targets)
