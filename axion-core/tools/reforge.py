"""
# TOOL-KNIG-001: The Reforger CLI (The Knight's Blade)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-KNIG-001`                                          |
| **2. Official Name**   | `reforge.py`                                             |
| **3. Version**         | **v13.0**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Transmutation**                                        |
| **11. Catalyst**       | **Structure Enforcement**                                |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Knight of Swords persona uses this tool for reforging.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-KNIG-003, EXECUTES, This tool leverages the standard application logic.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Active Execution (The Knight of Swords)
# Synergy Set: The Knight's Charge
# Primary Stat Buff: Speed (+15), Coherence (+10)
# Passive Ability: The Blade of Coherence (Active Refactor)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE` | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment | Zero Entropy |
"""

import argparse
import datetime
import logging
import os
import re

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
ARTIFACT_ID = "Artifact ID"
OFFICIAL_NAME = "Official Name"
HEADER_SCAN_LIMIT = 60
CELESTIAL_CLASS = "Celestial Class"

# Target Directories
TARGET_DIRS = [
    r"c:\Users\Chris\Synarche_Workspace\_governance",
    r"c:\Users\Chris\Synarche_Workspace\axion-core\docs",
    r"c:\Users\Chris\Synarche_Workspace\axion-core\.agent",
    r"c:\Users\Chris\_Desktop_Vault\Phoenix\Obsidian\Where Light Fades",
]

# Codex v13.0 Logic
VALID_DOMAINS = ["PHL", "ARCH", "GVRN", "CRTV", "LOGS"]
VALID_EVOLUTIONS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
]

# Domain Inference Map (Folder Name -> Domain Code)
DOMAIN_MAP = {
    "governance": "GVRN",
    "documentation": "ARCH",
    "philosophy": "PHL",
    "creative": "CRTV",
    "logs": "LOGS",
    "gamification": "CRTV",
    "protocol": "GVRN",
    "system": "ARCH",
    "architecture": "ARCH",
    ".agent": "ARCH",
}

# Defaults
DEFAULT_EVOLUTION = "Purposeful Drive"
DEFAULT_ESF = "ESF-GAMMA"
DEFAULT_STATE = "[ACTIVE]"

PROMPT_PACKET_TEMPLATE = """
## IV. Actionable Prompt Packet (APP)

| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD:AUDIT_COMPLIANCE` | Audit against v13.0 standards. | Enforces Supreme Law. |
| `⚡ EXECUTE:CANONIZE_PAL` | Formally cement alignment with governance. | Eliminates technical debt. |
"""


def infer_domain(filepath: str) -> str:
    """Infer domain code based on filepath keywords."""
    path_lower = filepath.lower()
    if "_governance" in path_lower or "governance" in path_lower:
        return "GVRN"
    if "logs" in path_lower or "log" in path_lower:
        return "LOGS"
    if "philosophy" in path_lower:
        return "PHL"
    if "creative" in path_lower or "lore" in path_lower:
        return "CRTV"
    for key, code in DOMAIN_MAP.items():
        if key in path_lower:
            return code
    return "ARCH"


def extract_existing_metadata(content: str) -> dict[str, str]:
    """Extracts existing metadata from the UIP table or blockquote."""
    metadata: dict[str, str] = {}
    # Match pipe table rows: | **Key** | `Value` | or | Key | Value |
    table_rows = re.findall(r"\| \s*\**?\d*\.?\s*(.*?)\**? \s*\| \s*(.*?) \s*\|", content)
    for key, value in table_rows:
        k = key.strip().strip("*")
        v = re.sub(r"[`\*]", "", value).strip()
        if k and k not in ["Field", "Attribute", "Value"]:
            metadata[k] = v

    # Fallback: blockquote metadata
    bq_matches = re.findall(r">\s*\*\*([A-Za-z0-9\s]+)\*\*[:\s]+(.*)(?:\n|$)", content)
    for key, value in bq_matches:
        k = key.strip()
        if k not in metadata:
            metadata[k] = value.strip()
    return metadata


def generate_header(metadata: dict[str, str], filepath: str) -> str:
    """Generates a v13.0 compliant UIP header."""
    filename = os.path.basename(filepath)
    domain_code = infer_domain(filepath)
    existing_domain = metadata.get("Domain", "").upper()
    for d in VALID_DOMAINS:
        if d in existing_domain:
            domain_code = d
            break

    evo = metadata.get("Evolution", metadata.get("Evolutionary Alignment", DEFAULT_EVOLUTION))
    if evo not in VALID_EVOLUTIONS:
        evo = DEFAULT_EVOLUTION

    header_fields = {
        ARTIFACT_ID: metadata.get(ARTIFACT_ID, os.path.splitext(filename)[0]),
        OFFICIAL_NAME: metadata.get(OFFICIAL_NAME, filename),
        "Version": "v13.0",
        "Provenance": metadata.get(
            "Provenance",
            f"Genesis Stamp: {datetime.datetime.now().strftime('%Y-%m-%d')}",
        ),
        "Domain": domain_code,
        "Evolution": evo,
        "Signal (ESF)": metadata.get("Signal (ESF)", DEFAULT_ESF),
        "Status (State)": metadata.get("Status (State)", DEFAULT_STATE),
        "Tier": metadata.get("Tier", "Operational"),
        CELESTIAL_CLASS: metadata.get(CELESTIAL_CLASS, "[PLANET]"),
        "Ethos": metadata.get("Ethos", "Guardian of Coherence"),
        "Catalyst": metadata.get("Catalyst", "Governance Alignment"),
        "Relations": metadata.get("Relations", "Governed by v13.0"),
        "Upstream": metadata.get("Upstream", "N/A"),
        "Downstream": metadata.get("Downstream", "N/A"),
        "Integrity Hash": metadata.get("Integrity Hash", "N/A"),
    }

    table_lines = [
        "---",
        "# Universal Identification & Provenance (UIP)",
        "| Attribute | Value |",
        "| :--- | :--- |",
        f"| **{ARTIFACT_ID}** | `{header_fields[ARTIFACT_ID]}` |",
        f"| **{OFFICIAL_NAME}** | `{header_fields[OFFICIAL_NAME]}` |",
        f"| **Version** | **{header_fields['Version']}** |",
        f"| **Domain** | `{header_fields['Domain']}` |",
        f"| **Evolution** | **{header_fields['Evolution']}** |",
        f"| **Signal (ESF)** | `{header_fields['Signal (ESF)']} ` |",
        f"| **Status (State)** | `{header_fields['Status (State)']} ` |",
        f"| **Tier** | **{header_fields['Tier']}** |",
        f"| **{CELESTIAL_CLASS}** | `{header_fields[CELESTIAL_CLASS]}` |",
        f"| **Upstream** | `{header_fields['Upstream']}` |",
        f"| **Downstream** | `{header_fields['Downstream']}` |",
        f"| **Integrity Hash** | `{header_fields['Integrity Hash']}` |",
        f"| **Provenance** | `{header_fields['Provenance']}` |",
        f"| **Relations** | `{header_fields['Relations']}` |",
        "---",
    ]

    return "\n".join(table_lines)


def clean_formatting(text: str) -> str:
    """Fix MD022 (header blank lines) and MD030 (list spacing)."""
    # Fix MD022: Ensure headers are surrounded by blank lines
    text = re.sub(r"\n+(#+ .*)\n+", r"\n\n\1\n\n", text)

    # Fix MD030: Ensure exactly one space after list markers
    lines = text.splitlines()
    cleaned_lines: list[str] = []
    for line in lines:
        match = re.match(r"^(\s*[*+-]|\s*\d+\.)\s{2,}(\S.*)$", line)
        if match:
            cleaned_lines.append(f"{match.group(1)} {match.group(2)}")
        else:
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _is_header_start_line(line: str) -> bool:
    """Check if a line looks like a header/metadata line to skip."""
    s = line.strip()
    if not s:
        return False

    if s.startswith("######") or s.startswith("---") or s.startswith("[ARTIFACT START]"):
        return True
    if s.startswith("| ") and ("Attribute" in s or "Field" in s or "Value" in s or ":---" in s):
        return True

    metadata_keys = [
        ARTIFACT_ID,
        OFFICIAL_NAME,
        "Version",
        "Provenance",
        "Domain",
        "Evolution",
        CELESTIAL_CLASS,
        "Tier",
        "State",
        "Ethos",
        "Catalyst",
        "Relations",
        "Genesis Stamp",
        "Universal Identification",
        "Vector Signature",
        "Upstream",
        "Downstream",
    ]

    if not (s.startswith("|") or s.startswith("**") or s.startswith("> ") or "stamp" in s.lower()):
        return False

    return any(key in s for key in metadata_keys)


def _extract_body_content(lines: list[str], filename: str) -> tuple[str, list[str]]:
    """Extracts the H1 and the body lines from the content."""
    h1_line = None
    body_start_index = 0

    for i, line in enumerate(lines):
        if line.strip().startswith("# "):
            h1_line = line.strip()
            body_start_index = i + 1
            break

    if not h1_line:
        h1_line = f"# {os.path.splitext(filename)[0]}"
        body_start_index = 0

    # Skip header noise
    idx = body_start_index
    while idx < len(lines):
        line = lines[idx].strip()
        if not line or _is_header_start_line(line):
            idx += 1
        elif line.startswith("#"):
            clean_title = line.strip("# ").strip("*").lower()
            if clean_title.startswith(("i. ", "ii. ", "iii. ")):
                idx += 1
            else:
                break
        else:
            break

    return h1_line, lines[idx:]


def _is_redundant_metadata(line: str, index: int) -> bool:
    """Checks if a line is redundant metadata that should be removed."""
    if index >= HEADER_SCAN_LIMIT:
        return False

    sbl_lower = line.strip().lower()
    if "step" in sbl_lower or "phase" in sbl_lower:
        return False

    kill_keywords = [
        ARTIFACT_ID,
        OFFICIAL_NAME,
        "version",
        "provenance",
        CELESTIAL_CLASS,
        "tier",
        "ethos",
        "catalyst",
        "relations",
        "evolution",
        "chronos lock",
        "metadata layer",
        "universal identification & provenance",
        "vector signature",
        "genesis stamp",
        "upstream",
        "downstream",
        "module id",
        "status",
    ]
    contextual_kill = ["domain", "state", "tags", "criticality", "signal"]

    if "|" in line and any(kw.lower() in sbl_lower for kw in kill_keywords + contextual_kill):
        return True

    for kw in kill_keywords:
        kw_lower = kw.lower()
        if f"**{kw_lower}" in sbl_lower or f"*{kw_lower}" in sbl_lower:
            return True

    return "| Attribute | Value |" in line or "| Field | Value |" in line or "| :---" in line


def _process_body(body_lines: list[str]) -> str:
    """Filters and cleans the body content."""
    filtered: list[str] = []
    for i, line in enumerate(body_lines):
        if _is_redundant_metadata(line, i):
            continue
        filtered.append(line)

    body_text = "\n".join(filtered)
    return clean_formatting(body_text)


def process_file(filepath: str) -> None:
    """Reforges a single file to v13.0 standards."""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        logger.exception(f"[!] Read failed: {filepath}")
        return

    filename = os.path.basename(filepath)
    logger.info(f"Reforging: {filename}")

    metadata = extract_existing_metadata(content)
    lines = content.splitlines()

    h1_line, raw_body = _extract_body_content(lines, filename)
    body_text = _process_body(raw_body)

    # Finalize APP
    if "IV. Actionable Prompt Packet (APP)" not in body_text:
        # If there's a legacy APP header, replace it
        if "Actionable Prompt Packet" in body_text:
            body_text = re.sub(
                r"#+ .*Actionable Prompt Packet.*", PROMPT_PACKET_TEMPLATE.strip(), body_text, flags=re.IGNORECASE
            )
        else:
            body_text += f"\n\n---\n{PROMPT_PACKET_TEMPLATE}"

    if "[ARTIFACT END]" not in body_text:
        body_text += "\n\n###### **[ARTIFACT END]**"

    new_header = generate_header(metadata, filepath)
    final_content = f"{h1_line}\n\n{new_header}\n\n{body_text.strip()}\n"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
    except Exception:
        logger.exception(f"[!] Write failed: {filepath}")


def scan_targets(targets: list[str]) -> None:
    """Recursively scan and process targets."""
    for d in targets:
        if not os.path.exists(d):
            logger.warning(f"[WARN] Target not found: {d}")
            continue

        if os.path.isfile(d):
            if d.endswith(".md"):
                process_file(d)
        else:
            for root, _, files in os.walk(d):
                for file in files:
                    if file.endswith(".md"):
                        process_file(os.path.join(root, file))


def main() -> None:
    parser = argparse.ArgumentParser(description="Reforge artifacts to v13.0 standards.")
    parser.add_argument("targets", nargs="*", help="Optional target directories or files.")
    args = parser.parse_args()

    targets = args.targets if args.targets else TARGET_DIRS
    logger.info("Starting Reforge v13.0 (Zero Entropy alignment)...")
    scan_targets(targets)
    logger.info("Reforge v13.0 Complete.")


if __name__ == "__main__":
    main()
