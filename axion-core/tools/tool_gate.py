#!/usr/bin/env python3
"""
# TOOL-GATE-001: The Hephaestus Gate CLI (Sentinel Suite)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-GATE-001`                                          |
| **2. Official Name**   | `tool_gate.py`                                           |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[MARS]`                                                 |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Integrity Enforcement**                                |
| **11. Catalyst**       | **Full 5-Point Audit**                                   |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this as the final gate check.
GVRN-SYNERGY-001, GOVERNS, This tool enforces the Hephaestus Gate quality standards.
TOOL-SENT-001, SYNERGY, Works with compliance_audit.py for multi-stage validation.

---
"""

import argparse
import json
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    from hephaestus.gate import HephaestusGate
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Execute Hephaestus Gate Audit")
    parser.add_argument("target", help="Path to artifact to audit")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        print(f"Error: File not found {args.target}")
        sys.exit(1)

    with open(args.target, "r", encoding="utf-8") as f:
        content = f.read()

    gate = HephaestusGate()
    report = gate.execute_gate(args.target, content)

    print(json.dumps(report, indent=2))

    if report["status"] == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
