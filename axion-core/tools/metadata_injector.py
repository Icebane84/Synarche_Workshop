"""
# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPR-007`                                |
| **2. Official Name**   | `metadata_injector.py`                         |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `SYNG` (Synergy)                               |
| **6. Evolution**       | **Crystalline Coherence**                      |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **The Loom Weaver**                            |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `MODIFIES: ALL_ARTIFACTS`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |
"""

import sys
from pathlib import Path

SYNERGY_BLOCK_TEMPLATE = """
---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
{links}

---
"""


def inject_metadata(file_path: Path, relationships: list[tuple[str, str, str]]) -> bool:
    """
    Injects or updates a Standardized Synergy Block in a markdown file.
    Expects relationships as a list of (ArtifactID, RelType, Impact).
    """
    if not file_path.exists():
        print(f"Error: File not found {file_path}")
        return False

    content = file_path.read_text(encoding="utf-8")

    # Check if a synergy block already exists
    if "### **I.B. Standardized Synergy Block" in content:
        print(f"Skipping {file_path.name}: Synergy block already exists.")
        return False

    # Find the end of the UIP header (marked by ---)
    # Usually the second --- in the file (one at start, one at end of UIP table)
    parts = content.split("---")
    if len(parts) < 3:
        print(f"Skipping {file_path.name}: Could not find standard UIP header boundaries.")
        return False

    links_str = ""
    for aid, rel, impact in relationships:
        links_str += f"| {aid} | {rel} | {impact} |\n"

    synergy_block = SYNERGY_BLOCK_TEMPLATE.format(links=links_str.strip())

    # Reconstruct content: [Start] --- [UIP Table] --- [Synergy Block] [Rest]
    new_content = parts[0] + "---" + parts[1] + "---" + synergy_block + "---".join(parts[2:])

    try:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Successfully injected synergy block into {file_path.name}")
        return True
    except Exception as e:
        print(f"Error writing to {file_path.name}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python metadata_injector.py <target_file> <AID> <REL> <IMPACT>")
        print("Example: python metadata_injector.py my_doc.md CORE-CODEX-001 GOVERNS 'Governed by Codex'")
        sys.exit(1)

    target_file = Path(sys.argv[1])
    aid_arg = sys.argv[2]
    rel_arg = sys.argv[3]
    impact_arg = sys.argv[4]

    inject_metadata(target_file, [(aid_arg, rel_arg, impact_arg)])
