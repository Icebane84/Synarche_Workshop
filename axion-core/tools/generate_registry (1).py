"""# TOOL-HPRI-003: Registry Generator (The Master Librarian).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-003`                                          |
| **2. Official Name**   | `generate_registry.py`                                   |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `OSLM`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Cataloging**                                           |
| **11. Catalyst**       | **Registry Build**                                       |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for registry generation.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
UMB-OSLM-001, CREATES, This tool generates the Master Registry.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Priestess's Veil
# Primary Stat Buff: Intuition (+10), Retention (+15)
# Passive Ability: The Silver Thread (Relational Mapping)
# Cognitive Load Cost: Medium
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: GENERATE_OSLM` | Build Master Registry | Library Indexing |
| `⚡ EXECUTE: SYNC_GRIMOIRE` | Export OSLM to JSON | External Integration |
"""

import argparse
import json
import logging
import os
import re
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

MIN_UIP_PARTS = 3

# Key Aliases for different generations of OGLN/Phoenix
KEY_MAP = {
    "Artifact ID": "Module ID",
    "Module ID": "Module ID",
    "Version": "Version",
    "Status": "Status",
    "Type": "Type",
    "Celestial Class": "Classification",
    "Classification": "Classification",
    "Evolution": "Evolution",
    "Dependency-Hash": "Dependencies",
    "Dependencies": "Dependencies",
    "Upstream": "Dependencies",
    "Downstream": "Downstream",
    "Governance": "Governance",
    "Integrity Hash": "Integrity Hash",
}


def _extract_title(content: str) -> str:
    """Finds the first H1 that is NOT UIP related."""
    h1_matches = re.finditer(r"^#\s+(.+)$", content, re.MULTILINE)
    for match in h1_matches:
        candidate = match.group(1).replace("*", "").strip()
        if (
            "Universal Identification & Provenance" not in candidate
            and "UIP" not in candidate
        ):
            return candidate
    return "Unknown"


def _parse_uip_metadata(content: str, uip: dict[str, str]) -> None:
    """Parses the UIP Table and maps keys to the uip dict."""
    lines = content.split("\n")
    in_uip = False
    for line in lines:
        # Check for UIP header (any header level or plain text)
        if (
            "Universal Identification & Provenance" in line
            or "The Vector Signature" in line
        ):
            in_uip = True
            continue

        if in_uip and line.strip().startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= MIN_UIP_PARTS:
                # Key cleaning: remove numbers, stars, backticks
                raw_key = parts[1].replace("*", "").replace("`", "").strip()
                # Remove leading numbers like "1. "
                clean_key = re.sub(r"^\d+\.\s*", "", raw_key)

                val = parts[2].replace("`", "").replace("*", "").strip()

                # Dynamic mapping
                if clean_key in KEY_MAP:
                    mapped_key = KEY_MAP[clean_key]
                    if mapped_key == "Dependencies":
                        # Standardize: remove brackets
                        val = val.replace("[", "").replace("]", "").strip()
                    uip[mapped_key] = val

        # Stop at horizontal rule or next major section if we have the ID
        if (
            in_uip
            and (line.strip() == "---" or line.startswith("##"))
            and uip["Module ID"] != "Unknown"
        ):
            break


def parse_uip(filepath: str) -> dict[str, str]:
    """Extracts UIP data from a file with enhanced flexibility for legacy formats."""
    uip: dict[str, str] = {
        "Module ID": "Unknown",
        "Version": "Unknown",
        "Classification": "Unknown",
        "Status": "Unknown",
        "Type": "Unknown",
        "Title": "Unknown",
        "Dependencies": "None",
    }

    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        logger.exception(f"Error reading {filepath}")
        return uip

    uip["Title"] = _extract_title(content)
    _parse_uip_metadata(content, uip)

    return uip


def render_table(items: list[dict[str, str]]) -> str:
    """Helper to render markdown table."""
    s = ""
    for item in sorted(items, key=lambda x: x["Module ID"]):
        deps = item.get("Dependencies", "None")
        if deps == "Unknown":
            deps = "None"
        s += f"| `{item['Module ID']}` | [{item['Title']}]({item['RelPath']}) | `{item['Version']}` | `{item['Status']}` | `{deps}` |\n"
    return s


def _get_registry_header(timestamp: str) -> str:
    """Returns the standardized registry header."""
    return f"""---
# Universal Identification & Provenance (UIP)
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `UMB-OSLM-001` |
| **Official Name** | `Master Artifact Registry` |
| **Version** | `v11.0` |
| **Domain** | `OSLM` |
| **Evolution** | **Cognitive Ascension** |
| **Signal (ESF)** | `ESF-STAR` |
| **Status (State)** | `ACTIVE` |
| **Tier** | **Strategic** |
| **Celestial Class** | `[STAR]` |
| **Integrity Hash** | `REGENERATED` |
| **Provenance** | `Genesis Stamp: 2025-10-01` |
| **Updated** | `{timestamp}` |
| **Relations** | `Governed by GVRN-SYNERGY-001` |
---

# Master Artifact Registry (The Library)

**Genesis Stamp**: {timestamp} | **Domain**: PHOENIX | **State**: ACTIVE

> [!NOTE]
> This document is the "Immutable Chronicle" of the Phoenix Protocol. It lists every legally recognized artifact within the system.

"""


def generate_markdown(artifacts: list[dict[str, str]]) -> str:
    """Generates the UMB-OSLM-001 content."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    md = _get_registry_header(timestamp)

    # Categorize
    categories = {
        cat: [] for cat in ["Core", "Protocol", "Manual", "Plan", "Log", "Other"]
    }

    for a in artifacts:
        if a["Type"] == "Unknown":
            _apply_type_heuristics(a)

        t = a["Type"]
        if t in categories:
            categories[t].append(a)
        else:
            categories["Other"].append(a)

    # Render Sections
    md += "## I. The Core (Star Class)\n\n"
    md += "| Module ID | Title | Version | Status | Dependencies |\n| :--- | :--- | :--- | :--- | :--- |\n"
    md += render_table(categories["Core"])

    section_map = [
        ("II. Protocols (Moon Class)", "Protocol"),
        ("III. Operations Manuals (Planet Class)", "Manual"),
        ("IV. Strategic Plans", "Plan"),
        ("V. Experience Logs", "Log"),
    ]

    for title, key in section_map:
        md += f"\n## {title}\n\n"
        md += "| Module ID | Title | Version | Status | Dependencies |\n| :--- | :--- | :--- | :--- | :--- |\n"
        md += render_table(categories[key])

    if categories["Other"]:
        md += "\n## VI. Unclassified / Reference\n\n"
        md += "| Module ID | Title | Version | Status | Dependencies |\n| :--- | :--- | :--- | :--- | :--- |\n"
        md += render_table(categories["Other"])

    md += """
---

## VII. Actionable Prompt Packet

### Packet A: Standard Compliance Check

> "Acting as the Protocol Auditor, review this document against the Phoenix Codex v11.0. Does it adhere to the Luminous Coherence standard?"

### Packet B: Operational Activation

> "Simulate the execution of this protocol. What are the immediate output artifacts?"

---
"""
    return md


def _apply_type_heuristics(a: dict[str, str]) -> None:
    """Guesses type based on filename or title."""
    f = a["Filename"]
    if "CORE" in f or "CODEX" in f:
        a["Type"] = "Core"
    elif "AOP" in f or "Protocol" in a["Title"]:
        a["Type"] = "Protocol"
    elif "MAN" in f or "Manual" in a["Title"]:
        a["Type"] = "Manual"
    elif "PLAN" in f:
        a["Type"] = "Plan"
    elif "LOG" in f:
        a["Type"] = "Log"
    elif "REF" in f:
        a["Type"] = "Other"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Master Artifact Registry")
    parser.add_argument("target_dir", help="Directory to scan for artifacts")
    parser.add_argument("--output", help="Path to save the registry")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target_dir)
    output_file = (
        args.output
        if args.output
        else os.path.join(target_dir, "UMB-OSLM-001_MasterArtifactRegistry_v11.0.md")
    )

    logger.info(f"Generating Master Artifact Registry for: {target_dir}")
    artifacts: list[dict[str, str]] = []

    for root, dirs, files in os.walk(target_dir):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")

        for f in files:
            if not f.endswith(".md") or "UMB-OSLM-001" in f:
                continue

            path = os.path.join(root, f)
            data = parse_uip(path)

            # Map RelPath for registry
            rel_path = os.path.relpath(path, os.path.dirname(output_file))
            data["RelPath"] = rel_path.replace("\\", "/")
            data["Filename"] = f

            # Assign ID from Filename if parse failed
            if data["Module ID"] == "Unknown":
                id_match = re.search(r"([A-Z]+-[A-Z]+-\d+)", f)
                if id_match:
                    data["Module ID"] = id_match.group(1)

            artifacts.append(data)
            logger.info(f"Index: {data['Module ID']} - {data['Title']}")

    if output_file.endswith(".json"):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(artifacts, f, indent=4)
    else:
        content = generate_markdown(artifacts)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

    logger.info(f"\nRegistry written to: {output_file}")


if __name__ == "__main__":
    main()
