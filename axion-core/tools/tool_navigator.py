#!/usr/bin/env python3
"""
# TOOL-NAV-001: OSLM Navigator CLI (Matrix Synchronization)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-NAV-001`                                           |
| **2. Official Name**   | `tool_navigator.py`                                      |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Architectural Discovery**                              |
| **11. Catalyst**       | **Navigation Scan**                                      |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this for navigation.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---
"""

import argparse
import json
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
    from hephaestus.oslm_gps import DEFAULT_OSLM_PATH, OSLMGPS
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Navigate OSLM Graph")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: neighbors
    p_neighbors = subparsers.add_parser("neighbors", help="Find connected nodes")
    p_neighbors.add_argument("node", help="Artifact ID")

    # Command: path
    p_path = subparsers.add_parser("path", help="Find path between nodes")
    p_path.add_argument("start", help="Start Artifact ID")
    p_path.add_argument("end", help="End Artifact ID")

    # Command: list
    subparsers.add_parser("list", help="List all nodes")

    parser.add_argument("--oslm", help="Path to OSLM file", default=DEFAULT_OSLM_PATH)

    args = parser.parse_args()

    gps = OSLMGPS(oslm_path=args.oslm)

    if args.command == "neighbors":
        links = gps.traverse_links(args.node)
        print(json.dumps(links, indent=2))

    elif args.command == "path":
        path = gps.find_path(args.start, args.end)
        if path:
            print(f"Path found: {' -> '.join(path)}")
        else:
            print("No path found.")

    elif args.command == "list":
        nodes = gps.get_all_nodes()
        print(json.dumps(nodes, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
