#!/usr/bin/env python3
"""IDENTIFICATION: TOOL-SENTINEL-SWORD-001
VERSION: v15.0 [OMEGA]
STATUS: [CANONIZED]
TIMESTAMP: 2026-03-24.
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

"""
ENTITY-SENTINEL-PRIME-001: The Sentinel's Sword
Domain: GVRN | State: ACTIVE | Version: v15.0 [OMEGA]
Objective: Execute ethical governance and document compliance audits.
"""

# Configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Paths
TOOLS_DIR = Path(__file__).parent
COMPLIANCE_TOOL = TOOLS_DIR / "compliance_audit.py"


def run_audit(target: str = ".") -> str:
    """Run the compliance audit wrapper."""
    if not COMPLIANCE_TOOL.exists():
        return json.dumps({
            "status": "ERROR",
            "message": "Physical compliance tool (compliance_audit.py) missing."
        }, indent=2)

    try:
        # Execute the external compliance tool
        result = subprocess.run([sys.executable, str(COMPLIANCE_TOOL), target], capture_output=True, text=True, check=True)
        return json.dumps({
            "status": "PASS",
            "message": "Compliance verified (Law 24).",
            "output": result.stdout.strip()
        }, indent=2)
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "status": "CRITICAL_ERROR",
            "exit_code": e.returncode,
            "output": e.stdout.strip(),
            "error": e.stderr.strip()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "CRITICAL_ERROR",
            "message": str(e)
        }, indent=2)


def _extract_references_from_file(file_path: Path, link_re: re.Pattern) -> set[str]:
    """Helper to extract referenced markdown filenames from a file."""
    referenced = set()
    try:
        # Iterate line-by-line to avoid loading massive files entirely into memory
        with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                for match in link_re.finditer(line):
                    ref = match.group(1) or os.path.basename(match.group(2) or "")
                    if ref:
                        referenced.add(ref.strip())
    except Exception:
        pass
    return referenced


def check_coherence(target: str = ".") -> str:
    """Implement the GOC Coherence Check (Law 14) to find unlinked markdown files."""
    target_path = Path(target)
    if not target_path.exists() or not target_path.is_dir():
        return json.dumps({"status": "ERROR", "message": "Target directory not found."}, indent=2)

    skip_dirs = {".git", "node_modules", ".venv", "__pycache__"}
    link_re = re.compile(r"\[\[([^\]]+)\]\]|\[[^\]]+\]\(([^)]+\.md)\)")

    all_files = set()
    all_referenced = set()

    for root, dirs, files in os.walk(target_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith(".md"):
                all_files.add(f)
                all_referenced.update(_extract_references_from_file(Path(root, f), link_re))

    orphans = sorted(all_files - all_referenced)
    coherence_index = 1.0 if not all_files else 1.0 - (len(orphans) / len(all_files))

    return json.dumps({
        "status": "PASS" if not orphans else "FAIL",
        "coherence_index": round(coherence_index, 2),
        "total_files": len(all_files),
        "orphan_count": len(orphans),
        "orphans": orphans
    }, indent=2)


def main() -> None:
    """Run the main CLI for Sentinel's Sword."""
    parser = argparse.ArgumentParser(description="Sentinel's Sword Audit Engine")
    parser.add_argument("--target", default=".")
    parser.add_argument(
        "--custom_rule",
        default=None,
        help="Custom Audit Rule (e.g., COHERENCE_CHECK)",
    )

    args = parser.parse_args()

    logger.info("--- [SENTINEL] SWORD STATUS: ACTIVE ---")

    result: str
    if args.custom_rule == "COHERENCE_CHECK":
        logger.info(f"--- [MODE] CUSTOM RULE: {args.custom_rule} ---")
        result = check_coherence(args.target)
    else:
        result = run_audit(args.target)

    logger.info(result)


if __name__ == "__main__":
    main()
