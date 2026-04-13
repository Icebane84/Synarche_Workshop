#!/usr/bin/env python3
"""
# TOOL-GVRN-002: Matrix Initializer (Matrix Synchronization)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-GVRN-002`                                          |
| **2. Official Name**   | `initialize_matrix.py`                                   |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Systemic Activation**                                  |
| **11. Catalyst**       | **Matrix Initialization**                                |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess/Emperor layer uses this for activation.
GVRN-SYNERGY-001, GOVERNS, This tool defines the operational Matrix.
UMB-SOT-001, PROTOCOL, Follows the Synergistic Opportunity Tracker.

---
"""

import os
import sys

try:
    from enums import TarotShard
except ImportError:
    # If running from root without package structure
    sys.path.append(os.path.dirname(__file__))
    from enums import TarotShard

# The Synergy Matrix Definition (GVRN-SYNERGY-001)
MATRIX = {
    TarotShard.MAGICIAN: [
        "ingest_vault.py",
        "extract_docx_text.py",
        "tool_gaze.py",
    ],
    TarotShard.EMPEROR: [
        "reforge_library.py",
        "standardize_docs.py",
        "scaffold_engine.py",
        "apply_rpg_header.py",
        "apply_standard.py",
    ],
    TarotShard.PRIESTESS: [
        "forge_backlinks.py",
        "sophia_wisdom.py",
        "generate_registry.py",
        "find_unlinked.py",
        "resonance_scanner.py",
        "catalyst_weaver.py",
        "tool_navigator.py",
        "query_csl.py",
        "reflect_memory.py",
    ],
    TarotShard.KNIGHT_OF_SWORDS: [
        "reforge.py",
        "knight_fixer.py",
        "reforge_oslm.py",
        "transmutation_pipeline.py",
    ],
    TarotShard.STAR: [
        "test_weaver.py",
        "generate_rag_graph.py",
        "chronicle_manager.py",
        "log_refactor_milestone.py",
    ],
    TarotShard.KING_OF_PENTACLES: [
        "map_markdown_structure.py",
        "generate_prs.js",
        "log_synthesis.py",
    ],
    TarotShard.JUDGEMENT: [
        "compliance_audit.py",
        "ide_sentinel.py",
        "lint_artifact.py",
        "analyze_docs_compliance.py",
        "diagnose_paths.py",
        "sentinel_sword.py",
        "impact_analysis.py",
        "verify_ast.py",
        "audit_weights.py",
        "assess_elegance.py",
        "tool_gate.py",
        "tool_crf.py",
        "tool_auditor.py",
    ],
}


def check_tools(tools_dir: str):
    print("\n🔮 INITIALIZING SEVEN-AGENT MATRIX...\n")

    total_tools = 0
    found_tools = 0

    for shard, tool_list in MATRIX.items():
        print(f"🔹 ACTIVATING: {shard.name} ({shard.value})")
        active = True
        for tool in tool_list:
            total_tools += 1
            # Check for .py or .js
            # Some tool names might be slightly different in file system or placeholders
            # We assume exact match for now based on GVRN-SYNERGY-001

            tool_path = os.path.join(tools_dir, tool)
            # Handle potential js files or just check basename match flexibility if needed
            # For now, simplistic check

            if os.path.exists(tool_path):
                found_tools += 1
                # print(f"  [OK] {tool}")
            else:
                # Try simple fuzzy match (e.g. without extension if logic changes, but definitions have ext)
                print(f"  ❌ [MISSING] {tool}")
                active = False

        if active:
            print(f"  ✅ STATUS: ONLINE")
        else:
            print(f"  ⚠️ STATUS: DEGRADED (Missing Tools)")
        print("")

    print("------------------------------------------------")
    print(f"matrix_integrity: {found_tools}/{total_tools} tools online.")

    if found_tools == total_tools:
        print("\n✨ SYSTEM STATE: SYNERGY ACHIEVED.")
    else:
        print("\n⚠️ SYSTEM STATE: PARTIAL FUNCTIONALITY.")


def main():
    # Assume script is run from project root, tools in axion-core/tools
    # Adjust path strategy if needed
    base_dir = os.getcwd()
    tools_dir = os.path.join(base_dir, "axion-core", "tools")

    if not os.path.exists(tools_dir):
        print(f"Error: Tools directory not found at {tools_dir}")
        return

    check_tools(tools_dir)


if __name__ == "__main__":
    main()
