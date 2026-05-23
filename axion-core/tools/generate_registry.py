"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-003`                                |
| **2. Official Name**   | `generate_registry.py`                          |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `OSLM` (Registry)                              |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Master Librarian**                       |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `INDEXES: ALL_ARTIFACTS`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CORE-CODEX-001 | GOVERNS | This tool follows the Supreme Law. |
| UMB-OSLM-001 | REGENERATES | This tool maintains the Master Registry. |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Librarian's Index
# Primary Stat Buff: Intuition (+15), Retention (+20)
# Passive Ability: The Silver Thread (Relational Mapping)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

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
KEY_MODULE_ID = "Module ID"
TABLE_HEADER = "| Module ID | Title | Version | Status | Dependencies |\n| :--- | :--- | :--- | :--- | :--- |\n"

# Key Aliases for different generations of OGLN/Phoenix
KEY_MAP = {
    "Artifact ID": KEY_MODULE_ID,
    "Module ID": KEY_MODULE_ID,
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


def _process_uip_row(line: str, uip: dict[str, str]) -> None:
    """Processes a single row of the UIP table."""
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < MIN_UIP_PARTS:
        return

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
            _process_uip_row(line, uip)

        # Stop at horizontal rule or next major section if we have the ID
        if (
            in_uip
            and (line.strip() == "---" or line.startswith("##"))
            and uip[KEY_MODULE_ID] != "Unknown"
        ):
            break


def parse_uip(filepath: str) -> dict[str, str]:
    """Extracts UIP data from a file with enhanced flexibility for legacy formats."""
    uip: dict[str, str] = {
        KEY_MODULE_ID: "Unknown",
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
    for item in sorted(items, key=lambda x: x[KEY_MODULE_ID]):
        deps = item.get("Dependencies", "None")
        if deps == "Unknown":
            deps = "None"
        s += f"| `{item[KEY_MODULE_ID]}` | [{item['Title']}]({item['RelPath']}) | `{item['Version']}` | `{item['Status']}` | `{deps}` |\n"
    return s


def _get_registry_header(timestamp: str) -> str:
    """Returns the standardized registry header (v13.0)."""
    return f"""# UMB-OSLM-001: Master Artifact Registry (v13.0)

## Genesis Stamp: {timestamp} | Domain: OSLM | State: [ACTIVE] | Criticality: High

---

### I. Universal Identification & Provenance (The Vector Signature)

| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `UMB-OSLM-001`                                 |
| **2. Official Name**   | `Master Artifact Registry`                     |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Regenerated: {timestamp}**                   |
| **5. Domain**          | `OSLM` (Master Index)                          |
| **6. Evolution**       | **Crystalline Coherence**                      |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Strategic**                                  |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Infinite Library**                       |
| **11. Catalyst**       | **System Pulse**                               |
| **12. Relations**      | `GOVERNED_BY: [CORE-CODEX-001]`                |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> This document is the "Immutable Chronicle" of the Phoenix Protocol. It lists every legally recognized artifact within the system.

---
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
    md += TABLE_HEADER
    md += render_table(categories["Core"])

    section_map = [
        ("II. Protocols (Moon Class)", "Protocol"),
        ("III. Operations Manuals (Planet Class)", "Manual"),
        ("IV. Strategic Plans", "Plan"),
        ("V. Experience Logs", "Log"),
    ]

    for title, key in section_map:
        md += f"\n## {title}\n\n"
        md += TABLE_HEADER
        md += render_table(categories[key])

    if categories["Other"]:
        md += "\n## VI. Unclassified / Reference\n\n"
        md += TABLE_HEADER
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


def scan_artifacts(target_dir: str, output_file_dir: str) -> list[dict[str, str]]:
    """Scans the target directory for artifacts and parses them."""
    artifacts: list[dict[str, str]] = []

    for root, dirs, files in os.walk(target_dir):
        # Filter directories in place
        dirs[:] = [d for d in dirs if d not in ("node_modules", ".git")]

        for f in files:
            if not f.endswith(".md") or "UMB-OSLM-001" in f:
                continue

            path = os.path.join(root, f)
            data = parse_uip(path)

            # Map RelPath for registry
            rel_path = os.path.relpath(path, output_file_dir)
            data["RelPath"] = rel_path.replace("\\", "/")
            data["Filename"] = f

            # Assign ID from Filename if parse failed
            if data[KEY_MODULE_ID] == "Unknown":
                id_match = re.search(r"([A-Z]+-[A-Z]+-\d+)", f)
                if id_match:
                    data[KEY_MODULE_ID] = id_match.group(1)

            artifacts.append(data)
            logger.info(f"Index: {data[KEY_MODULE_ID]} - {data['Title']}")

    return artifacts


def save_registry(artifacts: list[dict[str, str]], output_file: str) -> None:
    """Saves the registry to the specified output file."""
    if output_file.endswith(".json"):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(artifacts, f, indent=4)
    else:
        content = generate_markdown(artifacts)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

    logger.info(f"\nRegistry written to: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=">>> [HPRI] Registry Generator v13.0 (The Master Librarian)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example:\n  python generate_registry.py _governance --output UMB-OSLM-001.md",
    )
    parser.add_argument(
        "target_dir", help="Directory to scan for artifacts (e.g., '_governance')"
    )
    parser.add_argument("--output", help="Path to save the registry (Markdown or JSON)")
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target_dir)
    output_file = (
        args.output
        if args.output
        else os.path.join(target_dir, "UMB-OSLM-001_MasterArtifactRegistry_v11.0.md")
    )

    logger.info(f"Generating Master Artifact Registry for: {target_dir}")

    artifacts = scan_artifacts(target_dir, os.path.dirname(output_file))
    save_registry(artifacts, output_file)


if __name__ == "__main__":
    main()
