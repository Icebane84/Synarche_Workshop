"""
# TOOL-HPRI-001: The Backlink Weaver (High Harmony)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-001`                                          |
| **2. Official Name**   | `forge_backlinks.py`                                     |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `OSLM`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Interconnection**                                      |
| **11. Catalyst**       | **Link Forging**                                         |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for backlinking.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
UMB-OSLM-001, INDEXES, The registry provides the map for this tool.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Priestess's Veil
# Primary Stat Buff: Intuition (+15), Coherence (+10)
# Passive Ability: The Silver Thread (Relational Mapping)
# Cognitive Load Cost: High
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: FORGE_LINKS` | Parse OSLM & Inject Links | Relational Integrity |
| `⚡ EXECUTE: WEAVE` | Global Link Synthesis | High Coherence |
"""

import argparse
import logging
import os
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_artifact_map(registry_path: str) -> dict[str, str]:
    """Parses the UMB-OSLM-001 table to build the ID->RelPath map."""
    artifact_map = {}
    try:
        with open(registry_path, encoding="utf-8") as f:
            content = f.read()

        # Regex to capture table rows: | `ID` | [Title](RelPath) | ...
        # Match: | `(ID)` | [(Title)]((RelPath)) |
        matches = re.findall(r"\| `([^`]+)` \| \[.*?\]\(([^)]+)\)", content)

        for mid, rel_path in matches:
            if mid == "Unknown":
                continue
            # rel_path is relative to the registry file.
            # We will store the absolute path so we can recalculate relative to any file.
            abs_target = os.path.abspath(os.path.join(os.path.dirname(registry_path), rel_path))
            artifact_map[mid] = abs_target

        logger.info(f"Loaded {len(artifact_map)} artifacts from Registry.")
        return artifact_map

    except Exception as e:
        logger.error(f"Error loading registry: {e}")
        return {}


def get_relative_link(current_file_path: str, target_abs_path: str) -> str:
    """Calculates relative link from current_file to target_abs."""
    current_dir = os.path.dirname(current_file_path)
    try:
        rel_path = os.path.relpath(target_abs_path, current_dir)
        return rel_path.replace("\\", "/")
    except (ValueError, OSError):
        return ""


def forge_links(content: str, file_path: str, artifact_map: dict[str, str]) -> str:
    new_content = content

    for artifact_id, target_abs in artifact_map.items():
        # Avoid linking self
        if os.path.abspath(file_path) == target_abs:
            continue

        target_link = get_relative_link(file_path, target_abs)
        if not target_link:
            continue

        # Replacement Patterns

        # 1. Backticks: `ID`
        match_code = f"`{artifact_id}`"
        if match_code in new_content:
            pattern = re.compile(re.escape(match_code) + r"(?!\])")
            replacement = f"[`{artifact_id}`]({target_link})"
            new_content = pattern.sub(replacement, new_content)

        # 2. Table Cells: | ID |
        new_content = new_content.replace(f"| {artifact_id} |", f"| [{artifact_id}]({target_link}) |")

        # 3. Contextual (Greedy but safe-ish)
        new_content = new_content.replace(f"defined in {artifact_id}", f"defined in [{artifact_id}]({target_link})")
        new_content = new_content.replace(f"verified by {artifact_id}", f"verified by [{artifact_id}]({target_link})")
        new_content = new_content.replace(f"Laws of {artifact_id}", f"Laws of [{artifact_id}]({target_link})")
        new_content = new_content.replace(f"Authority: {artifact_id}", f"Authority: [{artifact_id}]({target_link})")
        new_content = new_content.replace(f"Authority | {artifact_id}", f"Authority | [{artifact_id}]({target_link})")

    return new_content


def scan_directory(root_dir: str, artifact_map: dict[str, str], registry_filename: str) -> None:
    logger.info(f"Forging links in: {root_dir}")
    for root, dirs, files in os.walk(root_dir):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file.endswith((".md", ".ts", ".tsx", ".py", ".json")):
                if file == registry_filename or file == "forge_backlinks.py":
                    continue

                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        original = f.read()

                    fixed = forge_links(original, path, artifact_map)

                    if fixed != original:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(fixed)
                        logger.info(f"Linked: {file}")
                except Exception as e:
                    logger.error(f"Error processing {file}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Forge Artifact Links")
    parser.add_argument("target_dir", help="Directory to scan")
    parser.add_argument("--registry", required=True, help="Path to UMB-OSLM-001 Registry file")
    args = parser.parse_args()

    artifact_map = load_artifact_map(args.registry)
    if not artifact_map:
        logger.error("Failed to load artifact map. Aborting.")
        return

    scan_directory(os.path.abspath(args.target_dir), artifact_map, os.path.basename(args.registry))


if __name__ == "__main__":
    main()
