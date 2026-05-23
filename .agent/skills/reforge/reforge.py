import argparse
import datetime
import logging
import os
import re

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
ARTIFACT_ID = "Artifact ID"
OFFICIAL_NAME = "Official Name"
HEADER_SCAN_LIMIT = 60
CELESTIAL_CLASS = "Celestial Class"

# Codex v13.0 Logic
VALID_DOMAINS = ["PHL", "ARCH", "GVRN", "CRTV", "LOGS"]
VALID_EVOLUTIONS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
]

# Domain Inference Map
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

PROMPT_PACKET_TEMPLATE = """
## IV. Actionable Prompt Packet (APP)

| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD:AUDIT_COMPLIANCE` | Audit against v13.0 standards. | Enforces Supreme Law. |
| `⚡ EXECUTE:CANONIZE_PAL` | Formally cement alignment with governance. | Eliminates technical debt. |
"""


def infer_domain(filepath: str) -> str:
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
    metadata: dict[str, str] = {}
    table_rows = re.findall(
        r"\| \s*\**?\d*\.?\s*(.*?)\**? \s*\| \s*(.*?) \s*\|", content
    )
    for key, value in table_rows:
        k = key.strip().strip("*")
        v = re.sub(r"[`\*]", "", value).strip()
        if k and k not in ["Field", "Attribute", "Value"]:
            metadata[k] = v
    return metadata


def generate_header(metadata: dict[str, str], filepath: str) -> str:
    filename = os.path.basename(filepath)
    domain_code = infer_domain(filepath)
    existing_domain = metadata.get("Domain", "").upper()
    for d in VALID_DOMAINS:
        if d in existing_domain:
            domain_code = d
            break

    evo = metadata.get("Evolution", "Purposeful Drive")
    if evo not in VALID_EVOLUTIONS:
        evo = "Purposeful Drive"

    header_fields = {
        ARTIFACT_ID: metadata.get(ARTIFACT_ID, os.path.splitext(filename)[0]),
        OFFICIAL_NAME: metadata.get(OFFICIAL_NAME, filename),
        "Version": "v13.0",
        "Provenance": metadata.get(
            "Provenance", f"Reforged: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        ),
        "Domain": domain_code,
        "Evolution": evo,
        "Status (State)": "[ACTIVE]",
        "Tier": "Operational",
        CELESTIAL_CLASS: "[PLANET]",
        "Ethos": "Guardian of Coherence",
        "Catalyst": "Protocol Standardization",
        "Relations": "Governed by v13.0",
        "Integrity Hash": "[AUTO-GENERATED]",
    }

    table_lines = [
        "---",
        "# Universal Identification & Provenance (UIP)",
        "| Field | Value |",
        "| :--- | :--- |",
        f"| **1. Artifact ID** | `{header_fields[ARTIFACT_ID]}` |",
        f"| **2. Official Name** | `{header_fields[OFFICIAL_NAME]}` |",
        f"| **3. Version** | **{header_fields['Version']}** |",
        f"| **4. Provenance** | **{header_fields['Provenance']}** |",
        f"| **5. Domain** | `{header_fields['Domain']}` |",
        f"| **6. Evolution** | **{header_fields['Evolution']}** |",
        f"| **7. Celestial Class** | `{header_fields[CELESTIAL_CLASS]}` |",
        "| **8. Tier** | **Foundational** |",
        f"| **9. Status (State)** | `{header_fields['Status (State)']} ` |",
        f"| **10. Ethos** | `{header_fields['Ethos']}` |",
        f"| **11. Catalyst** | `{header_fields['Catalyst']}` |",
        f"| **12. Relations** | `{header_fields['Relations']}` |",
        f"| **13. Integrity Hash** | `{header_fields['Integrity Hash']}` |",
        "---",
    ]
    return "\n".join(table_lines)


def process_file(filepath: str) -> None:
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"[!] Read failed: {filepath} - {e}")
        return

    filename = os.path.basename(filepath)
    logger.info(f"Reforging: {filename}")

    metadata = extract_existing_metadata(content)
    new_header = generate_header(metadata, filepath)

    # Strip existing header if it exists
    body = re.sub(r"^---.*?---", "", content, flags=re.DOTALL).strip()
    # Strip leading H1 if it matches filename
    body = re.sub(r"^# .*\n", "", body).strip()

    final_content = f"# {os.path.splitext(filename)[0]}\n\n{new_header}\n\n{body}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_content)


def reforge_artifact(
    target_file: str, domain: str = "GVRN", type: str = "Protocol"
) -> None:
    """Entry point for the skill."""
    if os.path.exists(target_file):
        process_file(target_file)
        print(f"Artifact {target_file} successfully reforged to v13.0.")
    else:
        print(f"Error: Target file {target_file} not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reforge artifacts to v13.0.")
    parser.add_argument("target", help="File to reforge")
    args = parser.parse_args()
    reforge_artifact(args.target)
