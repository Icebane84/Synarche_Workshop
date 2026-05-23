"""# AOP-SENTINEL-SCAN-001: The Code Sentinel Protocol.

# I. Universal Identification & Provenance (The Vector Signature)
| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `AOP-SENTINEL-SCAN-001` |
| **2. Official Name** | `sentinel.py` |
| **3. Version** | **v15.0 [OMEGA]** |
| **4. Provenance** | **Reforged: 2026-04-28** |
| **5. Domain** | `ARCH` |
| **6. Evolution** | **Authentic Persona** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. Status (State)** | `[ACTIVE]` |
| **10. Ethos** | **Guardian of Coherence** |
| **11. Integrity Hash** | `[UIP-V15-LOCK]` |

---

### **I.B. Axiom Reference**
> "The sentinel does not sleep, for entropy does not rest." — Axiom of Sentinel
"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .auditor import ComplianceAuditor
from .crf import CausalLinter
from .lib.resonance_scanner import ArtifactScanner
from .lib.task_context import TaskContext
from .soul import ArtificersSoul

# Configure logging
logger = logging.getLogger(__name__)


class CodeSentinel:
    """The Sentinel module responsible for proactive codebase analysis."""

    def __init__(self) -> None:
        self.soul = ArtificersSoul()
        self.crf = CausalLinter()
        self.auditor = ComplianceAuditor()
        self.task_context = TaskContext()
        self.scanner = ArtifactScanner(self.task_context)

    def scan_causality(self, root_path: str) -> list[dict[str, Any]]:
        """[NEW] Scans text artifacts for Causal Resoance."""
        causal_report = []
        for root, dirs, files in os.walk(root_path):
            # OMEGA v15.1 - Performance Optimization
            exclude_dirs = {
                ".git",
                ".venv",
                ".venv_prs",
                "__pycache__",
                "node_modules",
                ".gemini",
                "artifacts",
                "brain",
                ".mypy_cache",
                ".pytest_cache",
            }
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if not file.endswith(".md"):
                    continue

                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()

                    analysis = self.crf.validate_causality(content)
                    if not analysis["is_causal"]:
                        causal_report.append(
                            {
                                "file": file,
                                "path": path,
                                "dissonance": "Acausal / Floating Abstraction",
                                "score": analysis["resonance_score"],
                            }
                        )
                except Exception:
                    logger.warning(f"Failed to scan {path}")
                    continue
        return causal_report

    def scan_governance(self, root_path: str) -> dict:
        """Performs a dual-layer audit:
        1. Resonance Scan (Breadth)
        2. Compliance Audit (Depth/OGLN v11.0).
        """
        # Layer 1: Breadth (Resonance)
        total, aligned, unaligned_paths = self.scanner.scan_directory(Path(root_path))
        resonance_score = (aligned / total * 100) if total > 0 else 0.0

        # Layer 2: Depth (Compliance Auditor)
        detailed_findings = []
        for path in unaligned_paths:
            if path.suffix == ".md":
                res = self.auditor.audit_file(str(path))
                detailed_findings.append(
                    {
                        "file": res.file_path,
                        "status": res.status,
                        "errors": res.errors,
                        "score": res.score,
                    }
                )

        report = {
            "resonance_score": resonance_score,
            "dissonant_files": [str(p) for p in unaligned_paths],
            "detailed_findings": detailed_findings,
            "timestamp": datetime.now().isoformat(),
        }

        # Log to Triage Report (Sentinel Protocol)
        self.log_to_triage(report, root_path)

        return report

    PASS_THRESHOLD = 90.0
    TOP_FINDINGS_LIMIT = 3

    def log_to_triage(self, report: dict[str, Any], root_path: str) -> None:
        """Appends a summary of the scan to _governance/5_Logs/GVRN.Triage.Report.md."""
        try:
            # Construct path relative to workspace root (assuming running from root or similar context)
            # If root_path is '.', then use CWD.
            workspace_root = Path(root_path).resolve()
            report_path = (
                workspace_root / "_governance" / "5_Logs" / "GVRN.Triage.Report.md"
            )

            # If _governance doesn't exist relative to root_path, try to find it up one level or assume fixed path
            if not report_path.parent.exists():
                # Fallback: Try absolute path relative to known structure
                # This assumes standard Synarche layout
                # ../../../_governance/5_Logs/GVRN.Triage.Report.md depending on execution context
                pass

            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            score = report.get("resonance_score", 0.0)
            status = "PASS" if score > self.PASS_THRESHOLD else "FAIL"
            findings_count = len(report.get("detailed_findings", []))

            log_entry = f"""
# [{timestamp_str}] Sentinel Scan
> **Score**: {score:.1f}% | **Status**: {status}
> **Target**: `{root_path}` | **Dissonance**: {findings_count} files

"""
            # Append findings if any (limit to top 3)
            if findings_count > 0:
                log_entry += "| File | Error |\n| :--- | :--- |\n"
                for finding in report["detailed_findings"][: self.TOP_FINDINGS_LIMIT]:
                    fname = Path(finding["file"]).name
                    err = (
                        finding["errors"][0]
                        if finding["errors"]
                        else "Unknown Dissonance"
                    )
                    log_entry += f"| `{fname}` | {err} |\n"
                if findings_count > self.TOP_FINDINGS_LIMIT:
                    log_entry += f"| ...and {findings_count - self.TOP_FINDINGS_LIMIT} more | |\n"

            log_entry += "\n---\n"

            # Append to file
            if report_path.exists():
                with open(report_path, "a", encoding="utf-8") as f:
                    f.write(log_entry)
            # Attempt to create if directory exists
            elif report_path.parent.exists():
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(f"# GVRN.Triage.Report (Auto-Generated)\n\n{log_entry}")

        except Exception as e:
            logger.warning(f"Failed to log to Triage Report: {e}")


if __name__ == "__main__":
    import json

    # Default to scanning one level up from 'src' (the workspace root)
    # Correct path calculation: axion-core/src/hephaestus/sentinel.py -> axion-core/
    root_to_scan = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    print(f"[*] SENTINEL: Starting Governance Audit for: {root_to_scan}")
    sentinel = CodeSentinel()

    # Layer 1: Governance/Compliance
    report = sentinel.scan_governance(root_to_scan)

    # Layer 2: Causality
    causal_findings = sentinel.scan_causality(root_to_scan)
    report["causal_dissonance"] = causal_findings

    print("\n[+] AUDIT COMPLETE")
    print(f"Resonance Score: {report['resonance_score']:.1f}%")
    print(f"Dissonant Files: {len(report['dissonant_files'])}")
    print(f"Causal Dissonance: {len(causal_findings)} files")

    if report["resonance_score"] < 100.0:
        print("\n[!] Dissonance detected in the following paths:")
        for path in report["dissonant_files"][:10]:
            print(f"  - {path}")
        if len(report["dissonant_files"]) > 10:
            print(f"  - ... and {len(report['dissonant_files']) - 10} more.")

    # Write full JSON report to a temporary artifact
    with open("sentinel_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\n[i] Full report written to: sentinel_report.json")
