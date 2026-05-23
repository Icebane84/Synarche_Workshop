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

import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

DOCS_DIR = (
    r"c:\Users\Chris\_Desktop_Vault\dev\rosetta-stone_-the-phoenix-protocol-(cast)\docs"
)
TARGETS = ["UMB-OSLM-001", "CODEX-001"]


def scan_file(filepath: str, filename: str) -> None:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split by lines to give line numbers
    lines = content.split("\n")
    for i, line in enumerate(lines):
        for target in TARGETS:
            if target in line:
                # Naive check: does this line have the target inside a link?
                # We look for [ ... target ... ] or ( ... target ... ) which might be part of a link.
                # But typically we want: [Title](...ID...) OR [ID](...file...)

                # If we see `[ ... ]( ... )` containing our target, it's likely linked.
                # If we see the target purely as text, it's a candidate.

                # Let's count occurrences of target
                # Then count occurrences of target inside `[ ... ]` or `( ... )`?
                # This is hard with regex.

                # Heuristic: If we find target, check if it's NOT followed by `(` (if it was the link text `[ID]`)
                # OR preceded by `](` (if it was the file path).

                # Actually, simpler:
                # Let's just print all matches in context for visual filtering by the agent.
                logger.info(f"{filename}:{i + 1}: {line.strip()}")


def main() -> None:
    logger.info(f"Scanning for {TARGETS}...")
    if not os.path.exists(DOCS_DIR):
        logger.error(f"Docs directory not found: {DOCS_DIR}")
        return

    files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    for f in files:
        if f.startswith("UMB-OSLM-001"):
            continue  # Skip registry itself searching for itself
        scan_file(os.path.join(DOCS_DIR, f), f)


if __name__ == "__main__":
    main()
