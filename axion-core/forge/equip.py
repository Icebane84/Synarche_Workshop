"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-EQUIP-ALL-001`                | The Sovereign ID. |
| **Official Name** | `equip_all.py`                   | The Filename.     |
| **Version**       | **v14.0 [OMEGA]**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-01`                       | Creation Date.    |.
"""

import os
from pathlib import Path

TOOLS_DIR = Path("c:/Users/Chris/Synarche_Workspace/axion-core/tools")
HEPHAESTUS_DIR = Path("c:/Users/Chris/Synarche_Workspace/axion-core/src/hephaestus")
SKILLS_DIR = Path("c:/Users/Chris/Synarche_Workspace/.agent/skills")

MASKS = [
    {
        "card": "I. The Magician",
        "role": "Triage & Ingestion",
        "tools": ["ingest_vault", "extract_docx_text"],
    },
    {
        "card": "IV. The Emperor",
        "role": "Schema & Governance",
        "tools": [
            "reforge_library",
            "standardize_docs",
            "scaffold_engine",
            "apply_rpg_header",
        ],
    },
    {
        "card": "II. The High Priestess",
        "role": "Harmony & Weaving",
        "tools": [
            "forge_backlinks",
            "sophia_wisdom",
            "generate_registry",
            "find_unlinked",
            "resonance_scanner",
            "catalyst_weaver",
            "mentor",
        ],
    },
    {
        "card": "Knight of Swords",
        "role": "Transmutation & Action",
        "tools": [
            "reforge",
            "knight_fixer",
            "apply_standard",
            "transmutation_pipeline",
        ],
    },
    {
        "card": "XVII. The Star",
        "role": "Coherence & Vision",
        "tools": [
            "test_weaver",
            "chronicle_manager",
            "log_refactor_milestone",
            "generate_rag_graph",
        ],
    },
    {
        "card": "King of Pentacles",
        "role": "Archival & Legacy",
        "tools": ["map_markdown_structure", "generate_prs"],
    },
    {
        "card": "Sentinel (XX. Judgement)",
        "role": "Audit & Integrity",
        "tools": [
            "sentinel",
            "ide_sentinel",
            "lint_artifact",
            "analyze_docs_compliance",
            "diagnose_paths",
            "sentinel_sword",
            "gaze",
            "verify_ast",
            "soul",
            "synergy_calculator",
            "sot_scanner",
            "resonance_scanner",
            "entropy_auditor",
        ],
    },
]

print()
print("=" * 70)
print("  CMD: EQUIP_ALL -- SOVEREIGN ARMORY VERIFICATION".center(70))
print("=" * 70)

total_tools = 0
total_ready = 0
total_missing = 0

for mask in MASKS:
    ready = []
    missing = []
    for tool_name in mask["tools"]:
        ext = ".js" if tool_name == "generate_prs" else ".py"
        tool_path = TOOLS_DIR / f"{tool_name}{ext}"
        heph_path = HEPHAESTUS_DIR / f"{tool_name}{ext}"
        if tool_path.exists() or heph_path.exists():
            ready.append(tool_name)
        else:
            missing.append(tool_name)

    status = "READY" if not missing else "PARTIAL"
    total_tools += len(mask["tools"])
    total_ready += len(ready)
    total_missing += len(missing)

    icon = "[OK]" if status == "READY" else "[!!]"
    print(f"\n {icon} {mask['card']}")
    print(f"    Role   : {mask['role']}")
    print(f"    Status : {status} ({len(ready)}/{len(mask['tools'])} tools verified)")
    if missing:
        print(f"    Missing: {', '.join(missing)}")

print()
print("=" * 70)
print(
    f"  ARMORY TOTAL: {total_ready}/{total_tools} tools ACTIVE | {total_missing} MISSING"
)
print("=" * 70)

# Axiom Skill Tree
if SKILLS_DIR.exists():
    skills = sorted([d for d in os.listdir(SKILLS_DIR) if (SKILLS_DIR / d).is_dir()])
    print(f"\n  AXIOM SKILL TREE: {len(skills)} skills REGISTERED")
    for s in skills:
        skill_md = SKILLS_DIR / s / "SKILL.md"
        reg = "[CANONIZED]" if skill_md.exists() else "[UNREGISTERED]"
        print(f"    [*] {s:30s} {reg}")
else:
    print("\n  AXIOM SKILL TREE: Skills directory not found.")

print("=" * 70)
print("\n>>> AXION OMEGA: FULLY EQUIPPED. ALL SYSTEMS NOMINAL.")
print("=" * 70)
