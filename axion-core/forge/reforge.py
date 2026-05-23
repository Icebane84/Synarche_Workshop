"""IDENTIFICATION: TOOL-REFORGE-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24.
"""

import argparse
import logging
import os
import re
import sys

# Centralized Sentinel Gates
# Ensure we can find the 'src' directory regardless of how the script is called
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(SCRIPT_DIR)
CORE_ROOT = os.path.dirname(TOOLS_DIR)  # axion-core
SRC_DIR = os.path.join(CORE_ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

try:
    from logic.utils.sentinel_utils import heal_with_ruff, safe_run_command
except ImportError:
    # If called from a place where 'src' is expected to be a package
    if CORE_ROOT not in sys.path:
        sys.path.append(os.path.dirname(CORE_ROOT))  # Synarche_Workspace root
    from axion_core.src.logic.utils.sentinel_utils import heal_with_ruff

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
VALID_DOMAINS = [
    "GVRN",
    "COG",
    "SYNG",
    "ARCH",
    "COMM",
    "PHL",
    "CRTV",
    "NOVA",
    "WLF",
    "AXION",
    "LOGS",
    "TMPL",
]
VALID_EVOLUTIONS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
    "Phoenix Form",
    "SOVEREIGN",
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
    ".agent": "AXION",
    "axion-core": "AXION",
    "nova_forge": "NOVA",
}

# Defaults
DEFAULT_EVOLUTION = "Purposeful Drive"
DEFAULT_STATE = "[ACTIVE]"

# v13.0 AGP Templates
AGP_STATE_VECTOR = """
### **Block B: State Vector (AGP-001)**
| State Field | Value |
| :--- | :--- |
| **Coherence** | `1.0` |
| **Resonance** | `0.9` |
| **Stability** | `Stable` |
"""

AGP_RISK_BLOCK = """
### **Block C: Risk & Mitigation (AGP-002)**
| Risk | Mitigation |
| :--- | :--- |
| **Logic Drift** | Strict Linter Enforcement |
| **Dependency Break** | ForgeLink Validation |
"""

PROMPT_PACKET_TEMPLATE = """
### **Block D: Standardized Synergy Block (The Loom Signature)**
Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: REFORGE` | Execute Structural Transmutation | Canonization |
| `⚡ EXECUTE: CANONIZE` | Formally Cement Alignment | Zero Entropy |

---

### **Rationale (The "Why")**
{rationale}
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
    table_rows = re.findall(
        r"\| \s*\**?\d*\.?\s*(.*?)\**? \s*\| \s*(.*?) \s*\|", content
    )
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
    """Generates a v11.0 compliant UIP header."""
    filename = os.path.basename(filepath)
    domain_code = infer_domain(filepath)
    existing_domain = metadata.get("Domain", "").upper()
    for d in VALID_DOMAINS:
        if d in existing_domain:
            domain_code = d
            break

    evo = metadata.get(
        "Evolution", metadata.get("Evolutionary Alignment", DEFAULT_EVOLUTION)
    )
    if evo not in VALID_EVOLUTIONS:
        evo = DEFAULT_EVOLUTION

    header_fields = {
        ARTIFACT_ID: metadata.get(ARTIFACT_ID, os.path.splitext(filename)[0]),
        OFFICIAL_NAME: metadata.get(OFFICIAL_NAME, filename),
        "Version": "v14.0 [OMEGA]",
        "Domain": domain_code,
        "Celestial Class": metadata.get(CELESTIAL_CLASS, "[PLANET]"),
        "Evolution": evo,
        "Status": metadata.get("Status", metadata.get("Status (State)", DEFAULT_STATE)),
        "Ethos": metadata.get("Ethos", "Crystalline Structure"),
        "Relations": metadata.get("Relations", "GOVERNED_BY: CORE-CODEX-001"),
        "Integrity Hash": metadata.get("Integrity Hash", "[AUTO-GENERATED]"),
    }

    table_lines = [
        "### **Block A: The Identification Lock (UIP-V14)**",
        "",
        "| Key | Value | Description |",
        "| :--- | :--- | :--- |",
        f"| **Artifact ID** | `{header_fields[ARTIFACT_ID]}` | The Sovereign ID. |",
        f"| **Official Name** | `{header_fields[OFFICIAL_NAME]}` | The Filename. |",
        f"| **Version** | **{header_fields['Version']}** | The Standard. |",
        f"| **Domain** | `{header_fields['Domain']}` | The Subject. |",
        f"| **Celestial Class** | `{header_fields['Celestial Class']}` | The Weight. |",
        f"| **Evolution** | `{header_fields['Evolution']}` | The Maturity. |",
        f"| **Status (State)** | `{header_fields['Status']}` | The Lifecycle. |",
        f"| **Ethos** | `{header_fields['Ethos']}` | The Intent. |",
        f"| **Relations** | `{header_fields['Relations']}` | The Network. |",
        f"| **Integrity Hash** | `{header_fields['Integrity Hash']}` | Verification. |",
        "",
        "---",
    ]

    return "\n".join(table_lines)


def _ensure_header_spacing(text: str) -> str:
    """Fix MD022: Ensure headers are surrounded by blank lines."""
    return re.sub(r"\n+(#+ .*)\n+", r"\n\n\1\n\n", text)


def _fix_list_markers(line: str) -> str:
    """Fix MD030: Ensure exactly one space after list markers."""
    match = re.match(r"^(\s*[*+-]|\s*\d+\.)\s{2,}(\S.*)$", line)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return line


def _handle_list_transitions(
    is_list_item: bool, in_list: bool, current_line: str, history: list[str]
) -> bool:
    """MD032: Add blank lines before/after lists if needed. Returns new 'in_list' state."""
    # Before list starts
    if is_list_item and not in_list:
        if history and history[-1].strip() != "":
            history.append("")
        return True

    # After list ends
    if not is_list_item and in_list:
        if current_line.strip() != "" and history and history[-1].strip() != "":
            history.append("")
        return False

    return in_list


def _apply_list_rules(lines: list[str]) -> list[str]:
    """Fix MD030 (list spacing) and MD032 (list surrounding)."""
    cleaned_lines: list[str] = []
    in_list = False

    for line in lines:
        is_list_item = bool(re.match(r"^(\s*[*+-]|\s*\d+\.)\s", line))

        in_list = _handle_list_transitions(is_list_item, in_list, line, cleaned_lines)

        _line = _fix_list_markers(line) if is_list_item else line
        cleaned_lines.append(_line)

    return cleaned_lines


def clean_formatting(text: str) -> str:
    """Fix MD022 (headers), MD030 (list spacing), and MD032 (list surrounding)."""
    text = _ensure_header_spacing(text)
    lines = text.splitlines()
    cleaned_lines = _apply_list_rules(lines)

    text = "\n".join(cleaned_lines)
    # Final cleanup of multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _is_header_start_line(line: str) -> bool:
    """Check if a line looks like a header/metadata line to skip."""
    s = line.strip()
    if not s:
        return False

    if (
        s.startswith("######")
        or s.startswith("---")
        or s.startswith("[ARTIFACT START]")
    ):
        return True
    if s.startswith("| ") and (
        "Attribute" in s or "Field" in s or "Value" in s or ":---" in s
    ):
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

    if not (
        s.startswith("|")
        or s.startswith("**")
        or s.startswith("> ")
        or "stamp" in s.lower()
    ):
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
        "universal identification",
        "vector signature",
        "genesis stamp",
        "upstream",
        "downstream",
        "module id",
        "status",
        "block a",
        "block b",
        "block c",
        "block d",
    ]
    contextual_kill = ["domain", "state", "tags", "criticality", "signal"]

    if "|" in line and any(
        kw.lower() in sbl_lower for kw in kill_keywords + contextual_kill
    ):
        return True

    for kw in kill_keywords:
        kw_lower = kw.lower()
        if f"**{kw_lower}" in sbl_lower or f"*{kw_lower}" in sbl_lower:
            return True

    return (
        "| Attribute | Value |" in line
        or "| Field | Value |" in line
        or "| Key | Value |" in line
        or "| State Field | Value |" in line
        or "| Risk | Mitigation |" in line
        or "| :---" in line
    )


def _process_body(body_lines: list[str]) -> str:
    """Filters and cleans the body content."""
    filtered: list[str] = []
    for i, line in enumerate(body_lines):
        if _is_redundant_metadata(line, i):
            continue
        filtered.append(line)

    body_text = "\n".join(filtered)
    return clean_formatting(body_text)


def process_file(
    filepath: str, rationale: str = "Alignment with OMEGA v14.0 Semantic Standards."
) -> None:
    """Reforges a single file to v14.0 standards."""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        logger.exception(f"[AXION] [!] Read failed: {filepath}")
        return

    filename = os.path.basename(filepath)
    logger.info(f"[AXION] Reforging: {filename} (Rationale: {rationale})")

    metadata = extract_existing_metadata(content)
    lines = content.splitlines()

    h1_line, raw_body = _extract_body_content(lines, filename)
    body_text = _process_body(raw_body)

    # Finalize Blocks in correct order
    blocks_to_inject = ""
    if "Block B: State Vector" not in body_text:
        blocks_to_inject += AGP_STATE_VECTOR.strip() + "\n\n"

    if "Block C: Risk & Mitigation" not in body_text:
        blocks_to_inject += AGP_RISK_BLOCK.strip() + "\n\n"

    body_text = blocks_to_inject + body_text

    # Replace old APP logic with Block D + enhanced APP
    formatted_app = PROMPT_PACKET_TEMPLATE.strip().format(rationale=rationale)
    if "Block D: Standardized Synergy Block" not in body_text:
        if "Actionable Prompt Packet" in body_text:
            body_text = re.sub(
                r"#+ .*Actionable Prompt Packet.*",
                formatted_app,
                body_text,
                flags=re.IGNORECASE | re.DOTALL,
            )
        else:
            body_text += f"\n\n{formatted_app}"

    if "[ARTIFACT END]" not in body_text:
        body_text += "\n\n###### **[ARTIFACT END]**"

    new_header = generate_header(metadata, filepath)
    final_content = f"{h1_line}\n\n{new_header}\n\n{body_text.strip()}\n"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
    except Exception:
        logger.exception(f"[!] Write failed: {filepath}")


def _scan_directory_recursive(directory: str, rationale: str) -> None:
    """Recursively process all markdown files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), rationale)


def scan_targets(targets: list[str], rationale: str) -> None:
    """Recursively scan and process targets."""
    for target in targets:
        if not os.path.exists(target):
            logger.warning(f"[AXION] [WARN] Target not found: {target}")
            continue

        if os.path.isfile(target):
            if target.endswith(".md"):
                process_file(target, rationale)
        else:
            _scan_directory_recursive(target, rationale)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reforge artifacts to v14.0 standards."
    )
    parser.add_argument(
        "targets", nargs="*", help="Optional target directories or files."
    )
    parser.add_argument(
        "--heal", action="store_true", help="Automatically fix linter problems."
    )
    parser.add_argument(
        "--rationale",
        default="Alignment to v14.0 OMEGA standard.",
        help="The Architectural Rationale.",
    )
    args = parser.parse_args()

    targets = args.targets if args.targets else TARGET_DIRS
    rationale = args.rationale
    logger.info("[AXION] Starting Reforge v14.0 (Axiom Ascension)...")
    logger.info(
        '> "Entropy is the enemy. Structure is the shield. Coherence is the sword." — UEB-GOC-001\n'
    )

    if args.heal:
        logger.info("[AXION] Activating Heal Protocol...")
        heal_with_ruff(targets)

    scan_targets(targets, rationale)
    logger.info("[AXION] Reforge v14.0 Complete.")


if __name__ == "__main__":
    main()
