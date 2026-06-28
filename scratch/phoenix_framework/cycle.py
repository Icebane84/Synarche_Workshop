"""
phoenix_framework/aistf/cycle.py

AISTF (AI Self-Transformation Framework) — Continuous Improvement Cycle

Translates Phoenix 'AISTF Refinement Plan' into a typed improvement loop.

Industry equivalent:
    MLOps continuous improvement cycle / Kaizen loop
    Plan → Execute → Observe → Review → Improve

P4 enforcement: recommendations are surfaced here for human review,
never automatically applied to the command registry or governance engine.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from phoenix_framework.core.principles import assert_principle
from phoenix_framework.telemetry.pipeline import OmniLog


@dataclass
class AISTFRecommendation:
    """
    A single improvement recommendation produced by the AISTF cycle.
    Must be human-reviewed before any change is made (P4).
    """
    rec_id: str
    source_trace_id: str
    recommendation: str
    category: str          # "policy" | "command" | "architecture" | "process"
    priority: str          # "low" | "medium" | "high" | "critical"
    evidence: list[str]    # lessons_learned entries that produced this rec
    status: str = "pending"   # pending | accepted | rejected | deferred
    created_at: datetime = field(default_factory=datetime.utcnow)
    reviewed_at: datetime | None = None
    reviewer_id: str = ""


class AISTFCycle:
    """
    Continuous improvement engine.

    Reads OMNI-LOG entries → produces typed recommendations →
    stores them for human review → never self-applies changes.

    The key translation: Phoenix 'AISTF cycles' described as recursive
    self-improvement loops are here bounded by P4 (recommendations must
    be reviewable) and P1 (actions must be traceable).
    """

    def __init__(self, omni_log: OmniLog):
        self._omni_log = omni_log
        self._recommendations: list[AISTFRecommendation] = []
        self._cycle_count = 0

    def run_cycle(self, cycle_id: str | None = None) -> list[AISTFRecommendation]:
        """
        Execute one AISTF improvement cycle.

        Reads recent OMNI-LOG entries, distills recommendations,
        stores them for human review. Returns new recommendations only.

        P4: never mutates the registry or governance engine directly.
        """
        self._cycle_count += 1
        cycle_label = cycle_id or f"AISTF-CYCLE-{self._cycle_count:04d}"

        new_recs: list[AISTFRecommendation] = []

        for entry in self._omni_log.recent(n=50):
            for rec_text in entry.aistf_recommendations:
                # Deduplicate: don't re-emit the same recommendation
                if any(r.recommendation == rec_text for r in self._recommendations):
                    continue

                category = self._classify(rec_text)
                priority = self._prioritize(entry)

                rec = AISTFRecommendation(
                    rec_id=f"{cycle_label}-REC-{len(self._recommendations)+1:03d}",
                    source_trace_id=entry.trace_id,
                    recommendation=rec_text,
                    category=category,
                    priority=priority,
                    evidence=entry.lessons_learned,
                )
                self._recommendations.append(rec)
                new_recs.append(rec)

        return new_recs

    def accept(self, rec_id: str, reviewer_id: str) -> AISTFRecommendation:
        """Mark a recommendation as accepted by a human reviewer."""
        rec = self._get(rec_id)
        rec.status = "accepted"
        rec.reviewed_at = datetime.utcnow()
        rec.reviewer_id = reviewer_id
        return rec

    def reject(self, rec_id: str, reviewer_id: str) -> AISTFRecommendation:
        """Mark a recommendation as rejected."""
        rec = self._get(rec_id)
        rec.status = "rejected"
        rec.reviewed_at = datetime.utcnow()
        rec.reviewer_id = reviewer_id
        return rec

    def pending_recommendations(self) -> list[AISTFRecommendation]:
        return [r for r in self._recommendations if r.status == "pending"]

    def accepted_recommendations(self) -> list[AISTFRecommendation]:
        return [r for r in self._recommendations if r.status == "accepted"]

    def recommendation_adoption_rate(self) -> float:
        """Governance KPI: Recommendation Adoption Rate."""
        reviewed = [r for r in self._recommendations if r.status in ("accepted", "rejected")]
        if not reviewed:
            return 0.0
        accepted = [r for r in reviewed if r.status == "accepted"]
        return len(accepted) / len(reviewed)

    def summary(self) -> dict:
        return {
            "total_cycles": self._cycle_count,
            "total_recommendations": len(self._recommendations),
            "pending": len(self.pending_recommendations()),
            "accepted": len(self.accepted_recommendations()),
            "rejected": len([r for r in self._recommendations if r.status == "rejected"]),
            "adoption_rate": self.recommendation_adoption_rate(),
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get(self, rec_id: str) -> AISTFRecommendation:
        rec = next((r for r in self._recommendations if r.rec_id == rec_id), None)
        if not rec:
            raise KeyError(f"Recommendation '{rec_id}' not found")
        return rec

    def _classify(self, text: str) -> str:
        text_l = text.lower()
        if "policy" in text_l or "governance" in text_l:
            return "policy"
        if "command" in text_l or "cmd" in text_l:
            return "command"
        if "architecture" in text_l or "adr" in text_l:
            return "architecture"
        return "process"

    def _prioritize(self, entry: Any) -> str:
        from phoenix_framework.core.types import RiskLevel
        if entry.decision and entry.decision.risk_level == RiskLevel.R5:
            return "critical"
        if entry.governance_violations:
            return "high"
        if not entry.policy_compliance:
            return "medium"
        return "low"
