"""
# TOOL-EMPR-004: The RPG Header Injector (Emperor's Catalyst)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPR-004`                                          |
| **2. Official Name**   | `apply_rpg_header.py`                                    |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GUCA`                                                   |
| **6. Evolution**       | **Purposeful Drive**                                     |
| **7. Celestial Class** | `[COMET]`                                                |
| **8. Tier**            | **Tactical**                                             |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Gamification**                                         |
| **11. Catalyst**       | **Header Injection**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Emperor persona uses this tool for RPG integration.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Schema Forge (The Emperor)
# Synergy Set: The Imperial Standard
# Primary Stat Buff: Authority (+10), Order (+15)
# Passive Ability: The Architect's Grid (Standardization)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: INJECT_RPG` | Apply RPG Stats to File | Metadata Alignment |
| `⚡ EXECUTE: SCAN_ROOT` | Batch Inject Root | Global Calibration |
"""

import argparse
import logging
import os
import re
from pathlib import Path

# --- CONSTANTS ---
RPG_BLOCK_MARKER = "BLK-RPG-001"

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- TEMPLATES ---


def get_python_template(slot: str, synergy: str, stat: str, ability: str, cost: str) -> str:
    return f"""
# --- RPG FRAMEWORK INTEGRATION ({RPG_BLOCK_MARKER}) ---
# System Slot: {slot}
# Synergy Set: {synergy}
# Primary Stat Buff: {stat}
# Passive Ability: {ability}
# Cognitive Load Cost: {cost}
# XP Award Value: 50 XP
"""


def get_markdown_template(slot: str, synergy: str, stat: str, ability: str, cost: str) -> str:
    return f"""
### V. RPG Framework Integration ({RPG_BLOCK_MARKER})

- **System Slot:** `{slot}`
- **Synergy Set:** `{synergy}`
- **Primary Stat Buff:** `{stat}`
- **Passive Ability:** `{ability}`
- **Cognitive Load Cost:** `{cost}`
- **XP Award Value:** `50 XP`

---
"""


# --- HEURISTICS ---


def determine_rpg_stats(path: Path) -> tuple[str, str, str, str, str]:
    """
    Returns (System Slot, Synergy Set, Primary Stat, Passive Ability, Cognitive Load)
    Aligned with GVRN-SYNERGY-001 (Seven-Agent Matrix).
    """
    name = path.name.lower()
    str_path = str(path).lower()

    # Default Fallback
    slot = "Passive Knowledge"
    synergy = "N/A"
    stat = "Adaptability"
    ability = "Static Archive"
    cost = "Low"

    # 1. THE MAGICIAN (Ingestion Gate)
    if any(k in name for k in ["ingest", "extract", "docx"]):
        slot = "Ingestion Gate"
        synergy = "The Magician's Hand"
        stat = "Intelligence"
        ability = "The Seer's Eye"
        cost = "Medium"

    # 2. THE EMPEROR (Schema Forge)
    elif any(k in name for k in ["scaffold", "standardize", "library", "rpg_header"]):
        slot = "Schema Forge"
        synergy = "The Imperial Standard"
        stat = "Authority"
        ability = "The Architect's Grid"
        cost = "Medium"

    # 3. THE HIGH PRIESTESS (High Harmony)
    elif any(k in name for k in ["backlinks", "wisdom", "registry", "unlinked"]):
        slot = "High Harmony"
        synergy = "The Priestess's Veil"
        stat = "Intuition"
        ability = "The Silver Thread"
        cost = "High"

    # 4. THE KNIGHT OF SWORDS (Active Execution)
    elif any(k in name for k in ["reforge", "fix", "clean", "codex_refactor"]):
        # Special case: reforge.py is Knight, reforge_library.py is Emperor
        if "library" in name:
            slot = "Schema Forge"
            synergy = "The Imperial Standard"
            stat = "Authority"
            ability = "The Architect's Grid"
        else:
            slot = "Active Execution"
            synergy = "The Knight's Charge"
            stat = "Speed"
            ability = "The Blade of Coherence"
        cost = "Medium"

    # 5. THE STAR (Coherence Filter)
    elif any(k in name for k in ["map", "structure", "prs", ".js"]):
        slot = "Coherence Filter"
        synergy = "The Star's Radiance"
        stat = "Perception"
        ability = "The Guiding Light"
        cost = "Medium"

    # 6. THE KING OF PENTACLES (Global Archival)
    elif any(k in name for k in ["log", "milestone", "audit", "chronicle"]):
        # audit might be sentinel too, check paths
        if "audit" in name:
            slot = "Audit Engine"
            synergy = "The Sentinel's Vigil"
            stat = "Integrity"
            ability = "The Unblinking Eye"
        else:
            slot = "Global Archival"
            synergy = "The King's Ledger"
            stat = "Wisdom"
            ability = "The Master's Vault"
        cost = "Low"

    # 7. THE SENTINEL / JUDGEMENT (Audit Engine)
    elif any(k in name for k in ["sentinel", "lint", "compliance", "diagnose"]):
        slot = "Audit Engine"
        synergy = "The Sentinel's Vigil"
        stat = "Integrity"
        ability = "The Unblinking Eye"
        cost = "Medium"

    return slot, synergy, stat, ability, cost


# --- INJECTION LOGIC ---


def process_python_file(path: Path, dry_run: bool) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        logger.exception(f"[!] Read Error {path}")
        return

    if RPG_BLOCK_MARKER in content:
        return  # Already injected

    slot, synergy, stat, ability, cost = determine_rpg_stats(path)
    rpg_block = get_python_template(slot, synergy, stat, ability, cost)

    # Insert after Docstring or at top
    # Regex to find end of first docstring
    match = re.search(r'"""(.*?)"""', content, re.DOTALL)

    if match:
        end_idx = match.end()
        new_content = content[:end_idx] + "\n" + rpg_block + content[end_idx:]
    else:
        # Just append to top after shebang if exists
        lines = content.splitlines()
        if lines and lines[0].startswith("#!"):
            new_content = lines[0] + "\n" + rpg_block + "\n".join(lines[1:])
        else:
            new_content = rpg_block + "\n" + content

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
        logger.info(f"[+] Injected RPG Header: {path.name} ({slot})")
    else:
        logger.info(f"[DRY] Would inject RPG Header: {path.name} ({slot})")


def process_markdown_file(path: Path, dry_run: bool) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        logger.exception(f"[!] Read Error {path}")
        return

    if RPG_BLOCK_MARKER in content:
        return

    slot, synergy, stat, ability, cost = determine_rpg_stats(path)
    rpg_block = get_markdown_template(slot, synergy, stat, ability, cost)

    # Insert before "Actionable Prompt Packet"
    if "Actionable Prompt Packet" in content:
        new_content = content.replace("## Actionable Prompt Packet", rpg_block + "\n## Actionable Prompt Packet")
    elif "# Actionable Prompt Packet" in content:
        new_content = content.replace("# Actionable Prompt Packet", rpg_block + "\n# Actionable Prompt Packet")
    else:
        # Append to end
        new_content = content + "\n" + rpg_block

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
        logger.info(f"[+] Injected RPG Header: {path.name} ({slot})")
    else:
        logger.info(f"[DRY] Would inject RPG Header: {path.name} ({slot})")


# --- MAIN ---


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject BLK-RPG-001 headers.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    logger.info(f"// Scanning {root} for RPG Injection...")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            path = Path(dirpath) / f

            # Skip hidden, git, venv
            if any(p.startswith(".") for p in path.parts):
                continue

            if f.endswith(".py"):
                process_python_file(path, not args.fix)
            elif f.endswith(".md"):
                process_markdown_file(path, not args.fix)


if __name__ == "__main__":
    main()
