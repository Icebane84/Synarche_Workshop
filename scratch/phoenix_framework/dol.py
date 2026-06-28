"""
phoenix_framework/orchestration/dol.py

Decision Orchestration Layer (DOL)

Reframes the 'Coherent Synthesis Engine (CSE)' as a concrete engineering component.

Before this translation, CSE was described as:
    "a fractal coherence-seeking engine... the central gravity well of the system"

After this translation, it is:
    A typed input → processing → typed output component with measurable behavior.

Doc 4 proposed this exact reframe as the highest-value architectural change.
This module implements it.

Industry equivalents:
    - Rules engine (Drools, Easy Rules)
    - AI decision service (Azure Applied AI, AWS Bedrock Agents)
    - Workflow orchestrator (Temporal, Prefect)
"""

from __future__ import annotations
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

from phoenix_framework.core.types import (
    CommandDefinition, Decision, RiskLevel, SELTEvent, ImpactAssessment
)
from phoenix_framework.core.principles import assert_principle
from phoenix_framework.governance.engine import GovernanceEngine, PolicyViolation


# ---------------------------------------------------------------------------
# DOL Input  (typed — replaces prose 'user prompt + UCI feedback + knowledge bases')
# ---------------------------------------------------------------------------

@dataclass
class DOLInput:
    """
    Typed input to the Decision Orchestration Layer.

    Maps to CSE inputs: 'User prompt, Cognitive Loom, UCI Resonance Meter feedback,
    all Knowledge Bases' — but now machine-readable.
    """
    command_id: str
    parameters: dict[str, Any]
    context: dict[str, Any]              # execution context: read_only, user_id, session_id, etc.
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    adr_refs: list[str] = field(default_factory=list)
    requestor_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# DOL Output  (the concrete Decision — traceable, justified, scored)
# ---------------------------------------------------------------------------

# Decision is already defined in core/types.py — imported above.


# ---------------------------------------------------------------------------
# Decision Orchestration Layer
# ---------------------------------------------------------------------------

class DecisionOrchestrationLayer:
    """
    The renamed, reframed Coherent Synthesis Engine.

    Responsibilities (from Doc 4):
        Input:   telemetry, policy, context, commands
        Process: rule evaluation, context reconciliation, risk scoring,
                 workflow selection, recommendation generation
        Output:  decision, confidence, justification, trace_id

    This is no longer a "brain" metaphor. It is a decision service
    with typed I/O, measurable outputs, and full traceability.
    """

    def __init__(
        self,
        governance_engine: GovernanceEngine,
        risk_threshold_for_review: RiskLevel = RiskLevel.R4,
    ):
        self._gov = governance_engine
        self._risk_threshold = risk_threshold_for_review
        self._decision_history: list[Decision] = []

    # ------------------------------------------------------------------
    # Core Decision Method
    # ------------------------------------------------------------------

    def decide(
        self,
        inp: DOLInput,
        command: CommandDefinition,
    ) -> tuple[Decision, list[SELTEvent]]:
        """
        Produce a Decision for the given input + command definition.

        Steps:
            1. Assert P1 (trace_id present)
            2. Evaluate all governance policies
            3. Score risk and compute confidence
            4. Flag for human review if above threshold
            5. Return typed Decision + SELT events

        Returns (Decision, list[SELTEvent]) so the caller can persist both.
        """
        selt_events: list[SELTEvent] = []

        # --- P1: every action must be traceable ---
        assert_principle("P1", bool(inp.trace_id), "trace_id was empty in DOLInput")

        # --- SELT: decision start ---
        selt_events.append(SELTEvent(
            trace_id=inp.trace_id,
            command_id=inp.command_id,
            adr_ref=inp.adr_refs[0] if inp.adr_refs else "",
            event_type="DECISION_START",
            payload={"parameters": inp.parameters, "context_keys": list(inp.context.keys())},
            outcome="pending",
            risk_level=command.risk_level,
        ))

        # --- Governance evaluation ---
        all_passed, policy_results, violations = self._gov.evaluate(command, inp.context)

        if violations:
            selt_events.append(SELTEvent(
                trace_id=inp.trace_id,
                command_id=inp.command_id,
                event_type="POLICY_BLOCK",
                payload={"violations": [str(v) for v in violations]},
                outcome="blocked",
                risk_level=command.risk_level,
            ))

        # --- Risk scoring ---
        confidence = self._compute_confidence(command, policy_results, inp.context)
        risk_order = [RiskLevel.R1, RiskLevel.R2, RiskLevel.R3, RiskLevel.R4, RiskLevel.R5]
        needs_review = (
            risk_order.index(command.risk_level) >= risk_order.index(self._risk_threshold)
            or command.requires_human_approval
            or not all_passed
        )

        # --- Build decision ---
        decision = Decision(
            command_id=inp.command_id,
            action=command.command_name,
            approved=all_passed and not needs_review,
            confidence=confidence,
            justification=self._build_justification(command, policy_results, violations, confidence),
            risk_level=command.risk_level,
            impact=command.impact,
            trace_id=inp.trace_id,
            policy_results=policy_results,
            requires_human_review=needs_review,
        )

        self._decision_history.append(decision)

        # --- SELT: decision complete ---
        selt_events.append(SELTEvent(
            trace_id=inp.trace_id,
            command_id=inp.command_id,
            event_type="DECISION_COMPLETE",
            payload={
                "approved": decision.approved,
                "confidence": decision.confidence,
                "requires_human_review": decision.requires_human_review,
                "policy_results": policy_results,
            },
            outcome="success" if decision.approved else "blocked",
            risk_level=command.risk_level,
        ))

        return decision, selt_events

    # ------------------------------------------------------------------
    # Governance KPIs  (replaces vague 'UCI Resonance' with measurables)
    # ------------------------------------------------------------------

    def compute_kpis(self) -> dict[str, float]:
        """
        Governance KPIs as defined in Doc 4.
        Called by AISTF cycle and OMNI-LOG analysis.
        """
        if not self._decision_history:
            return {
                "command_success_rate": 0.0,
                "policy_compliance_pct": 0.0,
                "human_review_rate": 0.0,
                "avg_confidence": 0.0,
                "decision_count": 0,
            }

        total = len(self._decision_history)
        approved = sum(1 for d in self._decision_history if d.approved)
        compliant = sum(
            1 for d in self._decision_history
            if (all(d.policy_results.values()) if d.policy_results else True)
        )
        reviewed = sum(1 for d in self._decision_history if d.requires_human_review)
        avg_conf = sum(d.confidence for d in self._decision_history) / total

        return {
            "command_success_rate": approved / total,
            "policy_compliance_pct": compliant / total,
            "human_review_rate": reviewed / total,
            "avg_confidence": avg_conf,
            "decision_count": total,
        }

    def recent_decisions(self, n: int = 10) -> list[Decision]:
        return self._decision_history[-n:]

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _compute_confidence(
        self,
        command: CommandDefinition,
        policy_results: dict[str, bool],
        context: dict[str, Any],
    ) -> float:
        """
        Replaces vague 'InnerFlameScore' with a deterministic formula.

        Factors:
          - Policy pass rate (50% weight)
          - Risk level penalty (30% weight)
          - Context completeness (20% weight)
        """
        policy_score = (
            sum(policy_results.values()) / len(policy_results)
            if policy_results else 1.0
        )

        risk_penalties = {
            RiskLevel.R1: 0.00,
            RiskLevel.R2: 0.05,
            RiskLevel.R3: 0.15,
            RiskLevel.R4: 0.25,
            RiskLevel.R5: 0.40,
        }
        risk_score = 1.0 - risk_penalties[command.risk_level]

        required_keys = set(command.parameters.keys())
        provided_keys = set(context.keys()) | set(command.parameters.keys())
        context_score = len(required_keys & provided_keys) / max(len(required_keys), 1)

        confidence = (policy_score * 0.50) + (risk_score * 0.30) + (context_score * 0.20)
        return round(min(max(confidence, 0.0), 1.0), 4)

    def _build_justification(
        self,
        command: CommandDefinition,
        policy_results: dict[str, bool],
        violations: list[PolicyViolation],
        confidence: float,
    ) -> str:
        parts = [f"Command: {command.command_id} ({command.command_name})"]
        parts.append(f"Risk level: {command.risk_level.value}")
        parts.append(f"Confidence: {confidence:.2%}")

        if violations:
            parts.append("Policy violations:")
            for v in violations:
                parts.append(f"  - [{v.policy_id}] {v.reason}")
        else:
            parts.append(f"All {len(policy_results)} policies passed.")

        if command.requires_human_approval:
            parts.append("Human approval required before execution.")

        return "\n".join(parts)
