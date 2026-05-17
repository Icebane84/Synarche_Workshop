"""
# TOOL-KNIG-003: The Ultimate Reforger (Knight of Swords)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-KNIG-003`                                          |
| **2. Official Name**   | `apply_standard.py`                                      |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Standardization**                                      |
| **11. Catalyst**       | **Compliance Enforcement**                               |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Knight of Swords persona uses this tool for alignment.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-KNIG-004, ORCHESTRATES, This tool is part of the Transmutation Pipeline.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Knight of Swords (Transmutation)
# Synergy Set: The Knight's Blade
# Primary Stat Buff: Strength (+15), Precision (+10)
# Passive Ability: The Razor's Edge (Markdown Enforcement)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE_STANDARD` | Apply OGLN v10/v11 Standards | Structural Alignment |
| `⚡ EXECUTE: PURIFY_MARKDOWN` | Fast Style Fix | Coherence Maintenance |

---

Ultimate Reforger: Applies Codex v10.0 and Axion governance standards to markdown artifacts.
Enforces: 12-point Header, AGP Block, Roman Numeral H2s, 4-space Indent, and Asterisk Lists.
"""

import argparse
import datetime
import os
import re

# --- CONSTANTS & CONFIGURATION ---

DEFAULT_DOMAIN = "GVRN"
ROMAN_NUMERALS = [
    "III.",
    "IV.",
    "V.",
    "VI.",
    "VII.",
    "VIII.",
    "IX.",
    "X.",
    "XI.",
    "XII.",
]

DOMAIN_REGISTRY: dict[str, str] = {
    "PHL": "Foundational Philosophy",
    "ARCH": "Technical Infrastructure",
    "GVRN": "Operational Governance",
    "CRTV": "Creative Synthesis",
    "LOGS": "Temporal Chronicle",
    "UEB": "Ethos / Universal Ethic",
    "DQB": "Dissonance Questboard",
}

# --- TEMPLATES (v11.0 Compliant) ---

HEADER_TEMPLATE = """# **{ARTIFACT_NAME} ({ARTIFACT_ID})**

## Genesis Stamp: {TIMESTAMP}** **Domain: {DOMAIN_PATH}**
**State: CANONIZED** **Tags: `{TAGS}`**
**Criticality: {CRITICALITY}**

---

## **{ARTIFACT_TYPE}**

### **[κ-veracity:verified] [κ-state:active] [κ-nexus:cornerstone]**

---

## **I. Universal Identification & Provenance**

| Field | Value |
| :---- | :---- |
| **1. Artifact ID** | `{ARTIFACT_ID}` |
| **2. Official Name** | `{ARTIFACT_FULL_NAME}` |
| **3. Version** | **v11.0** (**The Synarche Edition**) |
| **4. Provenance** | **Genesis Stamp**: {TIMESTAMP_SHORT} |
| **5. Domain** | `{DOMAIN_CODE}` ({DOMAIN_DESC}) |
| **6. Evolution** | **{ALIGNMENT}** |
| **7. Celestial Class** | `[STAR]` |
| **8. Tier** | **Operational** |
| **9. State** | `[ACTIVE]` |
| **10. Ethos** | **Guardian of Coherence** |
| **11. Catalyst** | **Reforge Command** |
| **12. Relations** | `LINK: OGLN.Core.Governance.Codex` |

---
"""

AGP_TEMPLATE = """
## **II. Axiomatic Governance & Purpose (AGP)**

---

### [2.1] State Vector

*   **Operational State:** `ACTIVE`
*   **Integrity Check:** `PASS`
*   **Alignment:** `{DOMAIN_CODE}`

### [2.2] Risk Governance

*   **Risk Level:** `LOW` (Standard Operation)
*   **Mitigation:** `Standard Protocol`

### [2.3] Linkage

*   **Upstream:** `[Define Upstream]`
*   **Downstream:** `[Define Downstream]`

### [2.4] Core Purpose

> **"The Essence of {ARTIFACT_NAME}"**
> [Define Purpose Here]

---
"""

PROMPT_PACKET_TEMPLATE = """
## **XI. Actionable Prompt Packet**

---

*   **Audit Command:** `CMD: LINT_ARTIFACT --target:"{ARTIFACT_ID}"`
*   **Refactor Command:** `CMD: APPLY_STANDARD --target:"{ARTIFACT_ID}"`
*   **Verification Command:** `CMD: VERIFY_COHERENCE --scope:DEEP --target:"{ARTIFACT_ID}"`

"""

# --- REFORGER ENGINE ---


class Reforger:
    """Core logic for artifact transmutation."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.artifact_id = os.path.splitext(self.filename)[0]
        self.lines: list[str] = []
        self._load_file()

    def _load_file(self) -> None:
        """Reads file content into memory."""
        if os.path.exists(self.filepath):
            with open(self.filepath, encoding="utf-8") as f:
                self.lines = f.readlines()

    def _get_metadata(self) -> dict[str, str]:
        """Derives metadata from filename and system state."""
        parts = self.artifact_id.split(".")
        domain_code = DEFAULT_DOMAIN

        if parts[0] == "OGLN" and len(parts) > 1:
            if "Governance" in parts[1]:
                domain_code = "GVRN"
            elif "Architecture" in parts[1]:
                domain_code = "ARCH"
            elif "Philosophy" in parts[1]:
                domain_code = "PHL"

        id_match = re.search(r"([A-Z]+)-([A-Z]+)-(\d+)", self.artifact_id)
        if id_match:
            domain_code = id_match.group(2) if id_match.group(2) in DOMAIN_REGISTRY else domain_code

        return {
            "TIMESTAMP": datetime.datetime.now().strftime("%B %d, %Y, %I:%M:%S %p (%Z)"),
            "TIMESTAMP_SHORT": datetime.datetime.now().strftime("%Y-%m-%d"),
            "DOMAIN_PATH": f"GVRN.{domain_code}.Phoenix",
            "DOMAIN_CODE": domain_code,
            "DOMAIN_DESC": DOMAIN_REGISTRY.get(domain_code, "General Governance"),
            "TAGS": f"Codex_v11, {domain_code}_Asset, Phoenix_Canon",
            "CRITICALITY": "Standard",
            "ARTIFACT_ID": self.artifact_id,
            "ARTIFACT_NAME": self.artifact_id.replace("-", " "),
            "ARTIFACT_FULL_NAME": self.filename,
            "ARTIFACT_TYPE": "BLUEPRINT" if "UMB" in self.artifact_id else "PROTOCOL",
            "ALIGNMENT": "Balanced Integration",
        }

    def apply_formatting(self) -> None:
        """Applies style rules: 4-space indent, asterisk lists."""
        new_lines = []
        for line in self.lines:
            if re.match(r"^ {2}[-*1]", line):
                line = "    " + line.lstrip()

            if re.match(r"^\s*-\s+", line):
                line = line.replace("- ", "* ", 1)

            line = line.rstrip() + "\n"
            new_lines.append(line)
        self.lines = new_lines

    def inject_structural_spine(self) -> None:
        """Injects mandatory sections (Header, AGP, Prompt Packet)."""
        content = "".join(self.lines)
        meta = self._get_metadata()

        if "Universal Identification & Provenance" not in content:
            header = HEADER_TEMPLATE.format(**meta)
            self.lines.insert(0, header)

        if "Axiomatic Governance & Purpose" not in content:
            agp = AGP_TEMPLATE.format(**meta)
            insert_idx = 0
            for i, line in enumerate(self.lines):
                if "| **12. Relations** |" in line:
                    insert_idx = i + 3
                    break
            self.lines.insert(insert_idx, agp)

        self._fix_roman_numerals()

        if "Actionable Prompt Packet" not in content:
            footer = PROMPT_PACKET_TEMPLATE.format(**meta)
            self.lines.append(footer)

    def _fix_roman_numerals(self) -> None:
        """Ensures H2 sections use sequential Roman Numerals starting from III."""
        h2_count = 0
        new_lines = []
        for line in self.lines:
            if line.startswith("## ") and not any(x in line for x in ["I. ", "II. ", "XI. "]):
                clean_header = re.sub(r"^##\s+([IVXLCDM]+\.)?\s*", "", line).strip()
                clean_header = clean_header.replace("**", "")
                if h2_count < len(ROMAN_NUMERALS):
                    new_lines.append(f"## **{ROMAN_NUMERALS[h2_count]} {clean_header}**\n")
                    new_lines.append("\n---\n")
                else:
                    new_lines.append(line)
                h2_count += 1
            else:
                new_lines.append(line)
        self.lines = new_lines

    def save(self) -> None:
        """Writes refactored content to disk."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            final_content = "".join(self.lines)
            final_content = re.sub(r"\n{3,}", "\n\n", final_content)
            f.write(final_content)


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(description="Apply Codex v11.0 and Axion standards to markdown.")
    parser.add_argument("--target", required=True, help="Path to the markdown file.")
    args = parser.parse_args()

    print(f"🔥 INITIATING REFORGE: {args.target}")
    reforger = Reforger(args.target)
    reforger.apply_formatting()
    reforger.inject_structural_spine()
    reforger.save()
    print(f"✅ REFORGE SUCCESSFUL: {args.target}")


if __name__ == "__main__":
    main()
