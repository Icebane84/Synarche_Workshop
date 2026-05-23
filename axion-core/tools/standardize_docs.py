"""
# TOOL-EMPR-002: Doc Standardizer (Emperor's Law)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPR-002`                                          |
| **2. Official Name**   | `standardize_docs.py`                                    |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Uniformity**                                           |
| **11. Catalyst**       | **Header Alignment**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Emperor persona uses this tool for standardization.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Schema Forge (The Emperor)
# Synergy Set: The Imperial Standard
# Primary Stat Buff: Authority (+10), Order (+10)
# Passive Ability: The Architect's Grid (Standardization)
# Cognitive Load Cost: Medium
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: STANDARDIZE` | Enforce Header v11.0 | Protocol Compliance |
| `⚡ EXECUTE: RENAME_V11` | Bulk Rename to v11.0 | Consistency |
"""

import logging
import os
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TARGET_DIR = r"c:\Users\Chris\_Desktop_Vault\dev\rosetta-stone_-the-phoenix-protocol-(cast)\docs"
NEW_VERSION = "v11.0"


def update_file_content(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 1. Update UIP Header Version
    # Regex to find | **Version** | ... |
    # We want to be careful not to break table formatting
    # Pattern: | **Version** | `v...` | or | **Version** | v... |

    def version_replacer(_: re.Match) -> str:
        # Keep the structure, just change the value part
        return f"| **Version** | `{NEW_VERSION}` |"

    # Try matching with backticks first
    content = re.sub(r"\|\s*\*\*Version\*\*\s*\|\s*`?v\d+\.\d+`?\s*\|", version_replacer, content)

    # Also update the title section if it mentions version: **Version:** v11.0
    content = re.sub(r"\*\*Version:\*\* v\d+\.\d+", f"**Version:** {NEW_VERSION}", content)

    # 3. Check for Actionable Prompt Packet (Footer)
    packet_markers = ["Actionable Prompt Packet", "Catalyst Prompt Packets"]
    has_packet = any(marker in content for marker in packet_markers)

    if not has_packet:
        footer = """
---

## V. Actionable Prompt Packet

### Packet A: Standard Compliance Check
> "Acting as the Protocol Auditor, review this document against the Phoenix Codex v11.0. Does it adhere to the Luminous Coherence standard?"

### Packet B: Operational Activation
> "Simulate the execution of this protocol. What are the immediate output artifacts?"

---
"""
        content += footer.lstrip()

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def rename_file(filename: str) -> str:
    # Pattern: PREFIX-TYPE-ID_Name_vVersion.md
    # We want to find the _vXXXX.md part and replace with _v11.0.md

    # Regex for existing version suffix
    match = re.search(r"(_v\d+\.\d+)(\.md)$", filename, re.IGNORECASE)

    if match:
        base = filename[: match.start(1)]
        new_name = f"{base}_{NEW_VERSION}.md"
    else:
        # No version suffix? Just append or replace extension
        base = os.path.splitext(filename)[0]
        new_name = f"{base}_{NEW_VERSION}.md"

    return new_name


def main() -> None:
    logger.info(f"Standardizing docs in {TARGET_DIR} to {NEW_VERSION}...\n")

    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(".md") and f != "README.md"]

    renamed_count = 0
    updated_count = 0

    for f in files:
        old_path = os.path.join(TARGET_DIR, f)

        # 1. Update Content First
        if update_file_content(old_path):
            logger.info(f"  [UPDATED] Content for {f}")
            updated_count += 1

        # 2. Rename File
        new_name = rename_file(f)
        if new_name != f:
            new_path = os.path.join(TARGET_DIR, new_name)
            try:
                os.rename(old_path, new_path)
                logger.info(f"  [RENAMED] {f} -> {new_name}")
                renamed_count += 1
            except OSError as e:
                logger.error(f"  [ERROR] Could not rename {f}: {e}")

    logger.info("-" * 40)
    logger.info(f"Operation Complete. Content Updates: {updated_count}, Renames: {renamed_count}")


if __name__ == "__main__":
    main()
