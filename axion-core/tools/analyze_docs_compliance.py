"""
# TOOL-SENT-004: Simple Compliance Analyzer (Audit Engine)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-004`                                          |
| **2. Official Name**   | `analyze_docs_compliance.py`                             |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Rapid Analysis**                                       |
| **11. Catalyst**       | **Documentation Scan**                                   |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for rapid analysis.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+5), Logic (+10)
# Passive Ability: The Unblinking Eye (Bulk Analysis)
# Cognitive Load Cost: Low
# XP Award Value: 25 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: ANALYZE_DOCS` | Quick Compliance Scan | Rapid Audit |
| `⚡ EXECUTE: SCAN_DOCS` | Bulk Integrity Check | Entropy Detection |
"""

import logging
import os
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TARGET_DIR = r"c:\Users\Chris\_Desktop_Vault\dev\rosetta-stone_-the-phoenix-protocol-(cast)\docs"
REQUIRED_VERSION = "v11.0"


def parse_uip(content: str) -> dict[str, str]:
    uip: dict[str, str] = {}
    lines = content.split("\n")
    in_uip = False
    for line in lines:
        if "Universal Identification & Provenance" in line:
            in_uip = True
            continue
        if in_uip and line.strip().startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                key = parts[1].replace("*", "")
                val = parts[2].replace("`", "").strip()
                if key and val and "---" not in key:
                    uip[key] = val
        if in_uip and line.strip() == "---":
            # End of header block usually
            pass
    return uip


def check_file(filepath: str) -> list[str]:
    filename = os.path.basename(filepath)
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Read Error: {e}"]

    issues: list[str] = []

    # 1. Filename Check
    if not filename.lower().endswith(f"_{REQUIRED_VERSION.lower()}.md"):
        v_match = re.search(r"_v(\d+\.\d+)\.md$", filename, re.IGNORECASE)
        if v_match:
            issues.append(f"Filename Version Mismatch: Found {v_match.group(1)}, Expected {REQUIRED_VERSION}")
        elif filename != "README.md":
            issues.append("Filename Format Invalid (No version suffix)")

    # 2. UIP Header Check
    uip = parse_uip(content)
    if not uip:
        if filename != "README.md":
            issues.append("Missing UIP Header")
    elif "Version" in uip:
        if uip["Version"] != REQUIRED_VERSION:
            issues.append(f"UIP Version Mismatch: Found {uip['Version']}, Expected {REQUIRED_VERSION}")
    else:
        issues.append("UIP Header missing 'Version' key")

    # 3. Actionable Prompt Packet Check
    if "Actionable Prompt Packet" not in content and "Catalyst Prompt Packets" not in content:
        if filename != "README.md":
            issues.append("Missing Actionable Prompt Packet")

    return issues


# Suffix normalizer removed as redundant.


def main() -> None:
    logger.info(f"Auditing {TARGET_DIR} for {REQUIRED_VERSION} compliance...\n")

    if not os.path.exists(TARGET_DIR):
        logger.error(f"[!] Target Directory not found: {TARGET_DIR}")
        return

    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(".md")]
    total_files = len(files)
    compliant_files = 0

    for f in files:
        path = os.path.join(TARGET_DIR, f)
        issues = check_file(path)

        if issues:
            logger.info(f"[FAIL] {f}")
            for i in issues:
                logger.info(f"  - {i}")
        else:
            logger.info(f"[PASS] {f}")
            compliant_files += 1

    logger.info("-" * 40)
    logger.info(f"Summary: {compliant_files}/{total_files} compliant.")


if __name__ == "__main__":
    main()
