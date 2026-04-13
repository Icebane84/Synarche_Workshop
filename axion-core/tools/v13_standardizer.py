"""
# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HIER-001`                                |
| **2. Official Name**   | `v13_standardizer.py`                          |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `GVRN` (Governance)                            |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Guardian of Tradition**                  |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `UPGRADES: ALL_v11_ARTIFACTS`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |
"""

import datetime
import re
import sys
from pathlib import Path

# v13.0 UIP Template
UIP_HEADER_TEMPLATE = """# {id}: {name} (v13.0)

## Genesis Stamp: {date} | Domain: {domain} | State: {state} | Criticality: {crit}

**Tags:** {tags}

---

### I. Universal Identification & Provenance (The Vector Signature)

#### The Chronos Lock & Axiomatic Metadata Layer

| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `{id}`                                         |
| **2. Official Name**   | `{filename}`                                   |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: {date}**                           |
| **5. Domain**          | `{domain}` ({domain_name})                      |
| **6. Evolution**       | **Crystalline Coherence**                      |
| **7. Celestial Class** | `[{class_}]`                                   |
| **8. Tier**            | **{tier}**                                     |
| **9. Status (State)**  | `{state}`                                      |
| **10. Ethos**          | `{ethos}`                                      |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `GOVERNED_BY: [CORE-CODEX-001]`                |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |

---
"""

DOMAIN_MAP = {
    "GVRN": "Governance",
    "SYNR": "Synarche",
    "ARCH": "Archival",
    "SYNG": "Synergy",
    "EVOL": "Evolution",
    "TECH": "Technical",
    "CRTV": "Creativity",
}


def extract_old_data(content: str) -> dict:
    """Extracts basic metadata from v11.0 artifacts."""
    data = {
        "id": "Unknown",
        "name": "Unknown",
        "domain": "GVRN",
        "tier": "Operational",
        "class_": "PLANET",
        "state": "[ACTIVE]",
        "ethos": "Modernized Artifact",
        "tags": "`v13.0`, `Ascended` ",
    }

    # Try to find Artifact ID
    match_id = re.search(r"\*\*1\. Artifact ID\*\*\s*\|\s*`?(.*?)`?\s*\|", content)
    if match_id:
        data["id"] = match_id.group(1).strip(" `")

    # Try to find Official Name
    match_name = re.search(r"\*\*2\. Official Name\*\*\s*\|\s*`?(.*?)`?\s*\|", content)
    if match_name:
        data["name"] = match_name.group(1).replace(".md", "").strip(" `")

    # Try to find Domain
    match_domain = re.search(r"\*\*5\. Domain\*\*\s*\|\s*`?(.*?)`?\s*\|", content)
    if match_domain:
        data["domain"] = match_domain.group(1).split("(")[0].strip(" `")

    return data


def standardize_file(file_path: Path) -> bool:
    """Upgrades a v11.0 artifact to v13.0."""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding="utf-8")

    if "Version**         | **v13.0**" in content:
        print(f"Skipping {file_path.name}: Already v13.0")
        return False

    data = extract_old_data(content)
    date_str = datetime.date.today().strftime("%Y-%m-%d")

    header = UIP_HEADER_TEMPLATE.format(
        id=data["id"],
        name=data["name"],
        date=date_str,
        domain=data["domain"],
        domain_name=DOMAIN_MAP.get(data["domain"], "Unknown"),
        state=data["state"],
        crit="High",
        tags=data["tags"],
        filename=file_path.name,
        class_=data["class_"],
        tier=data["tier"],
        ethos=data["ethos"],
    )

    # Find start of content after the old UIP table (usually ends with ---)
    parts = content.split("---")
    if len(parts) < 3:
        print(f"Error parsing {file_path.name}: UIP boundaries not found.")
        return False

    # Keep everything after the second --- (the end of the old UIP table)
    # But we want to skip the legacy synergy block if it was just text
    rest = "---".join(parts[2:])

    new_content = header + rest

    try:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Upgraded {file_path.name} to v13.0")
        return True
    except Exception as e:
        print(f"Failed to upgrade {file_path.name}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python v13_standardizer.py <target_file_or_dir>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.is_file():
        standardize_file(target)
    elif target.is_dir():
        for f in target.rglob("*.md"):
            standardize_file(f)
