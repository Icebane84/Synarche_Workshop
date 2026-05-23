"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-ARMORY-AUDIT-001`        | The Sovereign ID. |
| **Official Name** | `armory_audit.py`              | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                   | Creation Date.    |.
"""

import json
from pathlib import Path

# Configuration
WORKSPACE_ROOT = Path(r"c:\Users\Chris\Synarche_Workspace")
TOOLS_DIR = WORKSPACE_ROOT / "axion-core" / "tools"
HEPHAESTUS_DIR = WORKSPACE_ROOT / "axion-core" / "src" / "hephaestus"

# 41 Tools listed in CHAR-AXION-001
ARMORY_TOOLS = [
    # 1. The Magician
    "ingest_vault",
    "extract_docx_text",
    "tool_gaze",
    # 2. The Emperor
    "reforge_library",
    "standardize_docs",
    "scaffold_engine",
    "apply_rpg_header",
    "apply_standard",
    # 3. The High Priestess
    "forge_backlinks",
    "sophia_wisdom",
    "generate_registry",
    "find_unlinked",
    "resonance_scanner",
    "catalyst_weaver",
    "tool_navigator",
    "query_csl",
    "reflect_memory",
    # 4. The Knight of Swords
    "reforge",
    "knight_fixer",
    "reforge_oslm",
    "transmutation_pipeline",
    # 5. The Star
    "test_weaver",
    "generate_rag_graph",
    "chronicle_manager",
    "log_refactor_milestone",
    # 6. The King of Pentacles
    "map_markdown_structure",
    "generate_prs",
    "log_synthesis",
    "sentinel",
    "ide_sentinel",
    "lint_artifact",
    "analyze_docs_compliance",
    "diagnose_paths",
    "sentinel_sword",
    "gaze",
    "verify_ast",
    "audit_weights",
    "soul",
    "tool_gate",
    "tool_crf",
    "tool_auditor",
]


def audit_armory():
    report = {"verified": [], "missing": [], "discrepancies": []}

    if not TOOLS_DIR.exists():
        print(f"Error: Tools directory not found: {TOOLS_DIR}")
        return

    # Get all actual files in tools dir
    actual_files = list(TOOLS_DIR.glob("*")) + list(HEPHAESTUS_DIR.glob("*"))
    actual_names = [f.name for f in actual_files]

    for tool in ARMORY_TOOLS:
        py_name = f"{tool}.py"
        js_name = f"{tool}.js"

        found = False
        if py_name in actual_names:
            report["verified"].append({"tool": tool, "file": py_name, "type": "py"})
            found = True
        elif js_name in actual_names:
            report["verified"].append({"tool": tool, "file": js_name, "type": "js"})
            found = True
        else:
            # Check for suffixes like (1), (2)
            candidates = []
            for f_name in actual_names:
                if f_name.startswith(tool) and "(" in f_name:
                    candidates.append(f_name)

            if candidates:
                # Pick the latest or one of them
                best_match = sorted(candidates)[-1]
                report["discrepancies"].append(
                    {
                        "tool": tool,
                        "found_as": best_match,
                        "suggestion": f"Rename {best_match} to {tool}.py",
                    }
                )
                found = True

        if not found:
            report["missing"].append(tool)

    # Print clean report
    print("--- ARMORY AUDIT RESULTS ---")
    print(f"Verified: {len(report['verified'])}")
    print(f"Discrepancies: {len(report['discrepancies'])}")
    print(f"Missing: {len(report['missing'])}\n")

    if report["discrepancies"]:
        print("DISCREPANCIES:")
        for d in report["discrepancies"]:
            print(f"  {d['tool']} -> Found as {d['found_as']}")

    if report["missing"]:
        print("\nMISSING:")
        for m in report["missing"]:
            print(f"  {m}")

    # Final JSON for easy parsing by agent
    json_path = WORKSPACE_ROOT / "axion-core" / "tools" / "audit_results.json"
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nAudit results saved to: {json_path}")

    print("\n--- JSON_REPORT_START ---")
    print(json.dumps(report, indent=2))
    print("--- JSON_REPORT_END ---")


if __name__ == "__main__":
    audit_armory()
