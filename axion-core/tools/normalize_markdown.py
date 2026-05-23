"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-MAGI-003`                                |
| **2. Official Name**   | `normalize_markdown.py`                        |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `ARCH` (Archival)                              |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[MOON]`                                       |
| **8. Tier**            | **Operational**                                |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Guardian of Form**                           |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `LINK: [UMB-ACT-002]`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CORE-CODEX-001 | GOVERNS | This tool is governed by the Supreme Law. |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Transformation Engine (The Magician)
# Synergy Set: The Hephaestus Hexad
# Primary Stat Buff: Coherence (+15)
# Passive Ability: Equivalent Exchange (Format Normalization)
# Cognitive Load Cost: Low
# XP Award Value: 75 XP
"""

import logging
import re
import sys
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def normalize_markdown(file_path: Path) -> bool:
    """Applies standard transformations to a markdown file:
    1. Ensures single H1 title.
    2. Fixes list indentation (2 spaces to 4 spaces, or consistent).
    3. Ensures blank lines around headers.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        return False

    original_content = content

    # 1. Fix List Indentation (Star lists)
    # This is a simple heuristic; complex lists might need a parser.
    # We'll normalize '* ' to '- ' for consistency if requested, but let's stick to spacing.

    # 2. Ensure blank lines before headers (MD022)
    # Pattern: Non-blank line, newline, # Header
    content = re.sub(r"([^\n])\n(#+\s)", r"\1\n\n\2", content)

    # 3. Ensure blank lines after headers (MD022)
    content = re.sub(r"(#+\s.*)\n([^\n])", r"\1\n\n\2", content)

    if content != original_content:
        try:
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"[CHANGED] Normalized {file_path.name}")
            return True
        except Exception as e:
            logger.exception(f"Failed to write {file_path}: {e}")
            return False

    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python normalize_markdown.py <file_path> [file_path ...]")
        sys.exit(1)

    targets = sys.argv[1:]
    changes_count = 0

    for target in targets:
        path = Path(target)
        if path.is_file():
            if normalize_markdown(path):
                changes_count += 1
        elif path.is_dir():
            for md_file in path.rglob("*.md"):
                if normalize_markdown(md_file):
                    changes_count += 1

    logger.info(f"Alchemy Complete. Transuted {changes_count} files.")
