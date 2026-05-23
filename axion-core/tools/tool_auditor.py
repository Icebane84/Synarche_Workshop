#!/usr/bin/env python3
"""# TOOL-AUDITOR-001: Compliance Auditor CLI (Sentinel Suite).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-AUDITOR-001`                                       |
| **2. Official Name**   | `tool_auditor.py`                                        |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[MARS]`                                                 |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Standards Compliance**                                 |
| **11. Catalyst**       | **OGLN v11.0 Audit**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this for standard audits.
GVRN-SYNERGY-001, GOVERNS, This tool enforces OGLN compliance across the library.
TOOL-SENT-003, SYNERGY, Works with lint_artifact.py for deep structural checks.

---
"""

import argparse
import json
import os
import sys
from dataclasses import asdict

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    from hephaestus.auditor import ComplianceAuditor
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Audit OGLN Compliance")
    parser.add_argument("target", help="File to audit")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Error: File not found {args.target}")
        sys.exit(1)

    auditor = ComplianceAuditor()
    result = auditor.audit_file(args.target)

    # Convert dataclass to dict
    print(json.dumps(asdict(result), indent=2))

    if result.status == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
