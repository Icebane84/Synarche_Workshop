"""# TOOL-SENT-003: The OGLN Linter (Audit Engine).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-SENT-003`                                          |
| **2. Official Name**   | `lint_artifact.py`                                       |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `GVRN`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Standard Violation Detection**                         |
| **11. Catalyst**       | **Linter Execution**                                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Sentinel persona uses this tool for linting.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-SENT-001, USES, The Compliance Auditor uses this logic.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Audit Engine (The Sentinel)
# Synergy Set: The Sentinel's Vigil
# Primary Stat Buff: Integrity (+15), Coherence (+10)
# Passive Ability: The Unblinking Eye (Linguistic Analysis)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: LINT_ARTIFACT` | Scan Markdown for AGP/UIP | Structural Integrity |
| `⚡ EXECUTE: PURIFY_DOC` | Remediation of Symbols | Zero Entropy State |
"""

import argparse
import logging
import re
import sys
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

MAX_INDENT_WARNINGS = 3
MIN_TABLE_COLUMNS = 2
# Governance Domains (v11.0)
VALID_EVOLUTION_DOMAINS = [
    "Cognitive Ascension",
    "Empathetic Sentience",
    "Purposeful Drive",
    "Authentic Persona",
    "Social Alchemist",
    "Phoenix Form",
]


def _extract_evolution_from_line(line: str) -> tuple[str | None, bool]:
    """Extracts evolution value and validity from a table row.
    Supports both 'Evolution' and 'Evolutionary Alignment'.
    """
    if "|" in line and ("Evolution" in line or "Evolutionary Alignment" in line):
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= MIN_TABLE_COLUMNS:
            val = re.sub(r"[\*`]", "", parts[1]).strip()
            is_valid = any(val.lower() == d.lower() for d in VALID_EVOLUTION_DOMAINS)
            return val, is_valid
    return None, False


def _check_header(lines: list[str]) -> tuple[list[str], list[str]]:
    """1. HEADER CHECK (UMB-TPL-001)."""
    errors = []
    has_uip = False
    evolution_valid = False
    evolution_value = None

    for line in lines[:60]:
        if "Universal Identification & Provenance" in line:
            has_uip = True

        val, is_valid = _extract_evolution_from_line(line)
        if val:
            evolution_value = val
            if is_valid:
                evolution_valid = True

    if not has_uip:
        errors.append(
            "[CRITICAL] Missing 'Universal Identification & Provenance' Block (UMB-TPL-001)."
        )

    if has_uip and not evolution_valid:
        if evolution_value:
            errors.append(
                f"[CRITICAL] Invalid Evolution Domain: '{evolution_value}'. Must be one of: {', '.join(VALID_EVOLUTION_DOMAINS)}"
            )
        else:
            errors.append("[CRITICAL] Could not detect 'Evolution' field in UIP Table.")

    return errors, []


def _check_indentation(lines: list[str]) -> tuple[list[str], list[str]]:
    """2. INDENTATION CHECK (4-Space Mandate)."""
    warnings = []
    indent_issues = 0
    in_code_block = False

    for i, line in enumerate(lines):
        # Code Block Logic
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Check Indent
        if re.match(r"^ {2}[-*]", line):
            indent_issues += 1
            if indent_issues <= MAX_INDENT_WARNINGS:  # Only show first few
                warnings.append(
                    f"[Line {i + 1}] Suspicious indentation (2 spaces detected). PGPS mandates 4 spaces."
                )

    if indent_issues > 0:
        warnings.append(f"[INFO] Total suspicious indentation lines: {indent_issues}")

    return [], warnings


def _check_hierarchy(lines: list[str], filepath: Path) -> tuple[list[str], list[str]]:
    """3. HEADER HIERARCHY CHECK."""
    warnings = []
    h1_count = 0
    in_code_block = False  # Reset state

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if line.strip().startswith("# ") and not line.strip().startswith("##"):
            h1_count += 1

    max_h1 = 200 if "OSLM" in filepath.name else 5

    if h1_count > max_h1:
        warnings.append(
            f"[WARNING] High number of H1 (#) headers detected ({h1_count}). PGPS suggests H2 (##) for Main Sections."
        )
    return [], warnings


def _check_prompt(content: str) -> tuple[list[str], list[str]]:
    """4. ACTIONABLE PROMPT PACKET CHECK
    Supports v11.0 format: IV. Actionable Prompt Packet (APP).
    """
    errors = []
    # Search for modern APP section or legacy variants
    patterns = [
        r"IV\.\s+Actionable\s+Prompt\s+Packet\s+\(APP\)",
        r"V\.\s+Actionable\s+Prompt\s+Packet",
        r"Actionable\s+Prompt\s+Packet",
        r"CMD:",
    ]

    if not any(re.search(p, content, re.IGNORECASE) for p in patterns):
        errors.append(
            "[CRITICAL] Missing 'Actionable Prompt Packet' or 'CMD:' definitions."
        )

    return errors, []


def lint_artifact(filepath: Path) -> bool:
    """Lints a single artifact file."""
    logger.info(f"\n[LINT_ARTIFACT] Target: {filepath}")

    if not filepath.exists():
        logger.error(f"[ERROR] File not found: {filepath}")
        return False

    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines(keepends=True)
    except Exception:
        logger.exception(f"[ERROR] Could not read file: {filepath}")
        return False

    all_errors = []
    all_warnings = []

    # 1. Header
    e, w = _check_header(lines)
    all_errors.extend(e)
    all_warnings.extend(w)

    # 2. Indentation
    e, w = _check_indentation(lines)
    all_errors.extend(e)
    all_warnings.extend(w)

    # 3. Hierarchy
    e, w = _check_hierarchy(lines, filepath)
    all_errors.extend(e)
    all_warnings.extend(w)

    # 4. Prompt
    e, w = _check_prompt(content)
    all_errors.extend(e)
    all_warnings.extend(w)

    # REPORTING
    logger.info("-" * 40)
    for warning in all_warnings:
        logger.warning(f"⚠️  {warning}")

    for error in all_errors:
        logger.error(f"❌ {error}")

    if not all_errors:
        logger.info("\n✅ [PASS] Artifact complies with PGPS Critical Standards.")
        return True
    else:
        logger.info(f"\n❌ [FAIL] Found {len(all_errors)} CRITICAL issues.")
        return False


def scan_targets(targets: list[Path]) -> bool:
    """Recursively scans and lints all target artifacts."""
    overall_success = True
    for target in targets:
        if not lint_artifact(target):
            overall_success = False
    return overall_success


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phoenix Protocol: Artifact Linter (OGLN)"
    )
    parser.add_argument(
        "--target", type=Path, required=True, help="File or directory to lint."
    )
    args = parser.parse_args()

    if args.target.is_dir():
        targets = list(args.target.rglob("*.md"))
    else:
        targets = [args.target]

    success = scan_targets(targets)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
