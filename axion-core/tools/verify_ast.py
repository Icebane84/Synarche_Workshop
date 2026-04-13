"""
# TOOL-SENT-008: Header Hierarchy Validator (Audit Engine)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-008`                                          |
| **2. Official Name**   | `verify_ast.py`                                          |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Hierarchy Verification**                               |
| **11. Catalyst**       | **AST Scan**                                             |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for hierarchy verification.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+10), Perceptivity (+15)
# Passive Ability: Structural Scan (Hierarchy Validation)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: VERIFY_AST` | Scan Markdown Headers | Structural Integrity |
| `⚡ EXECUTE: AST_CHECK` | Fast Hierarchy Scan | Coherence Maintenance |
"""

import argparse
import os
import sys
from typing import List, Optional, Tuple


def verify_ast(filepath: str) -> bool:
    """
    Checks the header hierarchy of a markdown file.
    """
    print(f"\n[VERIFY_AST] Target: {filepath}")

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Read Error: {e}")
        return False

    print("\n--- Abstract Syntax Tree (Headers) ---\n")

    headers: List[Tuple[int, str, int]] = []
    in_code_block = False

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        stripped = line.strip()
        if stripped.startswith("#"):
            level = 0
            for char in stripped:
                if char == "#":
                    level += 1
                else:
                    break

            title = stripped[level:].strip()
            headers.append((level, title, i + 1))

            indent = "  " * (level - 1)
            print(f"{indent}H{level}: {title} (L{i + 1})")

    print("\n--------------------------------------")

    if not headers:
        print("❌ [FAIL] No headers found. Flat structure?")
        return False

    root_level = headers[0][0]

    # Standard v11.0 skips the H6 metadata block check if it's there
    if root_level == 6 and (
        "Universal Identification" in headers[0][1]
        or "Universal Identification" in "".join([h[1] for h in headers[:3]])
    ):
        print("ℹ️  [INFO] Detected v11.0 Metadata Header (H6). Skipping root H1 check.")
        real_h1 = next((h for h in headers if h[0] == 1), None)
        if not real_h1:
            print("❌ [FAIL] Standard requires a Title H1 after metadata. None found.")
    elif root_level != 1:
        print(f"⚠️  [WARN] Document should start with H1 (after possible H6), found H{root_level}.")

    issues = 0
    prev_level = 0
    for lvl, title, ln in headers:
        if prev_level == 6 and lvl == 1:
            pass
        elif lvl > prev_level + 1 and prev_level != 0:
            print(f"❌ [FAIL] Hierarchy Jump: H{prev_level} -> H{lvl} at Line {ln}.")
            issues += 1
        prev_level = lvl

    if issues == 0:
        print("✅ [PASS] Structural Hierarchy is Sound.")
        return True
    else:
        print(f"❌ [FAIL] Found {issues} hierarchy issues.")
        return False


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(description="Verify Markdown Header Hierarchy.")
    parser.add_argument("--target", required=True, help="Path to the markdown file.")
    args = parser.parse_args()

    success = verify_ast(args.target)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
