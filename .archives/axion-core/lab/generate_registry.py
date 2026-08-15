"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-003`                                |
| **2. Official Name**   | `generate_registry.py`                          |
| **3. Version**         | **v14.0**                                      |
| **4. Provenance**      | **Reforged: 2026-03-01**                       |
| **5. Domain**          | `GVRN` (Registry)                              |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Master Librarian**                       |
| **11. Catalyst**       | **System Pulse v14.0**                         |
| **12. Relations**      | `INDEXES: ALL_ARTIFACTS`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CORE-CODEX-001 | GOVERNS | This tool follows the Supreme Law. |
| GVRN.REG.ArtifactInventory | REGENERATES | This tool maintains the Master Registry. |

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
TABLE_HEADER = (
    "| Module ID | Title | Version | Status |\n| :--- | :--- | :--- | :--- |\n"
)

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


class ArtifactParser:
    """Parses a single artifact file to extract UIP metadata."""

    def _extract_title(self, content: str) -> str:
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

    def _process_uip_row(self, line: str, uip: dict[str, str]) -> None:
        """Processes a single row of the UIP table."""
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < MIN_UIP_PARTS:
            return

        raw_key = re.sub(r"^\d+\.\s*", "", parts[1].replace("*", "").replace("`", "").strip())
        val = parts[2].replace("`", "").replace("*", "").strip()

        if raw_key in KEY_MAP:
            mapped_key = KEY_MAP[raw_key]
            if mapped_key == "Dependencies":
                val = val.replace("[", "").replace("]", "").strip()
            uip[mapped_key] = val

    def _parse_uip_metadata(self, content: str, uip: dict[str, str]) -> None:
        """Parses the UIP Table and maps keys to the uip dict."""
        lines = content.split("\n")
        in_uip = False
        for line in lines:
            if "Universal Identification & Provenance" in line or "The Vector Signature" in line:
                in_uip = True
                continue

            if in_uip and line.strip().startswith("|"):
                self._process_uip_row(line, uip)

            if in_uip and (line.strip() == "---" or line.startswith("##")) and uip.get(KEY_MODULE_ID) != "Unknown":
                break

    def parse_file(self, filepath: str) -> dict[str, str]:
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

        uip["Title"] = self._extract_title(content)
        self._parse_uip_metadata(content, uip)

        return uip


class ArtifactCategorizer:
    """Categorizes artifacts based on type and heuristics."""

    CATEGORIES = ["Core", "Protocol", "Manual", "Plan", "Log", "Other"]

    def _apply_type_heuristics(self, artifact: dict[str, str]) -> None:
        """Guesses type based on filename or title."""
        filename = artifact.get("Filename", "")
        title = artifact.get("Title", "")
        if "CORE" in filename or "CODEX" in filename:
            artifact["Type"] = "Core"
        elif "AOP" in filename or "Protocol" in title or "UMB" in filename:
            artifact["Type"] = "Protocol"
        elif "PLAN" in filename:
            artifact["Type"] = "Plan"
        elif "LOG" in filename or "CSL" in filename:
            artifact["Type"] = "Log"
        elif "REF" in filename or "Manual" in title:
            artifact["Type"] = "Manual"

    def categorize(self, artifacts: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
        """Categorizes a list of artifacts."""
        categories: dict[str, list[dict[str, str]]] = {cat: [] for cat in self.CATEGORIES}

        for artifact in artifacts:
            if artifact.get("Type") == "Unknown":
                self._apply_type_heuristics(artifact)

            artifact_type = artifact.get("Type", "Other")
            if artifact_type in categories:
                categories[artifact_type].append(artifact)
            else:
                categories["Other"].append(artifact)
        return categories


class MarkdownRenderer:
    """Renders categorized artifacts into a Markdown registry file."""

    def _get_registry_header(self, timestamp: str) -> str:
        """Returns the standardized registry header."""
        return f"""# GVRN.REG.ArtifactInventory: Master Artifact Inventory (v14.0)

## Genesis Stamp: {timestamp} | Domain: GVRN | State: [ACTIVE] | Criticality: Star

---

### I. Universal Identification & Provenance (The Vector Signature)

| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `GVRN.REG.ArtifactInventory`                   |
| **2. Official Name**   | `GVRN.REG.ArtifactInventory.md`                |
| **3. Version**         | **v14.0 [OMEGA]**                              |
| **4. Provenance**      | **Regenerated: {timestamp}**                   |
| **5. Domain**          | `GVRN` (Master Index)                          |
| **6. Evolution**       | **Crystalline Coherence**                      |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Infinite Library**                       |
| **11. Catalyst**       | **System Pulse**                               |
| **12. Relations**      | `GOVERNED_BY: [CORE-CODEX-001]`                |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |

---

### **II. The Synergy Vector (Relational Dynamics)**

| Relation Type | Target ID | Synergy Description |
| :--- | :--- | :--- |
| GOVERNED_BY | CORE-CODEX-001 | Compliance with overall system architecture. |
| ORCHESTRATES | ALL_ARTIFACTS | Links every node into the master cognitive weave. |

---
"""

    def _render_table(self, items: list[dict[str, str]]) -> str:
        """Helper to render a markdown table for a category."""
        rows = [
            f"| `{item[KEY_MODULE_ID]}` | [{item['Title']}]({item['RelPath']}) | `{item['Version']}` | `{item['Status']}` |"
            for item in sorted(items, key=lambda x: x[KEY_MODULE_ID])
        ]
        return "\n".join(rows) + "\n" if rows else ""

    def render(self, categories: dict[str, list[dict[str, str]]]) -> str:
        """Generates the full Markdown content."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        md_content = self._get_registry_header(timestamp)

        # Render Core section
        md_content += "## III. The Core (Star Class)\n\n"
        md_content += TABLE_HEADER
        md_content += self._render_table(categories["Core"])

        # Render other sections
        section_map = [
            ("IV. Protocols & Blueprints (Planet & Moon Class)", "Protocol"),
            ("V. Experience Logs & Archives", "Log"),
            ("VI. Strategic Plans", "Plan"),
        ]

        for title, key in section_map:
            if categories[key]:
                md_content += f"\n## {title}\n\n"
                md_content += TABLE_HEADER
                md_content += self._render_table(categories[key])

        # Render Other/Manuals section
        other_and_manuals = categories["Manual"] + categories["Other"]
        if other_and_manuals:
            md_content += "\n## VII. Operations Manuals & Reference\n\n"
            md_content += TABLE_HEADER
            md_content += self._render_table(other_and_manuals)

        md_content += """
---

## VII. Actionable Prompt Packet

### Packet A: Standard Compliance Check

> "Acting as the Protocol Auditor, review this document against the Phoenix Codex v11.0. Does it adhere to the Luminous Coherence standard?"

### Packet B: Operational Activation

> "Simulate the execution of this protocol. What are the immediate output artifacts?"

---
"""
        return md_content


class ArtifactScanner:
    """Scans a directory for artifacts and uses a parser to extract data."""

    def __init__(self, parser: ArtifactParser, target_dir: str, output_dir: str):
        self.parser = parser
        self.target_dir = target_dir
        self.output_dir = output_dir

    def scan(self) -> list[dict[str, str]]:
        """Scans the target directory for artifacts and parses them."""
        artifacts: list[dict[str, str]] = []
        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in ("node_modules", ".git")]

            for f in files:
                if not f.endswith(".md") or "GVRN.REG.ArtifactInventory" in f:
                    continue

                path = os.path.join(root, f)
                data = self.parser.parse_file(path)

                rel_path = os.path.relpath(path, self.output_dir)
                data["RelPath"] = rel_path.replace("\\", "/")
                data["Filename"] = f

                if data[KEY_MODULE_ID] == "Unknown":
                    id_match = re.search(r"([A-Z]+-[A-Z]+-\d+)", f)
                    if id_match:
                        data[KEY_MODULE_ID] = id_match.group(1)

                artifacts.append(data)
                logger.info(f"Index: {data[KEY_MODULE_ID]} - {data['Title']}")
        return artifacts


class RegistryGenerator:
    """Orchestrates the generation of the artifact registry."""

    def __init__(self, target_dir: str, output_file: str):
        self.target_dir = target_dir
        self.output_file = output_file
        self.output_dir = os.path.dirname(output_file)

    def generate(self) -> None:
        """Executes the full registry generation pipeline."""
        logger.info(f"Generating Master Artifact Registry for: {self.target_dir}")

        parser = ArtifactParser()
        scanner = ArtifactScanner(parser, self.target_dir, self.output_dir)
        artifacts = scanner.scan()

        if self.output_file.endswith(".json"):
            self._save_json(artifacts)
        else:
            self._save_markdown(artifacts)

        logger.info(f"\nRegistry written to: {self.output_file}")

    def _save_json(self, artifacts: list[dict[str, str]]) -> None:
        """Saves the registry as a JSON file."""
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(artifacts, f, indent=4)

    def _save_markdown(self, artifacts: list[dict[str, str]]) -> None:
        """Saves the registry as a Markdown file."""
        categorizer = ArtifactCategorizer()
        categories = categorizer.categorize(artifacts)

        renderer = MarkdownRenderer()
        content = renderer.render(categories)

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(content)


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
    if args.output:
        output_file = os.path.abspath(args.output)
    else:
        output_file = os.path.join(target_dir, "01_Registries", "GVRN.REG.ArtifactInventory.md")

    generator = RegistryGenerator(target_dir, output_file)
    generator.generate()


if __name__ == "__main__":
    main()
