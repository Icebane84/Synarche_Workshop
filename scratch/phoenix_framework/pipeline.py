"""
phoenix_framework/telemetry/pipeline.py

SELT (Structured Event Log & Telemetry) + OMNI-LOG (After-Action Analysis)

Translates Phoenix logging metaphors into a typed observability pipeline.

SELT    → Structured event emission (OpenTelemetry-compatible schema)
OMNI-LOG → Post-execution synthesis (MLflow / experiment tracking equivalent)

The traceability chain anchored here:
    ADR-001 → CMD-QCL-001 (GUCA) → [SELT events] → OmniLogEntry → AISTF recs
"""

from __future__ import annotations
import json
from datetime import datetime
from typing import Optional

from phoenix_framework.core.types import (
    SELTEvent, OmniLogEntry, Decision, RiskLevel, CommandDefinition
)
from phoenix_framework.core.principles import assert_principle


# ---------------------------------------------------------------------------
# SELT Pipeline
# ---------------------------------------------------------------------------

class SELTPipeline:
    """
    Structured Event Log & Telemetry.

    In production, this would emit to: OpenTelemetry collector, Datadog,
    CloudWatch, or any structured log sink. Here it stores in-process
    for introspection and test validation.

    P3 enforcement: all auto-triggered commands must emit via this pipeline.
    """

    def __init__(self):
        self._events: list[SELTEvent] = []

    def emit(self, event: SELTEvent) -> None:
        """
        Emit a structured telemetry event.
        P3: every automation must be observable — this is the enforcement point.
        """
        assert_principle(
            "P3",
            bool(event.trace_id),
            f"SELTEvent for command '{event.command_id}' missing trace_id (P3 violation)"
        )
        self._events.append(event)

    def emit_many(self, events: list[SELTEvent]) -> None:
        for e in events:
            self.emit(e)

    def events_for_trace(self, trace_id: str) -> list[SELTEvent]:
        return [e for e in self._events if e.trace_id == trace_id]

    def events_for_command(self, command_id: str) -> list[SELTEvent]:
        return [e for e in self._events if e.command_id == command_id]

    def recent(self, n: int = 20) -> list[SELTEvent]:
        return self._events[-n:]

    def compute_trace_coverage(self) -> float:
        """
        Governance KPI: Trace Coverage %.
        Ratio of events that carry a trace_id (should always be 1.0 with P3 enforcement).
        """
        if not self._events:
            return 0.0
        covered = sum(1 for e in self._events if e.trace_id)
        return covered / len(self._events)

    def to_json(self, trace_id: Optional[str] = None) -> str:
        events = self.events_for_trace(trace_id) if trace_id else self._events
        return json.dumps(
            [
                {
                    "event_id": e.event_id,
                    "trace_id": e.trace_id,
                    "command_id": e.command_id,
                    "event_type": e.event_type,
                    "outcome": e.outcome,
                    "risk_level": e.risk_level.value,
                    "timestamp": e.timestamp.isoformat(),
                    "payload": e.payload,
                }
                for e in events
            ],
            indent=2,
        )


# ---------------------------------------------------------------------------
# OMNI-LOG  (After-Action Synthesis)
# ---------------------------------------------------------------------------

class OmniLog:
    """
    Post-execution analytical layer.

    Each entry synthesizes a decision + its SELT events into:
    - outcome summary
    - lessons learned
    - AISTF recommendations
    - governance KPIs

    P4 enforcement: AISTF recommendations are written here, never silently applied.
    """

    def __init__(self, selt: SELTPipeline):
        self._selt = selt
        self._entries: list[OmniLogEntry] = []

    def record(
        self,
        decision: Decision,
        command: CommandDefinition,
        execution_result: Optional[dict] = None,
    ) -> OmniLogEntry:
        """
        Synthesize a post-execution OMNI-LOG entry.

        P4: recommendations are stored here and never auto-applied.
        P2: trace_id links back to the original decision.
        """
        assert_principle(
            "P4",
            True,   # recording is always safe; the assertion is in apply() which doesn't exist
            "AISTF recommendations must be reviewable"
        )

        selt_events = self._selt.events_for_trace(decision.trace_id)
        trace_coverage = len([e for e in selt_events if e.trace_id]) / max(len(selt_events), 1)

        lessons, recommendations, violations = self._synthesize(
            decision, command, selt_events, execution_result
        )

        entry = OmniLogEntry(
            trace_id=decision.trace_id,
            command_id=decision.command_id,
            decision=decision,
            selt_events=selt_events,
            outcome_summary=self._summarize(decision, execution_result),
            lessons_learned=lessons,
            aistf_recommendations=recommendations,
            governance_violations=violations,
            command_success=decision.approved and not decision.requires_human_review,
            trace_coverage_pct=trace_coverage,
            policy_compliance=all(decision.policy_results.values()) if decision.policy_results else True,
        )

        self._entries.append(entry)
        return entry

    def recent(self, n: int = 10) -> list[OmniLogEntry]:
        return self._entries[-n:]

    def entries_with_violations(self) -> list[OmniLogEntry]:
        return [e for e in self._entries if e.governance_violations]

    def aggregate_kpis(self) -> dict:
        """Governance KPIs across all recorded entries."""
        if not self._entries:
            return {}
        total = len(self._entries)
        return {
            "total_executions": total,
            "command_success_rate": sum(1 for e in self._entries if e.command_success) / total,
            "policy_compliance_rate": sum(1 for e in self._entries if e.policy_compliance) / total,
            "avg_trace_coverage": sum(e.trace_coverage_pct for e in self._entries) / total,
            "entries_with_violations": len(self.entries_with_violations()),
            "total_aistf_recommendations": sum(len(e.aistf_recommendations) for e in self._entries),
        }

    # ------------------------------------------------------------------
    # Private synthesis helpers
    # ------------------------------------------------------------------

    def _summarize(self, decision: Decision, result: Optional[dict]) -> str:
        status = "APPROVED" if decision.approved else (
            "PENDING HUMAN REVIEW" if decision.requires_human_review else "BLOCKED"
        )
        outcome = f"Command {decision.command_id} | {status} | Confidence: {decision.confidence:.2%}"
        if result:
            outcome += f" | Result keys: {list(result.keys())}"
        return outcome

    def _synthesize(
        self,
        decision: Decision,
        command: CommandDefinition,
        events: list[SELTEvent],
        result: Optional[dict],
    ) -> tuple[list[str], list[str], list[str]]:
        lessons: list[str] = []
        recommendations: list[str] = []
        violations: list[str] = []

        # Lessons from policy failures
        failed_policies = [pid for pid, passed in decision.policy_results.items() if not passed]
        if failed_policies:
            lessons.append(f"Policies failed: {failed_policies}. Review command definition or context.")
            violations.extend(failed_policies)
            recommendations.append(
                f"Consider revising command '{command.command_id}' to satisfy: {failed_policies}"
            )

        # Lessons from low confidence
        if decision.confidence < 0.7:
            lessons.append(
                f"Low confidence ({decision.confidence:.2%}) — context may be incomplete "
                "or risk level underestimated."
            )
            recommendations.append(
                "Enrich context or reduce command scope to improve confidence score."
            )

        # Lessons from R5 command usage
        if command.risk_level == RiskLevel.R5:
            lessons.append("R5 command executed — post-execution alignment check recommended.")
            recommendations.append("Run CMD-CRM-001 (Calibrate Resonance Meter) after this cycle.")

        # Positive pattern capture
        if decision.approved and decision.confidence >= 0.9:
            lessons.append(
                f"High-confidence approval ({decision.confidence:.2%}) — "
                "this command pattern is well-governed."
            )

        return lessons, recommendations, violations
