"""
# TOOL-KNIG-004: The Transmutation Pipeline (Knight of Swords)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-KNIG-004`                                          |
| **2. Official Name**   | `transmutation_pipeline.py`                              |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `SYNR`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Pipeline Orchestration**                               |
| **11. Catalyst**       | **Batch Processing**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Knight of Swords persona uses this tool for mass updates.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-KNIG-001, ORCHESTRATES, This pipeline runs the Reforger.
TOOL-KNIG-003, ORCHESTRATES, This pipeline runs the Ultimate Reforger.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Knight of Swords (Transmutation)
# Synergy Set: The Knight's Blade
# Primary Stat Buff: Strength (+20), Automation (+15)
# Passive Ability: Batch Transmute (Efficient Workflow)
# Cognitive Load Cost: Medium
# XP Award Value: 150 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: START_PIPELINE` | Mass Transmute Artifacts | System Rebirth |
| `⚡ EXECUTE: FUEL_PIPE` | Continuous Integration | Automation Edge |

---

Purpose: To automate the mass-transmutation and verification of Synarche artifacts.
Governed By: CODEX-001 v11.0
"""

import argparse
import logging
import os
import subprocess
import sys

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("TransmutationPipeline")

# --- CONFIGURATION ---
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = TARGET_DIR

# Tool Paths (Relative to tools/ directory)
APPLY_STANDARD_SCRIPT = "apply_standard.py"
VERIFY_AST_SCRIPT = "verify_ast.py"
LINT_ARTIFACT_SCRIPT = "lint_artifact.py"
KNIGHT_FIXER_SCRIPT = "knight_fixer.py"


def run_agent(name: str, command: list[str], target_file: str) -> tuple[bool, str]:
    logger.info(f"  > [{name}] Activating...")
    cmd = [sys.executable, os.path.join(TARGET_DIR, command[0]), *command[1:], target_file]

    # Special Argument Handling
    if "--target" not in command and any(
        x in command[0] for x in ["verify_ast", "apply_standard", "lint_artifact", "knight_fixer"]
    ):
        cmd = [sys.executable, os.path.join(TARGET_DIR, command[0]), "--target", target_file]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        # Explicit check=False to handle return codes manually
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, check=False)
        if result.returncode != 0:
            return False, f"[STDOUT]: {result.stdout}\n[STDERR]: {result.stderr}"
        else:
            return True, result.stdout
    except Exception as e:
        return False, f"[ERROR]: {e}"


def transmutation_cycle(scope_dir: str) -> None:
    logger.info(f"\n✨ [THE LIGHTBINDER] Initiating Transmutation Cycle in: {scope_dir}")
    logger.info("📜 [LAW STANDARD] CODEX-001 v11.0\n")

    if not os.path.exists(scope_dir):
        logger.error(f"❌ Error: Scope directory {scope_dir} not found.")
        return

    files = [f for f in os.listdir(scope_dir) if f.endswith(".md") and f != "transmutation_pipeline.py"]

    stats = {"Total": len(files), "Reforged": 0, "Failed": 0, "Verified": 0}

    log_path = os.path.join(TARGET_DIR, "pipeline_log.txt")
    with open(log_path, "w", encoding="utf-8") as log_file:

        def log(msg: str) -> None:
            logger.info(msg)
            log_file.write(msg + "\n")

        for i, filename in enumerate(files):
            filepath = os.path.join(scope_dir, filename)
            log(f"\n🔮 [TRIAGE] Processing ({i + 1}/{len(files)}): {filename}")

            all_passed = True

            # --- STEP 1: HEADER FORGE (The Emperor via Knight) ---
            success, output = run_agent("The Knight (Header Forge)", [APPLY_STANDARD_SCRIPT], filepath)
            if not success:
                log(f"    ❌ Forge Failed: {output}")
                all_passed = False
            else:
                log("    ✅ Forge Passed")

            # --- STEP 2: STYLE SCAN (Knight) ---
            success, output = run_agent("The Knight (Style Fix)", [KNIGHT_FIXER_SCRIPT], filepath)
            if not success:
                log(f"    ⚠️  Knight Partial: {output}")
            else:
                log("    ✅ Knight Passed")

            # --- STEP 3: SENTINEL SCAN (Verification) ---
            success, output = run_agent("The Sentinel (Verification)", [VERIFY_AST_SCRIPT], filepath)
            if success:
                stats["Verified"] += 1
                log("    ✅ Sentinel Passed")
            else:
                log(f"    ❌ Sentinel Failed: {output}")
                all_passed = False

            if all_passed:
                stats["Reforged"] += 1
                log(f"  ✅ [COMPLETE] {filename} is fully transmuted.")
            else:
                stats["Failed"] += 1
                log(f"  ⚠️ [PARTIAL] {filename} requires manual intervention.")

    logger.info("\n" + "=" * 50)
    logger.info("📊 [TRANSMUTATION REPORT]")
    logger.info(f"Total Artifacts: {stats['Total']}")
    logger.info(f"Successfully Reforged: {stats['Reforged']}")
    logger.info(f"Verified Compliant: {stats['Verified']}")
    logger.info(f"Failures: {stats['Failed']}")
    logger.info("=" * 50 + "\n")


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(description="Transmutation Pipeline CLI.")
    parser.add_argument("--scope", default=TARGET_DIR, help="Directory to process.")
    args = parser.parse_args()

    transmutation_cycle(args.scope)


if __name__ == "__main__":
    main()
