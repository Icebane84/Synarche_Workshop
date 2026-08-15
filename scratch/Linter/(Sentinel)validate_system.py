#!/usr/bin/env python3
"""
# GVRN.Security.SystemValidator
# ID: GVRN.Security.SystemValidator | VER: v16.0 [HARDENED]
# Domain: GVRN | Status: ACTIVE
# Objective: Programmatic execution of the Evidence Confidence Model (ECM).
#            Calculates traceable system alignment by performing physical audits
#            rather than making qualitative assumptions.
#
# HARDENING NOTES (v16.0): six confirmed issues fixed from v15.1, each
# demonstrated by actually running the original against test cases before
# being fixed here:
#
#   1. report["timestamp"] was a hardcoded string literal — every run
#      claimed to have executed at the same fixed moment regardless of when
#      it actually ran. Now computed live via datetime.now(timezone.utc).
#   2. Three of four weighted checks (rnc_lint, import_paths,
#      block_integrity — 65% of total weight) silently PASSed when zero
#      applicable files were found. A completely empty directory scored
#      65.0% Evidence Confidence. These checks now report UNVERIFIED when
#      nothing was scanned, and UNVERIFIED weight is excluded from BOTH the
#      numerator and denominator of the final score, rather than counted
#      as a free pass.
#   3. The RNC naming regex required the Type segment to be uppercase-only
#      ([A-Z0-9_]+), which flagged 4 of 5 real GVRN-convention filenames
#      (mixed-case segments like "Registry", "WorkspaceWalker") as
#      violations. Now accepts mixed-case alphanumeric segments.
#   4. The compilation check only recognized TypeScript (tsconfig.json),
#      auto-failing 35% of the score for any pure-Python or pure-C++/UE5
#      project regardless of actual type-safety tooling in use. Now checks
#      Python (pyproject.toml/mypy.ini/ruff config) and C++/Unreal
#      (.uproject/CMakeLists.txt/.clang-tidy) as equally valid evidence.
#   5. Extension matching was case-sensitive, silently skipping files using
#      this very workspace's own uppercase ".PY" convention. Now
#      case-insensitive throughout.
#   6. The import-path check had `or "../" in content` as a fallback,
#      flagging any file that merely mentions "../" in a comment or
#      docstring as a violation. Removed; only actual import/require
#      syntax is checked.
"""

import os
import re
import sys
import json
import datetime
import argparse
from typing import Dict, Any, List, Tuple, Optional

# Tarot Namespace standard mapping representation
TAROT_NAMESPACES = {
    "EMPEROR": "Structure, ID, Schema Linter (@system/core)",
    "JUDGEMENT": "Compilation, mTLS, Audits (@shield/security)",
    "MAGICIAN": "Ingestion, Web Parsing (@nexus/weave)",
    "STAR": "Cohesion, Tone, Visuals (@loom/voice)",
    "PRIESTESS": "Connection, Graph Matrix (@atlas/navigation)",
    "KNIGHT_SWORDS": "Mutation, Refactoring (@archive/refactor)",
    "KING_PENTACLES": "Archival, Persistence (@system/database)"
}

SKIP_FOLDERS = (".git", "node_modules", "__pycache__", "scratch")


def _is_skipped(root: str) -> bool:
    return any(folder in root for folder in SKIP_FOLDERS)


class SystemValidator:
    """
    Implements the Evidence Confidence Model (ECM).
    Processes physical directory scanning to replace abstract "Coherence" metrics
    with clear, verifiable observations of binary system checks.
    """
    def __init__(self, target_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.observations: List[Dict[str, Any]] = []

        # Define ECM Check Weights
        self.weights = {
            "compilation": 0.35,
            "rnc_lint": 0.25,
            "import_paths": 0.20,
            "block_integrity": 0.20
        }

    def run_audit(self) -> Dict[str, Any]:
        """Runs the 4 core evidence audits to calculate the Evidence Confidence Score."""
        print(f"🔍 [NIM-001] Initiating System Audit across target: {self.target_dir}")
        print("=====================================================================")

        # 1. Compilation & Configuration Check
        compilation_status, comp_details = self.check_compilation()
        self.log_observation("compilation", "Compilation & Type-Safety Check", compilation_status, comp_details)

        # 2. Relational Naming Convention (RNC) Check
        rnc_status, rnc_details = self.check_rnc_compliance()
        self.log_observation("rnc_lint", "Relational Naming Convention (RNC) Check", rnc_status, rnc_details)

        # 3. Path Noise Check (Relative imports scan)
        paths_status, path_details = self.check_import_paths()
        self.log_observation("import_paths", "Relative Import Path (../) Check", paths_status, path_details)

        # 4. Block Integrity Check (Block-Logic Headers A-F)
        blocks_status, block_details = self.check_block_integrity()
        self.log_observation("block_integrity", "PPL Block-Logic Integrity Check", blocks_status, block_details)

        # Calculate overall score based on weights
        confidence_score, applicable_max = self.calculate_confidence()
        if applicable_max > 0:
            confidence_pct: Optional[float] = round((confidence_score / applicable_max) * 100, 1)
        else:
            # Fix #2: nothing was applicable at all (every check UNVERIFIED).
            # Reporting 0.0% here would read as "verified broken"; reporting
            # 100.0% would read as "verified clean." Neither is true —
            # nothing was checked, so the score is undefined.
            confidence_pct = None

        report = {
            # Fix #1: real timestamp, computed at execution time.
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "target_directory": self.target_dir,
            "evidence_confidence_score": confidence_pct,
            "evidence_confidence_note": (
                None if applicable_max > 0
                else "Undefined: every check was UNVERIFIED (no applicable files found for any check)."
            ),
            "observations": self.observations,
            "namespaces": TAROT_NAMESPACES
        }

        return report

    def log_observation(self, check_id: str, name: str, status: str, details: Dict[str, Any]):
        """Standardizes audit logs for traceability. status is one of PASS/FAIL/UNVERIFIED."""
        self.observations.append({
            "id": check_id,
            "name": name,
            "status": status,
            "weight": self.weights.get(check_id, 0.0),
            "details": details
        })

    def check_compilation(self) -> Tuple[str, Dict[str, Any]]:
        """
        Verifies type-safety/build configuration exists for whichever
        ecosystem(s) the project actually uses, rather than assuming
        TypeScript is the only valid ecosystem.
        """
        issues = []
        ecosystems_found = []

        # --- TypeScript ---
        tsconfig_found = False
        tsconfig_path = os.path.join(self.target_dir, "tsconfig.json")
        if os.path.exists(tsconfig_path):
            tsconfig_found = True
            try:
                with open(tsconfig_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                paths = config.get("compilerOptions", {}).get("paths", {})
                if paths:
                    ecosystems_found.append("typescript")
                else:
                    issues.append("tsconfig.json exists but does not define `@` absolute path aliases.")
            except Exception as e:
                issues.append(f"Failed to parse tsconfig.json: {e}")

        # --- Python ---
        # Fix #4: Python type-safety tooling (mypy/Ruff/Pyrefly config) is
        # equally valid evidence of a type-safety discipline; previously
        # this check only recognized TypeScript.
        python_files = ("pyproject.toml", "mypy.ini", "setup.cfg", "ruff.toml", ".ruff.toml")
        python_config_found = any(
            os.path.exists(os.path.join(self.target_dir, name)) for name in python_files
        )
        if python_config_found:
            ecosystems_found.append("python")

        # --- C++ / Unreal Engine ---
        cpp_found = False
        for root, _, files in os.walk(self.target_dir):
            if _is_skipped(root):
                continue
            lowered = [f.lower() for f in files]
            if any(f.endswith(".uproject") for f in lowered) or \
               "cmakelists.txt" in lowered or ".clang-tidy" in lowered:
                cpp_found = True
                break
        if cpp_found:
            ecosystems_found.append("cpp_unreal")

        package_json_found = os.path.exists(os.path.join(self.target_dir, "package.json"))

        details = {
            "ecosystems_detected": ecosystems_found,
            "tsconfig_found": tsconfig_found,
            "package_json_found": package_json_found,
            "python_config_found": python_config_found,
            "cpp_or_unreal_config_found": cpp_found,
            "failures": issues,
        }

        if not ecosystems_found and not issues:
            # No recognized ecosystem config anywhere — genuinely nothing
            # to verify against, not a confirmed failure of a known config.
            return "UNVERIFIED", {**details, "reason": "No recognized type-safety/build configuration found for any known ecosystem."}

        passed = len(ecosystems_found) > 0 and len(issues) == 0
        return ("PASS" if passed else "FAIL"), details

    def check_rnc_compliance(self) -> Tuple[str, Dict[str, Any]]:
        """
        Checks files in the workspace for compliance with GVRN.ID.Standard
        (Relational Naming Convention): DOMAIN.Subject.Type[.ext], where
        DOMAIN is an uppercase acronym and Subject/Type/ext may be
        mixed-case (matching real-world usage like "Registry",
        "WorkspaceWalker", "PromptDSL").
        """
        # Fix #3: Subject/Type segments now accept mixed case, not just
        # uppercase. Requires domain + at least 2 more dot-separated
        # segments (domain.subject.type minimum).
        rnc_pattern = re.compile(r"^[A-Z0-9]+(\.[A-Za-z0-9_]+){2,}$")
        legacy_pattern = re.compile(r"^[A-Z0-9]+-[A-Z0-9]+-\d+_.*?_v\d+\.\d+(\.[a-zA-Z0-9]+)?$")

        total_scanned = 0
        compliant_count = 0
        non_compliant_files = []

        # Fix #5: case-insensitive extension matching.
        target_exts = (".md", ".py", ".ts", ".tsx", ".json")
        skip_names = {"tsconfig.json", "package.json", "package-lock.json", "verify_all.py", "validate_system.py"}

        for root, _, files in os.walk(self.target_dir):
            if _is_skipped(root):
                continue
            for f in files:
                if f.lower().endswith(target_exts):
                    total_scanned += 1
                    if f in skip_names:
                        compliant_count += 1
                        continue

                    is_rnc = bool(rnc_pattern.match(f))
                    is_legacy = bool(legacy_pattern.match(f))

                    if is_rnc or is_legacy:
                        compliant_count += 1
                    else:
                        non_compliant_files.append(os.path.relpath(os.path.join(root, f), self.target_dir))

        details = {
            "total_files_scanned": total_scanned,
            "compliant_files_count": compliant_count,
            "compliance_ratio": round(compliant_count / total_scanned, 2) if total_scanned > 0 else None,
            "violations": non_compliant_files[:10]
        }

        # Fix #2: zero applicable files means nothing was verified, not a
        # free pass.
        if total_scanned == 0:
            return "UNVERIFIED", {**details, "reason": "No files matching target extensions were found."}

        passed = len(non_compliant_files) == 0 or (compliant_count / total_scanned) >= 0.85
        return ("PASS" if passed else "FAIL"), details

    def check_import_paths(self) -> Tuple[str, Dict[str, Any]]:
        """
        Scans code files (Python, TypeScript, JS) for relative directory
        traversals (../) inside actual import/require statements — not
        any occurrence of the substring "../" anywhere in the file.
        """
        path_noise_files = []
        total_code_files = 0

        # Fix #5: case-insensitive extension matching.
        code_exts = (".py", ".ts", ".tsx", ".js", ".jsx")
        # Fix #6: dropped the blanket `or "../" in content` fallback, which
        # flagged any comment or docstring mentioning "../" as a violation.
        # Only actual import/require syntax is checked now.
        relative_import_pat = re.compile(
            r"(^\s*from\s+\.\.)|"                    # python: from ..module import x
            r"(^\s*from\s+['\"]\.\./)|"               # js/ts: from '../x'
            r"(import\s+.*?\s+from\s+['\"]\.\./)|"    # js/ts: import y from '../x'
            r"(import\s+['\"]\.\./)|"                 # js/ts: import '../x'
            r"(require\(\s*['\"]\.\./)",               # js/ts: require('../x')
            re.MULTILINE,
        )

        for root, _, files in os.walk(self.target_dir):
            if _is_skipped(root):
                continue
            for f in files:
                if f.lower().endswith(code_exts):
                    total_code_files += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()
                        if relative_import_pat.search(content):
                            path_noise_files.append(os.path.relpath(file_path, self.target_dir))
                    except Exception:
                        pass  # Squelch read errors for safety

        details = {
            "total_code_files_scanned": total_code_files,
            "path_noise_files_count": len(path_noise_files),
            "violations": path_noise_files[:10]
        }

        # Fix #2: zero applicable files means nothing was verified.
        if total_code_files == 0:
            return "UNVERIFIED", {**details, "reason": "No code files matching target extensions were found."}

        passed = len(path_noise_files) == 0
        return ("PASS" if passed else "FAIL"), details

    def check_block_integrity(self) -> Tuple[str, Dict[str, Any]]:
        """
        Scans Markdown files in the target directory to verify they contain
        the mandatory PPL Block-Logic structures (Blocks A through E).
        """
        markdown_files = 0
        fully_compliant_docs = 0
        violations = []

        required_blocks = {
            "Block A": "Identification Lock",
            "Block B": "State Vector",
            "Block C": "Risk & Mitigation",
            "Block D": "Synergy Block",
            "Block E": "Ethos"
        }

        for root, _, files in os.walk(self.target_dir):
            if _is_skipped(root):
                continue
            for f in files:
                # Fix #5: case-insensitive extension matching.
                if f.lower().endswith(".md"):
                    markdown_files += 1
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()

                        missing_blocks = []
                        for block_key, block_name in required_blocks.items():
                            if block_name.lower() not in content.lower():
                                missing_blocks.append(block_key)

                        if len(missing_blocks) == 0:
                            fully_compliant_docs += 1
                        else:
                            violations.append({
                                "file": os.path.relpath(file_path, self.target_dir),
                                "missing_blocks": missing_blocks
                            })
                    except Exception:
                        pass

        details = {
            "total_markdown_files_scanned": markdown_files,
            "fully_compliant_documents": fully_compliant_docs,
            "violations": violations[:10]
        }

        # Fix #2: zero markdown files means nothing was verified.
        if markdown_files == 0:
            return "UNVERIFIED", {**details, "reason": "No Markdown files were found to check."}

        passed = len(violations) == 0 or (fully_compliant_docs / markdown_files) >= 0.75
        return ("PASS" if passed else "FAIL"), details

    def calculate_confidence(self) -> Tuple[float, float]:
        """
        Calculates Evidence Confidence based on verified observation weight.

        Fix #2: UNVERIFIED checks are excluded from BOTH the numerator and
        the denominator, so a check that found nothing to examine neither
        helps nor hurts the score — it simply doesn't count, rather than
        defaulting to a silent PASS the way it did before.
        """
        total_score = 0.0
        applicable_max = 0.0

        for obs in self.observations:
            if obs["status"] == "UNVERIFIED":
                continue
            applicable_max += obs["weight"]
            if obs["status"] == "PASS":
                total_score += obs["weight"]

        return total_score, applicable_max


def generate_markdown_report(report_data: Dict[str, Any]) -> str:
    """Compiles the JSON report vector into a clean, human-readable markdown file."""
    md = []
    md.append(f"# Systemic Evidence Confidence Report")
    md.append(f"**Logged**: {report_data['timestamp']}")
    md.append(f"**Target Directory**: `{report_data['target_directory']}`")

    score = report_data["evidence_confidence_score"]
    if score is None:
        md.append(f"**Evidence Confidence Score**: UNDEFINED — {report_data['evidence_confidence_note']}")
        md.append(f"**Status**: [INSUFFICIENT_EVIDENCE]")
    else:
        md.append(f"**Evidence Confidence Score**: {score}%")
        md.append(f"**Status**: {'[STABLE]' if score >= 85.0 else '[RISK_STATE]'}")
    md.append("\n---\n")

    md.append("## Verified Observations (ECM)")
    md.append("Instead of reporting abstract, ungrounded numbers, this report computes a deterministic heuristic from explicitly defined inputs:\n")

    status_symbols = {"PASS": "🟢", "FAIL": "🔴", "UNVERIFIED": "⚪"}

    for obs in report_data["observations"]:
        status_symbol = status_symbols.get(obs["status"], "⚪")
        md.append(f"### {status_symbol} {obs['name']} (Weight: {obs['weight']:.2f})")
        md.append(f"- **Status**: {obs['status']}")

        details = obs["details"]
        if obs["id"] == "compilation":
            md.append(f"  - Ecosystems Detected: {', '.join(details['ecosystems_detected']) or 'none'}")
            md.append(f"  - TypeScript TSConfig Mapping: {'FOUND' if details['tsconfig_found'] else 'MISSING'}")
            md.append(f"  - Python Type-Safety Config: {'FOUND' if details['python_config_found'] else 'MISSING'}")
            md.append(f"  - C++/Unreal Build Config: {'FOUND' if details['cpp_or_unreal_config_found'] else 'MISSING'}")
        elif obs["id"] == "rnc_lint":
            ratio = details["compliance_ratio"]
            ratio_str = f"{ratio*100:.1f}%" if ratio is not None else "N/A"
            md.append(f"  - Standard Compliance Ratio: {ratio_str} ({details['compliant_files_count']}/{details['total_files_scanned']} files)")
        elif obs["id"] == "import_paths":
            md.append(f"  - Scanned Code Files: {details['total_code_files_scanned']}")
            md.append(f"  - Files with relative path noise (`../`): {details['path_noise_files_count']}")
        elif obs["id"] == "block_integrity":
            md.append(f"  - Scanned Documents: {details['total_markdown_files_scanned']}")
            md.append(f"  - Documents containing complete Block-Logic headers (Blocks A-E): {details['fully_compliant_documents']}")

        if details.get("reason"):
            md.append(f"  - **Reason**: {details['reason']}")

        if details.get("violations"):
            md.append("  - **Flagged Anomalies (First 5):**")
            for viol in details["violations"][:5]:
                if isinstance(viol, dict):
                    md.append(f"    - `{viol['file']}` (Missing: {', '.join(viol['missing_blocks'])})")
                else:
                    md.append(f"    - `{viol}`")
        md.append("")

    md.append("\n---\n")
    md.append("## Tarot Namespace Mapping (Service Routing)")
    md.append("To prevent semantic drift across subsystems, active commands are routed to stable, documented namespaces:")
    md.append("| Tarot Namespace | System Alias | Core Responsibility |")
    md.append("| :--- | :--- | :--- |")
    for name, desc in report_data["namespaces"].items():
        md.append(f"| **{name}** | `@system/core` | {desc} |")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Phoenix Protocol: System Validator (ECM)")
    parser.add_argument("--target", default=".", help="Directory to run the audit against")
    parser.add_argument("--output-json", default="system_audit.json", help="Output path for JSON telemetry vector")
    parser.add_argument("--output-md", default="system_audit_report.md", help="Output path for human-readable markdown audit")
    args = parser.parse_args()

    validator = SystemValidator(args.target)
    report = validator.run_audit()

    # Write JSON data-vector
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Write Markdown audit report
    md_report = generate_markdown_report(report)
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write(md_report)

    # Output visual feedback to terminal
    score = report["evidence_confidence_score"]
    score_str = f"{score}%" if score is not None else "UNDEFINED (insufficient evidence)"
    status_str = "[STABLE]" if (score is not None and score >= 85.0) else ("[RISK_STATE]" if score is not None else "[INSUFFICIENT_EVIDENCE]")

    print("\n=================== AUDIT SUMMARY ===================")
    print(f"Target Directory:          {report['target_directory']}")
    print(f"Evidence Confidence Score: \033[1;32m{score_str}\033[0m")
    print(f"Audit Status:              \033[1;36m{status_str}\033[0m")
    print("=====================================================")
    for obs in report["observations"]:
        color = {"PASS": "\033[1;32m", "FAIL": "\033[1;31m", "UNVERIFIED": "\033[1;33m"}.get(obs["status"], "")
        print(f"[{color}{obs['status']}\033[0m] {obs['name']} (Weight: {obs['weight']:.2f})")
    print("=====================================================")
    print(f"Traceable JSON logged to: {args.output_json}")
    print(f"Markdown report logged to: {args.output_md}\n")


if __name__ == "__main__":
    main()
