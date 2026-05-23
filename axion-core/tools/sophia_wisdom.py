"""# TOOL-HPRI-002: Sophia's Wisdom (The Synarche Auditor).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-002`                                          |
| **2. Official Name**   | `sophia_wisdom.py`                                       |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Wisdom**                                               |
| **11. Catalyst**       | **Insight Generation**                                   |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The High Priestess persona uses this tool for wisdom.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: High Harmony (The High Priestess)
# Synergy Set: The Priestess's Veil
# Primary Stat Buff: Intuition (+20), Wisdom (+15)
# Passive Ability: Sophia's Eye (Anomaly Detection)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: SOPHIA_AUDIT` | Run Complexity & Governance Scan | Quality Assurance |
| `⚡ EXECUTE: FIX_ALL` | Auto-Repair Dissonance | Restoration of Order |
"""

import argparse
import json
import logging
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- Constants ---
DEFAULT_THRESHOLD = 10
VALID_EVOLUTION_DOMAINS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
    "Phoenix Form",
]
CRITICAL_COMPLEXITY_THRESHOLD = 15
INDENT_WARNING_THRESHOLD = 5
MAX_COMPLIANCE_SCORE = 100
UIP_HEADER_TEXT = "Universal Identification & Provenance"


def resolve_executable(cmd_name: str) -> str:
    """Resolves executable path, vital for Windows.
    Matches the robust logic from Sentinel Sword.
    """
    path = shutil.which(cmd_name)
    if path:
        return path

    if platform.system() == "Windows" and not cmd_name.endswith((".cmd", ".exe")):
        path = shutil.which(f"{cmd_name}.cmd")
        if path:
            return path
    return cmd_name


# --- COMPLEXITY ENGINE ---


def scan_code_complexity(target_dir: str) -> list[dict[str, Any]]:
    """Runs ruff to find C901 violations."""
    logger.info(
        f"\n--- [SOPHIA] Scanning {target_dir} for Cognitive Dissonance (C901) ---"
    )

    ruff_cmd = resolve_executable("ruff")
    if not shutil.which(ruff_cmd):
        logger.error("[ERROR] Ruff not found. Please install it (pip install ruff).")
        return []

    cmd = [ruff_cmd, "check", target_dir, "--select", "C901", "--output-format", "json"]

    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        raw_json = result.stdout
        if not raw_json.strip():
            return []
        return json.loads(raw_json)
    except Exception:
        logger.exception("[ERROR] Scan failed")
        return []


def report_complexity(violations: list[dict[str, Any]]) -> None:
    if not violations:
        logger.info("\n✅ [RESULT] Clarity Absolute. No cognitive hotspots detected.")
        return

    hotspots = []
    for v in violations:
        msg = v.get("message", "")
        filename = v.get("filename", "unknown")
        line = v.get("location", {}).get("row", "?")
        score = 0
        try:
            nums = re.findall(r"\d+", msg)
            if nums:
                # Heuristic: usually the larger number or specifically positioned
                score = int(nums[-1] if len(nums) == 1 else nums[-2])
        except Exception:
            pass
        if score > 0:
            hotspots.append(
                {"file": filename, "line": line, "msg": msg, "score": score}
            )

    hotspots.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"\n[SOPHIA] Detected {len(hotspots)} Cognitive Hotspots.")
    logger.info("=" * 60)
    for idx, spot in enumerate(hotspots):
        f_name = Path(spot["file"]).name
        logger.info(f"{idx + 1}. {f_name}:{spot['line']} (Score: {spot['score']})")
        if spot["score"] > CRITICAL_COMPLEXITY_THRESHOLD:
            logger.warning("   Wisdom: CRITICAL. Decompose immediately.")
    logger.info("-" * 60)


# --- GOVERNANCE ENGINE ---


def check_file_governance(filepath: str) -> list[str]:
    """Checks a single file for OGLN v10 standards."""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        content = "".join(lines)
    except Exception as e:
        return [f"[ERROR] Read failure: {e}"]

    issues = []
    issues.extend(_check_uip_header(content, lines))
    # issues.extend(_check_agp_block(content)) # Deprecated in v10? Checking for Artifact Block instead
    issues.extend(_check_artifact_block(content))
    issues.extend(_check_prompt_packet(content))
    issues.extend(_check_indentation(lines))
    return issues


def _check_uip_header(content: str, lines: list[str]) -> list[str]:
    issues = []
    if UIP_HEADER_TEXT not in content:
        issues.append(f"[CRITICAL] Missing UIP Header ({UIP_HEADER_TEXT}).")
        return issues  # Abort deeper checks if header missing

    # Evolution Domain Check
    evo_valid = False
    for line in lines[:60]:
        if (
            "Evolution" in line
            and "|" in line
            and any(domain in line for domain in VALID_EVOLUTION_DOMAINS)
        ):
            evo_valid = True
            break

    if not evo_valid:
        issues.append("[CRITICAL] Invalid or Missing 'Evolution' Domain in UIP.")
    return issues


def _check_artifact_block(content: str) -> list[str]:
    """Checks for [ARTIFACT START] and [ARTIFACT END] blocks."""
    if "[ARTIFACT START]" not in content:
        return ["[CRITICAL] Missing [ARTIFACT START] marker."]
    if "[ARTIFACT END]" not in content:
        return ["[CRITICAL] Missing [ARTIFACT END] marker."]
    return []


def _check_prompt_packet(content: str) -> list[str]:
    """Checks for APP presence."""
    if "Actionable Prompt Packet" not in content and "CMD:" not in content:
        return ["[CRITICAL] Missing Actionable Prompt Packet / CMDs."]
    return []


def _check_indentation(lines: list[str]) -> list[str]:
    suspicious_indent = 0
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        # Check for 2-space indentation where 4 is expected (approximate heuristic)
        if re.match(r"^ {2}[-*]", line):
            suspicious_indent += 1

    if suspicious_indent > INDENT_WARNING_THRESHOLD:
        return [
            f"[WARNING] Detected {suspicious_indent} lines with 2-space indentation (PGPS mandates 4)."
        ]
    return []


def _find_markdown_targets(target: str) -> list[str]:
    if os.path.isdir(target):
        targets = []
        for root, _, files in os.walk(target):
            for f in files:
                if f.endswith(".md"):
                    targets.append(os.path.join(root, f))
        return targets
    elif target.endswith(".md"):
        return [target]
    return []


def scan_governance(target: str) -> None:
    """Scans .md files in target for compliance."""
    logger.info(
        f"\n--- [SOPHIA] Scanning {target} for Governance Compliance (OGLN v10) ---"
    )

    targets = _find_markdown_targets(target)
    if not targets:
        logger.info("[INFO] No Markdown artifacts found to audit.")
        return

    compliance_score = MAX_COMPLIANCE_SCORE
    for t in targets:
        issues = check_file_governance(t)
        if issues:
            logger.info(f"\n📄 {os.path.basename(t)}")
            for i in issues:
                logger.info(f"   {i}")
                if "[CRITICAL]" in i:
                    compliance_score -= 10
                else:
                    compliance_score -= 1

    if compliance_score < MAX_COMPLIANCE_SCORE:
        base_score = max(0, compliance_score)
        logger.info(f"\n[RESULT] Governance Integrity: {base_score}%")
        logger.info(
            "Action: Run 'reforge.py' or 'lint_artifact.py' logic on failing artifacts."
        )
    else:
        logger.info("\n✅ [RESULT] Governance Integrity: 100%. The Law is Upheld.")


# --- MAIN ORCHESTRATOR ---


def _handle_complexity_mode(args: argparse.Namespace) -> None:
    violations = scan_code_complexity(args.target)
    report_complexity(violations)

    if args.fix and violations:
        logger.info("\n[WISDOM] Initiating Sentinel Auto-Fix for Codebase...")
        sentinel_script = Path(__file__).parent / "sentinel_sword.py"
        try:
            subprocess.run(["python", str(sentinel_script)], check=True)
            logger.info("✅ [ACTION] Sentinel fix complete.")
        except Exception:
            logger.exception("❌ [ERROR] Sentinel fix failed")


def _handle_governance_mode(args: argparse.Namespace) -> None:
    scan_governance(args.target)

    if args.fix:
        logger.info("\n[WISDOM] Initiating Reforge v3 for Governance Artifacts...")
        reforge_script = Path(__file__).parent / "reforge.py"

        # Reforge targets the specific path if provided, else defaults
        target_arg = args.target if args.target != "." else None

        cmd = ["python", str(reforge_script)]
        if target_arg:
            cmd.append(target_arg)

        try:
            subprocess.run(cmd, check=True)
            logger.info("✅ [ACTION] Reforge complete (UIP/AGP repaired).")
        except Exception:
            logger.exception("❌ [ERROR] Reforge failed")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sophia's Wisdom: The Synarche Auditor"
    )
    parser.add_argument(
        "--mode",
        choices=["complexity", "governance", "all"],
        default="all",
        help="Scan mode",
    )
    parser.add_argument("--target", default=".", help="Target directory or file")
    parser.add_argument(
        "--fix", action="store_true", help="Autonomously repair detected issues."
    )

    args = parser.parse_args()

    # 1. COMPLEXITY / CODE WISDOM
    if args.mode in ["complexity", "all"]:
        _handle_complexity_mode(args)

    # 2. GOVERNANCE WISDOM
    if args.mode in ["governance", "all"]:
        _handle_governance_mode(args)


if __name__ == "__main__":
    main()
