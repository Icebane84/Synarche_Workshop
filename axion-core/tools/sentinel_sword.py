"""
artifact_anchor:
  id: INFR.SENTINEL_SWORD.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: INFRA
  celestial_class: STAR
  tier: COMPUTE
  state: ACTIVE
  ethos: SOVEREIGN_COMPUTE_COMPONENT
  relations: []
"""

"""
# TOOL-SENT-006: The Sentinel's Sword (Audit Engine).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-006`                                          |
| **2. Official Name**   | `sentinel_sword.py`                                      |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Entropy Purge**                                        |
| **11. Catalyst**       | **Auto-Fix**                                             |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for bulk remediation.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+15), Strength (+10)
# Passive Ability: The Unblinking Eye (Bulk Remediation)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: SWORD_FIX` | Global Python/TS Lint Fix | Automated Restoration |
| `⚡ EXECUTE: PURGE_ENTROPY` | Forced Alignment | Zero Entropy |
"""

# cspell:ignore INFR

import argparse
import logging
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- Constants ---
ROOT_DIR = Path(os.getcwd())
AXION_DIR = ROOT_DIR / "axion-core"
FORGE_DIR = ROOT_DIR / "nova_forge"
PLAYGROUND_DIR = ROOT_DIR / "Playground" / "tarot-forge"


def resolve_executable(cmd_name: str) -> str:
    """Resolves executable path, vital for Windows (npx -> npx.cmd).
    Checks PATH and PATHEXT logic via shutil.which.
    """
    path = shutil.which(cmd_name)
    if path:
        return path

    # Fallback for Windows if PATHEXT isn't perfect
    if platform.system() == "Windows" and not cmd_name.endswith((".cmd", ".exe")):
        path = shutil.which(f"{cmd_name}.cmd")
        if path:
            return path

    return cmd_name


def run_command(
    cmd: list[str], cwd: str | Path | None = None, description: str = "task"
) -> bool:
    """Executes a shell command safely, logs output, and returns True on success."""
    logger.info(f"\n--- [SENTINEL] Executing {description} ---")

    # Resolve the executable (e.g. npx -> npx.cmd) without mutating the input list
    resolved_cmd = cmd.copy()
    resolved_cmd[0] = resolve_executable(resolved_cmd[0])

    working_dir = cwd or os.getcwd()

    logger.info(f"Command: {' '.join(resolved_cmd)}")
    logger.info(f"Directory: {working_dir}")

    try:
        result = subprocess.run(
            resolved_cmd, cwd=working_dir, check=False, capture_output=True, text=True, encoding="utf-8"
        )

        stdout_text = result.stdout or ""
        stderr_text = result.stderr or ""

        if result.returncode == 0:
            logger.info(f"   > {description}: SUCCESS (Clean)")
            if stdout_text.strip():
                logger.info(f"[STDOUT]:\n{stdout_text.strip()}")
            return True
        else:
            logger.warning(
                f"   > {description}: COMPLETED (Exit Code: {result.returncode})"
            )
            if stdout_text.strip():
                logger.info(f"[STDOUT]:\n{stdout_text.strip()}")
            if stderr_text.strip():
                logger.info(f"[STDERR]:\n{stderr_text.strip()}")
            return False

    except FileNotFoundError:
        logger.error(f"   > [ERROR] Command not found: {resolved_cmd[0]}")
        return False
    except Exception as e:
        logger.exception(f"   > [ERROR] Failed to execute {description}: {e}")
        return False


def fix_python(target_dirs: list[str | Path]) -> bool:
    """Runs Ruff Auto-Fix on Python directories."""
    logger.info("\n=== PHASE 1: PYTHON TRANSMUTATION (Ruff) ===")

    # Check validity first
    ruff_exe = resolve_executable("ruff")
    if not shutil.which(ruff_exe):
        logger.warning("   > [WARNING] Ruff not found. Skipping Python fix.")
        logger.warning("   > Install via: pip install ruff")
        return True

    all_success = True
    for directory in target_dirs:
        target_path = Path(directory) if isinstance(directory, str) else directory

        if target_path.exists():
            success_fix = run_command(
                ["ruff", "check", "--fix", "."],
                cwd=target_path,
                description=f"Fixing Python in {target_path.name}",
            )
            success_fmt = run_command(
                ["ruff", "format", "."],
                cwd=target_path,
                description=f"Formatting Python in {target_path.name}",
            )
            if not success_fix or not success_fmt:
                all_success = False
        else:
            logger.warning(f"   > [SKIP] Directory not found: {target_path}")

    return all_success


def fix_typescript(target_dirs: list[str | Path]) -> bool:
    """Runs ESLint Auto-Fix on TS/JS directories."""
    logger.info("\n=== PHASE 2: TYPESCRIPT TRANSMUTATION (ESLint) ===")

    all_success = True
    for directory in target_dirs:
        target_path = Path(directory) if isinstance(directory, str) else directory

        if target_path.exists() and (target_path / "package.json").exists():
            if not (target_path / "node_modules").exists():
                logger.warning(
                    f"   > [WARNING] node_modules not found in {target_path.name}. Run 'npm install' first."
                )
                continue

            success = run_command(
                ["npx", "eslint", ".", "--fix"],
                cwd=target_path,
                description=f"Fixing TS/JS in {target_path.name}",
            )
            if not success:
                all_success = False
        else:
            logger.warning(
                f"   > [SKIP] Target not valid for TS Linting: {target_path}"
            )

    return all_success


def fix_markdown(target_dirs: list[str | Path]) -> bool:
    """
    Phase 3: Markdown Transmutation
    Executes Prettier to enforce consistent formatting across all Markdown files.
    """
    logger.info("\n=== PHASE 3: MARKDOWN TRANSMUTATION (Prettier) ===")
    
    npx_executable = resolve_executable("npx")
    if not npx_executable:
        logger.warning("   > [WARNING] 'npx' executable not found. Skipping Markdown formatting.")
        return True
        
    all_success = True
    for directory in target_dirs:
        target_path = Path(directory) if isinstance(directory, str) else directory

        if target_path.exists():
            md_files = list(target_path.rglob("*.md"))
            if not md_files:
                logger.info(f"   > Prettier: No markdown files found in {target_path.name}. Skipping.")
                continue

            success = run_command(
                ["npx", "prettier", "--write", "**/*.md"],
                cwd=target_path,
                description=f"Prettier (Markdown Formatting) in {target_path.name}",
            )
            if not success:
                all_success = False
        else:
            logger.warning(f"   > [SKIP] Directory not found: {target_path}")
            
    return all_success

def main() -> None:
    parser = argparse.ArgumentParser(description="Sentinel Auto-Fix Tool")
    parser.add_argument(
        "--scope", choices=["all", "python", "ts", "markdown"], default="all", help="Scope of fixes"
    )
    args = parser.parse_args()

    # Targets
    py_targets: list[str | Path] = [ROOT_DIR, AXION_DIR, FORGE_DIR]
    ts_targets: list[str | Path] = [PLAYGROUND_DIR, ROOT_DIR / "rosetta-stone-app"]
    md_targets: list[str | Path] = [ROOT_DIR, AXION_DIR, FORGE_DIR, PLAYGROUND_DIR, ROOT_DIR / "rosetta-stone-app"]

    overall_success = True

    if args.scope in ["all", "python"]:
        if not fix_python(py_targets):
            overall_success = False

    if args.scope in ["all", "ts"]:
        if not fix_typescript(ts_targets):
            overall_success = False

    if args.scope in ["all", "markdown"]:
        if not fix_markdown(md_targets):
            overall_success = False

    if overall_success:
        logger.info("\n[SENTINEL SWORD] Entropy Purge Complete. Zero Dissonance Detected.")
        sys.exit(0)
    else:
        logger.warning("\n[SENTINEL SWORD] Purge Completed with Errors. Review logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
