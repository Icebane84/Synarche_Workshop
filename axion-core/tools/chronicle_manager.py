"""# TOOL-KING-001: The King's Chronicle (Global Archival).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-KING-001`                                          |
| **2. Official Name**   | `chronicle_manager.py`                                   |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Archival Integrity**                                   |
| **11. Catalyst**       | **Log Refining**                                         |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The King of Pentacles persona uses this tool for archival.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
UMB-RULES-001, COMPLIES_WITH, Ensures logs adhere to global rules.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Global Archival (The King of Pentacles)
# Synergy Set: The King's Ledger
# Primary Stat Buff: Wisdom (+15), Integrity (+10)
# Passive Ability: The Master's Vault (Structure Enforcement)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFINE_CHRONICLE` | Parse & Restructure Logs | Archival Integrity |
| `⚡ EXECUTE: SEAL_LEDGER` | Finalize Master Outline | Immutable Record |
"""

import argparse
import logging
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class ChronicleManager:
    """The King of Pentacles: Master of Records and Structural Integrity."""

    def __init__(self) -> None:
        self.chapter_pattern = re.compile(r"^Chapter (\d+):", re.IGNORECASE)
        self.ignore_patterns = [
            r"Step Id: \d+",
            r"\[\d{2}:\d{2}:\d{2}\]",
            r"CMD:",
            r"Simulated Execution",
            r"Initiating Phase",
            r"^User:",
            r"^Model:",
            r"Command Invocation",
        ]

    def _clean_line(self, line: str) -> str | None:
        """Cleans artifacts and noise from a line."""
        for pattern in self.ignore_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return None

        # HTML Header Fix (Manual Replacement)
        if "<h3>" in line:
            line = line.replace("<h3>", "### ").replace("</h3>", "")
        if "<h2>" in line:
            line = line.replace("<h2>", "## ").replace("</h2>", "")
        if "<h1>" in line:
            line = line.replace("<h1>", "# ").replace("</h1>", "")

        return line.rstrip()

    def parse_log(self, filepath: str) -> dict:
        """Parses a raw log into structured sections."""
        sections: dict = {
            "synopsis": [],
            "lore": [],
            "chapters": {},
            "profiles": [],
            "appendix": [],
            "uncategorized": [],
        }

        current_section = "uncategorized"
        current_chapter_num = 0

        try:
            with open(filepath, encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            logger.exception(f"[!] Read failed: {filepath}")
            return sections

        for line in lines:
            cleaned = self._clean_line(line)
            if cleaned is None:
                continue

            # Chapter Detection
            chap_match = self.chapter_pattern.match(cleaned.strip())
            if chap_match:
                current_chapter_num = int(chap_match.group(1))
                current_section = "chapters"
                if current_chapter_num not in sections["chapters"]:
                    sections["chapters"][current_chapter_num] = []
                sections["chapters"][current_chapter_num].append(cleaned)
                continue

            # Section Triggers (Non-Chapter)
            if "CONSOLIDATED LORE" in cleaned.upper():
                current_section = "lore"
            elif any(x in cleaned for x in ["Synopsis", "Title:"]):
                current_section = "synopsis"
            elif any(x in cleaned for x in ["Character Dynamics", "Definitive Guide"]):
                current_section = "profiles"
            elif (
                "MIMIR'S WELL" in cleaned.upper()
                or "EXPERIENTIAL MEMORY" in cleaned.upper()
            ):
                current_section = "well"
            elif (
                "PORTFOLIO ANALYSIS" in cleaned.upper()
                or "METRIC WEIGHTING" in cleaned.upper()
            ):
                current_section = "metrics"
            elif any(x in cleaned for x in ["Development Prompts", "Appendix"]):
                current_section = "appendix"

            # Append to current
            if current_section == "chapters":
                if current_chapter_num > 0:
                    sections["chapters"][current_chapter_num].append(cleaned)
                else:
                    sections["synopsis"].append(cleaned)
            else:
                if current_section not in sections:
                    sections[current_section] = []  # Safety init
                sections[current_section].append(cleaned)

        return sections

    def generate_outline(self, sections: dict) -> str:
        """Generates a refined Markdown outline."""
        output = ["# Master Outline: Refined Ledger\n"]

        if sections["synopsis"]:
            output.append("## I. Synopsis\n")
            output.extend(sections["synopsis"])
            output.append("\n")

        if sections["lore"]:
            output.append("## II. World Lore & Rules\n")
            output.extend(sections["lore"])
            output.append("\n")

        if sections["profiles"]:
            output.append("## III. Character Dynamics\n")
            output.extend(sections["profiles"])
            output.append("\n")

        if sections["chapters"]:
            output.append("## IV. Narrative Outline\n")
            for num in sorted(sections["chapters"].keys()):
                output.append(f"### Chapter {num}\n")
                for line in sections["chapters"][num]:
                    if not self.chapter_pattern.match(line.strip()):
                        output.append(line)
                output.append("\n")

        if sections.get("well"):
            output.append("## IV. Mimir's Well (Experiential Memory)\n")
            output.extend(sections["well"])
            output.append("\n")

        if sections.get("metrics"):
            output.append("## V. Portfolio Metrics (DMPM)\n")
            output.extend(sections["metrics"])
            output.append("\n")

        if sections["appendix"]:
            output.append("## VI. Appendix\n")
            output.extend(sections["appendix"])

        return "\n".join(output)

    def process_file(self, input_path: str, output_path: str) -> None:
        """Standard refinement workflow."""
        logger.info(f"[📖] Parsing Chronicle: {input_path}")
        sections = self.parse_log(input_path)
        refined = self.generate_outline(sections)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(refined)
        logger.info(f"[📜] Ledger Sealed: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="The King's Chronicle: Mastering the Archival Ledger."
    )
    parser.add_argument("input", help="Source log/markdown file.")
    parser.add_argument("--output", help="Destination for refined outline.")
    args = parser.parse_args()

    output = args.output or args.input.replace(".md", "_Refined.md")
    manager = ChronicleManager()
    manager.process_file(args.input, output)


if __name__ == "__main__":
    main()
