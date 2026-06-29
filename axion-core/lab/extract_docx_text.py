"""# TOOL-MAGI-002: DOCX Text Extractor (The Magician's Focus).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-MAGI-002`                                          |
| **2. Official Name**   | `extract_docx_text.py`                                   |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Purposeful Drive**                                     |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Unveiling**                                            |
| **11. Catalyst**       | **Extraction Protocol**                                  |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Magician persona uses this tool for extraction.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Ingestion Gate (The Magician)
# Synergy Set: The Hephaestus Hexad
# Primary Stat Buff: Intelligence (+10)
# Passive Ability: The Unveiling (Text Extraction)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: EXTRACT_DOCX` | Convert DOCX to TXT | Raw Content Retrieval |
| `⚡ EXECUTE: BATCH_EXT` | Batch Conversion | High Volume Ingestion |
"""

import logging
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def extract_text_from_docx(docx_path: str, output_path: str) -> str:
    """Extracts raw text from a DOCX file by parsing the internal XML.
    Returns a status message.
    """
    try:
        with zipfile.ZipFile(docx_path) as zf:
            xml_content = zf.read("word/document.xml")

        root = ET.fromstring(xml_content)

        # Define namespace (Word usually uses this)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

        text_parts = []
        for p in root.findall(".//w:p", ns):
            para_text = []
            for t in p.findall(".//w:t", ns):
                if t.text:
                    para_text.append(t.text)
            text_parts.append("".join(para_text))

        full_text = "\n".join(text_parts)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    except Exception as e:
        logger.error(f"Error extracting {docx_path}: {e}")
        return f"ERROR_EXTRACTING: {e!s}"
    else:
        return f"SUCCESS: Extracted to {output_path}"


if __name__ == "__main__":
    MIN_ARGS = 3
    if len(sys.argv) < MIN_ARGS:
        logger.error("Usage: python extract_docx_text.py <docx_path> <output_txt_path>")
        sys.exit(1)

    docx_path_arg = sys.argv[1]
    output_path_arg = sys.argv[2]

    if not Path(docx_path_arg).exists():
        logger.error(f"File not found: {docx_path_arg}")
        sys.exit(1)

    result = extract_text_from_docx(docx_path_arg, output_path_arg)
    logger.info(result)
