"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.utils.guca_healer`                  | The Sovereign ID. |
| **Official Name** | `guca_healer.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Metadata Erasure** | Append-Only Header Injection |
# | **Encoding Conflict** | Enforced UTF-8 Normalization |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**

The GUCA-HEALER Unit: Scans the workspace for Orphan Nodes missing the UIP / OMEGA headers.
Automates the 'Healing' of non-compliant artifacts through header injection.
Conforms to OGLN/AISTF v15.0 compliance standards.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Optional

# Ensure standard output uses UTF-8 to handle specialized characters
sys.stdout.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Users/Chris/Synarche_Workspace")
TARGET_DIRS = ["_governance", "axion-core"]

# Patterns to identify compliance status
UIP_PATTERN = re.compile(r"## \*\*Block A: The Identification Lock \(UIP-V15\)\*\*", re.IGNORECASE)
UIP_ALT_PATTERN = re.compile(r"# Universal Identification & Provenance \(UIP\)", re.IGNORECASE)


def generate_uip_header(file_name: str) -> str:
    """
    Generates a standardized OMEGA v15.0 UIP header for an orphan file.

    Args:
        file_name: The name of the file to generate the header for.

    Returns:
        A multi-line string containing the formatted UIP block.
    """
    module_id = file_name.replace(".md", "").upper()
    return f"""---
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `SYNG.AUTO.{module_id}`          | The Sovereign ID. |
| **Official Name** | `{file_name}`                     | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `AUTO`                            | The Subject.      |
| **Status (State)**| `[ACTIVE]`                        | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

---
## **[ARTIFACT END]**

"""


def scan_for_orphans(heal: bool = False) -> None:
    """
    Scans the specified target directories for Markdown files missing compliance headers.

    Args:
        heal: If True, automatically prepends a generated header to orphan files.
    """
    orphan_nodes: list[Path] = []
    scanned_files = 0

    for target in TARGET_DIRS:
        target_path = WORKSPACE_ROOT / target
        if not target_path.exists():
            continue

        for root, _dirs, files in os.walk(target_path):
            # Skip noise directories and archives
            if any(
                skip in root
                for skip in [
                    "node_modules",
                    "__pycache__",
                    ".git",
                    "vendor",
                    "_archive",
                    "docs\\agents",
                    "docs\\commands",
                    "docs\\specs",
                ]
            ):
                continue

            for file in files:
                if file.endswith(".md"):
                    scanned_files += 1
                    file_path = Path(root) / file

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            # Read just the head to look for UIP patterns
                            content = f.read(2048)

                            if not UIP_PATTERN.search(content) and not UIP_ALT_PATTERN.search(content):
                                orphan_nodes.append(file_path)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    print(f"\nScan Complete. Total MD files scanned: {scanned_files}")
    if orphan_nodes:
        print(f"Detected {len(orphan_nodes)} Orphan Nodes (Missing UIP):")
        for node in orphan_nodes:
            print(f" - {node.relative_to(WORKSPACE_ROOT)}")

            if heal:
                try:
                    with open(node, "r", encoding="utf-8") as f:
                        original_content = f.read()

                    header = generate_uip_header(node.name)
                    with open(node, "w", encoding="utf-8") as f:
                        f.write(header + original_content)
                    print(f"   [HEALED] Applied canonical OMEGA header to {node.name}")
                except Exception as e:
                    print(f"   [ERROR] Failed to heal {node.name}: {e}")
    else:
        print("System Coherence is at 100%. No Orphan Nodes detected.")


if __name__ == "__main__":
    heal_mode = "--heal" in sys.argv
    scan_for_orphans(heal=heal_mode)

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.utils.guca_healer VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [ACTIVE] TS: 2026-03-28
# ---
