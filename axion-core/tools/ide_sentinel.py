"""
# TOOL-SENT-002: The IDE Integrity Sentinel (Audit Engine)

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-002`                                          |
| **2. Official Name**   | `ide_sentinel.py`                                        |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Environment Integrity**                                |
| **11. Catalyst**       | **Config Enforcement**                                   |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for IDE integrity.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+10), Automation (+15)
# Passive Ability: The Unblinking Eye (Config Enforcement)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: AUDIT_IDE` | VS Code Config Scan | Workspace Alignment |
| `⚡ EXECUTE: ALIGN_IDE` | Repair Local Entropy | Developer Experience |
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- PHOENIX STANDARDS DEFINITION ---
RUFF_EXTENSION = "charliermarsh.ruff"
PYTHON_SECTION = "[python]"
KEY_DEFAULT_FORMATTER = "editor.defaultFormatter"
KEY_CODE_ACTIONS = "editor.codeActionsOnSave"

REQUIRED_EXTENSIONS = [
    RUFF_EXTENSION  # The Synergy Link to 'uv'
]

REQUIRED_SETTINGS = {
    "editor.formatOnSave": True,
    KEY_DEFAULT_FORMATTER: RUFF_EXTENSION,
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",  # Enforces 'uv' venv (Windows)
    "markdownlint.configFile": "axion-core/standards/markdownlint.json",  # Sophia's Law
    PYTHON_SECTION: {KEY_DEFAULT_FORMATTER: RUFF_EXTENSION},
    "[markdown]": {
        KEY_DEFAULT_FORMATTER: "DavidAnson.vscode-markdownlint",
        "editor.tabSize": 2,
        "editor.insertSpaces": True,
        KEY_CODE_ACTIONS: {
            "source.fixAll.markdownlint": "always",
            "source.organizeImports": "never",
        },
    },
}

REQUIRED_CODE_ACTIONS = {"source.organizeImports": "always"}

# --- UTILITY FUNCTIONS ---


def load_json(path: Path) -> dict[str, Any]:
    """Safely loads a JSON file, returning empty dict if missing."""
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            # Handle comments in JSON (common in VSCode) by simple skipping if strict json fails
            # For this script, we assume standard JSON or empty.
            return json.load(f)
    except json.JSONDecodeError:
        logger.exception(f"[!] CRITICAL: {path} is corrupted or contains invalid JSON.")
        return {}


def save_json(path: Path, data: dict[str, Any]) -> None:
    """Writes JSON data to file with indentation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# --- AUDIT LOGIC ---


def audit_extensions(vscode_dir: Path, fix: bool) -> list[str]:
    """Checks extensions.json for required tools."""
    ext_path = vscode_dir / "extensions.json"
    data = load_json(ext_path)
    recommendations = data.get("recommendations", [])

    issues = []
    modified = False

    for ext in REQUIRED_EXTENSIONS:
        if ext not in recommendations:
            issues.append(f"[MISSING EXTENSION] {ext}")
            if fix:
                recommendations.append(ext)
                modified = True

    if fix and modified:
        data["recommendations"] = recommendations
        save_json(ext_path, data)
        logger.info(f"[+] FIXED: Added missing extensions to {ext_path}")

    return issues


def _audit_top_level_settings(data: dict[str, Any], fix: bool) -> tuple[list[str], bool]:
    """Audits top-level settings in settings.json."""
    issues = []
    modified = False

    # Prune deprecated keys
    if "markdownlint.config" in data:
        issues.append("[DEPRECATED KEY] markdownlint.config found")
        if fix:
            del data["markdownlint.config"]
            modified = True

    for key, value in REQUIRED_SETTINGS.items():
        if key == PYTHON_SECTION:
            continue  # Handle nested separately

        if data.get(key) != value:
            issues.append(f"[BAD SETTING] {key} is not '{value}'")
            if fix:
                data[key] = value
                modified = True

    return issues, modified


def _audit_python_overrides(data: dict[str, Any], fix: bool) -> tuple[list[str], bool]:
    """Audits [python] section in settings.json."""
    issues = []
    modified = False

    if PYTHON_SECTION not in data and fix:
        data[PYTHON_SECTION] = {}
        modified = True

    # Re-check presence after potential creation
    if PYTHON_SECTION in data:
        py_block = data[PYTHON_SECTION]
        target_block = REQUIRED_SETTINGS[PYTHON_SECTION]

        if isinstance(target_block, dict):
            for k, v in target_block.items():
                if py_block.get(k) != v:
                    issues.append(f"[BAD SETTING] {PYTHON_SECTION}.{k} is not '{v}'")
                    if fix:
                        py_block[k] = v
                        modified = True
            data[PYTHON_SECTION] = py_block

    return issues, modified


def _audit_code_actions(data: dict[str, Any], fix: bool) -> tuple[list[str], bool]:
    """Audits editor.codeActionsOnSave in settings.json."""
    issues = []
    modified = False

    code_actions = data.get(KEY_CODE_ACTIONS, {})

    if isinstance(code_actions, list):
        issues.append(f"[BAD FORMAT] {KEY_CODE_ACTIONS} should be a dictionary")
        if fix:
            code_actions = {}
            modified = True

    if isinstance(code_actions, dict):
        for action, status in REQUIRED_CODE_ACTIONS.items():
            if code_actions.get(action) != status:
                issues.append(f"[BAD ACTION] {action} is not active on save")
                if fix:
                    code_actions[action] = status
                    modified = True
        data[KEY_CODE_ACTIONS] = code_actions

    return issues, modified


def audit_settings(vscode_dir: Path, fix: bool) -> list[str]:
    """Checks settings.json for behavioral compliance."""
    settings_path = vscode_dir / "settings.json"
    data = load_json(settings_path)

    issues = []
    any_modified = False

    # 1. Check Top-Level Settings
    top_issues, top_mod = _audit_top_level_settings(data, fix)
    issues.extend(top_issues)
    any_modified = any_modified or top_mod

    # 2. Check Python Specific Overrides
    py_issues, py_mod = _audit_python_overrides(data, fix)
    issues.extend(py_issues)
    any_modified = any_modified or py_mod

    # 3. Check Code Actions
    ca_issues, ca_mod = _audit_code_actions(data, fix)
    issues.extend(ca_issues)
    any_modified = any_modified or ca_mod

    if fix and any_modified:
        save_json(settings_path, data)
        logger.info(f"[+] FIXED: aligned settings in {settings_path}")

    return issues


# --- MAIN CONTROLLER ---


def main() -> None:
    parser = argparse.ArgumentParser(description="Phoenix Protocol: IDE Integrity Sentinel")
    parser.add_argument("--fix", action="store_true", help="Automatically repair configuration drift.")
    parser.add_argument("--strict", action="store_true", help="Exit with error code if issues found (for CI/CD).")
    args = parser.parse_args()

    # Define Scope
    cwd = Path(os.getcwd())
    vscode_dir = cwd / ".vscode"

    logger.info(f"// INITIATING SCAN: {cwd}")

    if not vscode_dir.exists():
        logger.warning(f"[!] WARNING: No .vscode directory found in {cwd}.")
        if args.fix:
            logger.info("[+] CREATING .vscode directory...")
            vscode_dir.mkdir()
        else:
            logger.info("[-] Use --fix to initialize Phoenix Environment.")
            sys.exit(1)

    # Execute Audits
    ext_issues = audit_extensions(vscode_dir, args.fix)
    set_issues = audit_settings(vscode_dir, args.fix)

    all_issues = ext_issues + set_issues

    # Reporting
    if not all_issues:
        logger.info("\n>> SYSTEM STATUS: COHERENT [OK]")
        sys.exit(0)
    else:
        logger.info("\n>> SYSTEM STATUS: ENTROPY DETECTED")
        for issue in all_issues:
            logger.info(f"   - {issue}")

        if args.fix:
            logger.info("\n>> REMEDIATION COMPLETE. RESTART VS CODE.")
            sys.exit(0)
        else:
            logger.info("\n>> RECOMMENDATION: Run with --fix to align.")
            if args.strict:
                sys.exit(1)


if __name__ == "__main__":
    main()
