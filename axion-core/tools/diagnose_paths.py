"""# TOOL-SENT-005: Path Diagnostic Tool (Audit Engine).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-005`                                          |
| **2. Official Name**   | `diagnose_paths.py`                                      |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Path Verification**                                    |
| **11. Catalyst**       | **Diagnostic Scan**                                      |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for path diagnostics.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Perceptivity (+15), Logic (+5)
# Passive Ability: The Unblinking Eye (Environment Check)
# Cognitive Load Cost: Low
# XP Award Value: 25 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: DIAGNOSE_PATHS` | Scan File Visibility | Debugging |
| `⚡ EXECUTE: FIND_LOST` | Identify Missing Files | Restoration |
"""

import logging
import os

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

target_dir = r"c:\Users\Chris\Synarche_Workspace\Where_Light_Fades\Unfiltered\Where Light Fades\Master Documents"

logger.info(f"Scanning: {target_dir}")
if not os.path.exists(target_dir):
    logger.error("DIRECTORY DOES NOT EXIST!")
else:
    logger.info("Directory exists.")
    files = os.listdir(target_dir)
    logger.info(f"Found {len(files)} items:")
    for f in files:
        full = os.path.join(target_dir, f)
        if os.path.isfile(full):
            logger.info(f" - [FILE] {f} ({os.path.getsize(full)} bytes)")
        else:
            logger.info(f" - [DIR ] {f}")

    logger.info("-" * 20)
    # Check specifically for the files we miss
    missing = [
        "Master_Outline_Where_Light_Fades.md",
        "Master_Refined_Where_Light_Fades.md",
    ]
    for m in missing:
        p = os.path.join(target_dir, m)
        if os.path.exists(p):
            logger.info(f"SUCCESS: {m} found at {p}")
        else:
            logger.info(f"FAILURE: {m} NOT found at {p}")
