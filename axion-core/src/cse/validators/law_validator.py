"""
artifact_anchor:
  id: "GVRN.LAW.001"
  version: "v1.0.0"
  provenance: "2026-04-22"
  domain: "GVRN"
  celestial_class: "PLANET"
  tier: "AXIOMATIC"
  state: "PROPOSED"
  ethos: "LAW_ENFORCEMENT"
  relations:
    - type: "VALIDATES"
      node: "SYSTEM_RULES"
"""

import json
import os


class LawValidator:
    """
    WHAT: Cross-references Loom data against absolute Governance data.
    HOW: Compares ingested dictionary states with task.md.metadata.json.
    WHY: To identify 'Context Drift' and enforce Zero Entropy.
    """

    def __init__(self, root_dir: str):
        self.meta_path = os.path.join(root_dir, "task.md.metadata.json")

    def audit_drift(self, loom_state: dict) -> list:
        findings = []
        if not os.path.exists(self.meta_path):
            findings.append("CRITICAL: task.md.metadata.json is missing.")
            return findings

        with open(self.meta_path, encoding="utf-8") as f:
            metadata = json.load(f)

        target_mission = metadata.get("mission_id", "UNDEFINED")

        if loom_state.get("mission") != target_mission:
            findings.append(f"MISSION_DRIFT: Loom({loom_state.get('mission')}) != Law({target_mission})")

        return findings
