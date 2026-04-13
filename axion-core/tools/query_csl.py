#!/usr/bin/env python3
"""
# TOOL-GVRN-003: The Chronicler's Eye (High Priestess Suite)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-GVRN-003`                                          |
| **2. Official Name**   | `query_csl.py`                                           |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[NEPTUNE]`                                              |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Chronicling Insight**                                  |
| **11. Catalyst**       | **CSL Archival Query**                                   |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this to query past logs.
GVRN-SYNERGY-001, GOVERNS, This tool manages the Collaborative Synthesis Log.
TOOL-HPRI-007, SYNERGY, Works with reflect_memory.py for contextual retrieval.

---
"""

import argparse
import os
import re
from pathlib import Path

# Constants
CSL_DIR = Path("c:/Users/Chris/_Desktop_Vault/Phoenix/Documentation/Library/5_Logs/CSL")


def query_logs(filter_text: str, limit: int):
    """Queries logs for a specific keyword or tag."""

    if not CSL_DIR.exists():
        print("Error: CSL directory not found.")
        return

    logs = list(CSL_DIR.glob("*.md"))
    matches = []

    for log_path in logs:
        try:
            content = log_path.read_text(encoding="utf-8")
            if filter_text.lower() in content.lower():
                # Extract title from H1
                match = re.search(r"^#\s*(.*)", content, re.MULTILINE)
                title = match.group(1) if match else log_path.name
                matches.append((log_id := log_path.stem, title, log_path))
        except Exception:
            continue

    if not matches:
        print(f"No CSL entries found matching: '{filter_text}'")
        return

    print(f"\n🔍 FOUND {len(matches)} ENTRIES (Limit: {limit}):\n")
    for i, (log_id, title, path) in enumerate(matches[:limit]):
        print(f"{i + 1}. [{log_id}] {title}")
        print(f"   Path: {path}\n")


def main():
    parser = argparse.ArgumentParser(description="QUERY_CSL: Search the CSL archives.")
    parser.add_argument("--filter", required=True, help="Keyword or tag to search for.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results.")

    args = parser.parse_args()
    query_logs(args.filter, args.limit)


if __name__ == "__main__":
    main()
