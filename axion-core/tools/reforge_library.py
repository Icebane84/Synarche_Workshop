"""
# TOOL-EMPR-001: The Pattern Reforger (Emperor's Schema)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPR-001`                                          |
| **2. Official Name**   | `reforge_library.py`                                     |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Standardization**                                      |
| **11. Catalyst**       | **Schema Validation**                                    |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Emperor persona uses this tool for schema enforcement.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Schema Forge (The Emperor)
# Synergy Set: The Imperial Standard
# Primary Stat Buff: Authority (+10), Order (+15)
# Passive Ability: The Architect's Grid (Standardization)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE_MD` | Bulk Reforge Markdown | Standardize Formatting |
| `⚡ EXECUTE: SCAN_FORGE` | Scan & Fix All | Zero Entropy State |
"""

import argparse
import logging
import os
import re
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# v11.0 Standard UIP Template
UIP_TEMPLATE = """## I. Universal Identification & Provenance
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `{mid}` |
| **Official Name** | `{filename}` |
| **Version** | **v11.0** |
| **Domain** | `{domain}` |
| **Evolution** | **{evolution}** |
| **Signal (ESF)** | `ESF-ALPHA` |
| **Status (State)** | `[ACTIVE]` |
| **Tier** | **Operational** |
| **Celestial Class** | `{classification}` |
| **Governance** | `GVRN-SYNERGY-001` |
| **Upstream** | `N/A` |
| **Downstream** | `N/A` |
| **Integrity Hash** | `N/A` |
| **Provenance** | `Genesis Stamp: {timestamp}` |
| **Relations** | `Governed by GVRN-SYNERGY-001` |
"""

APP_TEMPLATE = """
---

## VII. Actionable Prompt Packet

### Packet A: Standard Compliance Check

> "Acting as the Protocol Auditor, review this document against the Phoenix Codex v11.0. Does it adhere to the Luminous Coherence standard?"

### Packet B: Operational Activation

> "Simulate the execution of this protocol. What are the immediate output artifacts?"

---
"""


class Reforger:
    def __init__(self, target_dir: str) -> None:
        self.target_dir = os.path.abspath(target_dir)
        self.timestamp = datetime.now().strftime("%Y-%m-%d")

    def extract_metadata(self, content: str, filename: str) -> dict[str, str]:
        """Tries to find existing metadata or infer it."""
        meta = {
            "mid": "Unknown",
            "evolution": "Cognitive Ascension",
            "type": "Protocol",
            "classification": "Moon",
            "tags": "Reforged, v11.0",
            "title": "Untitled Artifact",
        }

        # Infer MID from filename - handle multiple segments
        mid_match = re.search(r"([A-Z0-9]+(?:-[A-Z0-9]+)+)", filename)
        if mid_match:
            meta["mid"] = mid_match.group(1)

        # Try to find existing ID in content
        id_match = re.search(r"\|\s+\*\*(?:Artifact|Module) ID\*\*\s+\|\s+`?([^`\n|]+)`?", content, re.IGNORECASE)
        if id_match:
            meta["mid"] = id_match.group(1).strip()

        # Try to find Evolution
        evo_match = re.search(r"\|\s+\*\*Evolution\*\*\s+\|\s+\*\*?([^*|\n]+)\*\*?", content)
        if evo_match:
            meta["evolution"] = evo_match.group(1).strip()

        # Try to find Title from first H1
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
            # Clean title: remove bolding, parentheticals, and OGLN prefixes
            title = re.sub(r"\*\*|\*", "", title)
            title = re.sub(r"\(v\d+\.\d+\)", "", title, flags=re.IGNORECASE)
            title = re.sub(r"^OGLN\.", "", title, flags=re.IGNORECASE)
            meta["title"] = title.strip()

        return meta

    def reforge_content(self, content: str, meta: dict[str, str], filename: str) -> str:
        # 1. Remove old UIP if it exists
        new_content = re.sub(
            r"---.*?# Universal Identification & Provenance.*?---", "", content, flags=re.DOTALL | re.IGNORECASE
        )
        new_content = re.sub(r"---.*?The Vector Signature.*?---", "", new_content, flags=re.DOTALL | re.IGNORECASE)
        # Also remove the "Artifact Start" legacy markers
        new_content = re.sub(r"######\s+\[ARTIFACT (START|END)\]", "", new_content)

        # 2. Fix H1 Singularity
        # Find all H1s
        h1s = re.findall(r"^#\s+.*$", new_content, re.MULTILINE)
        if h1s:
            # Keep the first H1 as the main title (after UIP)
            # Demote all subsequent H1s to H2
            def demote(match: re.Match) -> str:
                if not hasattr(demote, "count"):
                    demote.count = 0
                demote.count += 1
                if demote.count == 1:
                    return match.group(0)
                return "##" + match.group(0)[1:]

            new_content = re.sub(r"^#\s+.*$", demote, new_content, flags=re.MULTILINE)
            delattr(demote, "count")
        else:
            # If no H1 found, prepend the title from meta
            new_content = f"# {meta['title']}\n\n" + new_content

        # 3. Normalize Indentation (4 spaces to 2 spaces)
        new_content = re.sub(r"^    - ", "  - ", new_content, flags=re.MULTILINE)
        new_content = re.sub(r"^        - ", "    - ", new_content, flags=re.MULTILINE)

        # 4. Inject v11.0 UIP
        uip = UIP_TEMPLATE.format(
            mid=meta["mid"],
            filename=filename,  # Use passed filename
            domain=meta.get("domain", "ARCH"),
            evolution=meta["evolution"],
            classification=meta["classification"],
            timestamp=self.timestamp,
        )

        new_content = uip + "\n" + new_content.strip()

        # 5. Ensure APP
        if "Actionable Prompt Packet" not in new_content and "CMD:" not in new_content:
            new_content = new_content.rstrip() + APP_TEMPLATE

        return new_content

    def reforge_file(self, filepath: str) -> None:
        filename = os.path.basename(filepath)
        logger.info(f"Reforging: {filename}")

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            meta = self.extract_metadata(content, filename)
            reforged = self.reforge_content(content, meta, filename)

            # Sanity check: ensure single title H1
            # (Sometimes demote produces double # # due to regex)
            reforged = reforged.replace("# #", "##")

            # Write back
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(reforged)

            # Rename to strict RNC pattern if needed
            # [PREFIX]-[ID]_[Name]_v11.0.md
            clean_title = "".join(x for x in meta["title"] if x.isalnum() or x in " -_").strip()
            clean_title = clean_title.replace(" ", "")
            new_filename = f"{meta['mid']}_{clean_title}_v11.0.md"

            new_path = os.path.join(os.path.dirname(filepath), new_filename)
            if filepath != new_path:
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(filepath, new_path)
                logger.info(f"  -> Renamed: {new_filename}")

        except Exception:
            logger.exception(f"Error reforging {filename}")

    def run(self, files: list[str]) -> None:
        for f in files:
            self.reforge_file(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phoenix Protocol Artifact Reforger")
    parser.add_argument("target_dir", help="Directory or file to reforge")
    parser.add_argument("--batch", help="Path to a text file containing list of files to reforge")
    args = parser.parse_args()

    reforger = Reforger(os.path.dirname(args.target_dir) if os.path.isfile(args.target_dir) else args.target_dir)

    if os.path.isfile(args.target_dir):
        reforger.run([args.target_dir])
    elif args.batch:
        with open(args.batch) as f:
            batch_files = [line.strip() for line in f if line.strip()]
        reforger.run(batch_files)
    else:
        logger.error("Please specify a file or use --batch.")


if __name__ == "__main__":
    main()
