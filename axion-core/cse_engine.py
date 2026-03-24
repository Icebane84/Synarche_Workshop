"""
IDENTIFICATION: SYNG.ENGINE.CSE
VERSION: v15.0 [OMEGA]
STATUS: KINETIC
TIMESTAMP: 2026-03-24
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class CoherentSynthesisEngine:
    """
    WHAT: The primary execution substrate for repository-wide data synthesis.
    HOW: Ingests the Flattened Loom and validates it against the Law (Metadata).
    WHY: To achieve a Zero Entropy state where documentation and code are unified.
    """

    def __init__(self) -> None:
        # Anchor to the repository root relative to axion-core/
        self.root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def synthesize_loom(self) -> Dict[str, Any]:
        """
        WHAT: High-density synthesis of the Flattened Loom vs. Active Mission metadata.
        HOW: Regex-based state extraction to detect 'Context Drift'.
        WHY: Ensures the Engine's reality matches the Sovereign Law's intent.
        """
        report: Dict[str, Any] = {
            "timestamp": self.timestamp,
            "status": "INITIALIZING",
            "drift_detected": False,
            "entropy_level": 0.0,
            "findings": [],
        }

        try:
            # 1. Ingest the Flattened Loom Substrate
            loom_filename: str = "Flattened_Synarche_Synthesis_System_Loom.md"
            loom_path: str = os.path.join(self.root_dir, loom_filename)

            # Fallback check for alternate naming
            if not os.path.exists(loom_path):
                # Search for any .md file with 'Loom' in the name in root
                for filename in os.listdir(self.root_dir):
                    if "Loom" in filename and filename.endswith(".md"):
                        loom_path = os.path.join(self.root_dir, filename)
                        break

            if not os.path.exists(loom_path):
                raise FileNotFoundError(f"Loom substrate not found at {loom_path}")

            with open(loom_path, "r", encoding="utf-8") as f_loom:
                loom_content: str = f_loom.read()

            # 2. Extract State via Antigravity Anchors (Regex)
            mission_match: Optional[re.Match] = re.search(
                r"Active Mission:\s*(.*)", loom_content
            )
            phase_match: Optional[re.Match] = re.search(r"Phase:\s*(.*)", loom_content)

            loom_state: Dict[str, str] = {
                "mission": (
                    mission_match.group(1).strip() if mission_match else "UNKNOWN"
                ),
                "phase": phase_match.group(1).strip() if phase_match else "UNKNOWN",
            }

            # 3. Ingest Sovereign Law (Metadata)
            meta_filename: str = "task.md.metadata.json"
            meta_path: str = os.path.join(self.root_dir, meta_filename)

            if not os.path.exists(meta_path):
                # Check .agent/substrate/governance/
                alt_meta_path: str = os.path.join(
                    self.root_dir, ".agent", "substrate", "governance", meta_filename
                )
                if os.path.exists(alt_meta_path):
                    meta_path = alt_meta_path

            task_metadata: Dict[str, Any] = {"mission_id": "UNDEFINED"}
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f_meta:
                    task_metadata = json.load(f_meta)

            # 4. Conflict Resolution & Entropy Check
            target_mission: str = task_metadata.get("mission_id", "UNDEFINED")
            if loom_state["mission"] != target_mission:
                report["drift_detected"] = True
                report["entropy_level"] = float(report["entropy_level"]) + 0.5
                findings: List[str] = report["findings"]
                findings.append(
                    f"MISSION_DRIFT: Loom({loom_state['mission']}) != Law({target_mission})"
                )

            # 5. Final Synthesis Outcome
            report["status"] = "STABLE" if not report["drift_detected"] else "DEGRADED"
            self._log_selt_entry(report)

            return report

        except Exception as e:
            return {"status": "HALTED", "error": str(e)}

    def _log_selt_entry(self, data: Dict[str, Any]) -> None:
        """
        WHAT: Standardized Experience Log (SELT) generation.
        HOW: Appends formatted JSON results to the audit logs.
        """
        log_path: str = os.path.join(self.root_dir, "audit_log.txt")
        with open(log_path, "a", encoding="utf-8") as file_log:
            file_log.write(
                f"\n[SELT-LOG] {self.timestamp} | STATUS: {data['status']} | ENTROPY: {data['entropy_level']}\n"
            )


if __name__ == "__main__":
    engine: CoherentSynthesisEngine = CoherentSynthesisEngine()
    result: Dict[str, Any] = engine.synthesize_loom()
    print(f"CSE Synthesis Result: {json.dumps(result, indent=4)}")
