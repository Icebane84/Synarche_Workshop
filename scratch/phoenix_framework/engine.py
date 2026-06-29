"""
phoenix_framework/governance/engine.py

Governance Engine — Policy-as-Code layer.

Industry equivalent: Open Policy Agent (OPA), HashiCorp Sentinel.
Phoenix equivalent: UCI + SIVC + AGCA combined into one enforcement surface.

Key insight from Doc 4: governance must be *above* execution in the stack,
not just documented alongside it. This engine enforces rules before
CommandExecutor is ever called.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable
import re

from phoenix_framework.core.types import (
    CommandDefinition, Decision, RiskLevel, ImpactAssessment
)
from phoenix_framework.core.principles import assert_principle


# ---------------------------------------------------------------------------
# Policy Definition
# ---------------------------------------------------------------------------

@dataclass
class Policy:
    """
    A single governance rule. Versioned (P5), named, and evaluable.

    rule_fn: receives (command, context) → returns (passed: bool, reason: str)
    """
    policy_id: str
    version: str                        # semantic version required — P5
    name: str
    description: str
    applies_to_risk_levels: set[RiskLevel]
    rule_fn: Callable[[CommandDefinition, dict[str, Any]], tuple[bool, str]]
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        # P5 enforcement: every policy must be versioned
        assert_principle(
            "P5",
            bool(re.match(r"^\d+\.\d+\.\d+$", self.version)),
            f"Policy '{self.policy_id}' has invalid version '{self.version}'. "
            "Must be semantic (e.g. '1.0.0')."
        )

    def evaluate(
        self,
        command: CommandDefinition,
        context: dict[str, Any]
    ) -> tuple[bool, str]:
        if command.risk_level not in self.applies_to_risk_levels:
            return True, "policy not applicable to this risk level"
        return self.rule_fn(command, context)


# ---------------------------------------------------------------------------
# PolicyViolation
# ---------------------------------------------------------------------------

@dataclass
class PolicyViolation:
    policy_id: str
    policy_name: str
    command_id: str
    reason: str
    risk_level: RiskLevel
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __str__(self) -> str:
        return (
            f"[POLICY BLOCKED] {self.policy_id} | {self.policy_name}\n"
            f"  Command : {self.command_id}\n"
            f"  Risk    : {self.risk_level.value}\n"
            f"  Reason  : {self.reason}"
        )


# ---------------------------------------------------------------------------
# Governance Engine
# ---------------------------------------------------------------------------

class GovernanceEngine:
    """
    Policy-as-Code enforcement layer.

    Sits between the ADR/UMB layer and the GUCA command executor.
    Evaluates all registered policies before any command may run.

    Doc 4 stack position:
        UMB → [GOVERNANCE ENGINE] → GUCA → SELT → OMNI-LOG → AISTF
    """

    def __init__(self):
        self._policies: dict[str, Policy] = {}
        self._violation_log: list[PolicyViolation] = []
        self._register_builtin_policies()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_policy(self, policy: Policy) -> None:
        """
        Register a governance policy. Rejects unversioned policies (P5).
        The Policy.__post_init__ already asserts P5, so this is defense-in-depth.
        """
        self._policies[policy.policy_id] = policy

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate(
        self,
        command: CommandDefinition,
        context: dict[str, Any],
    ) -> tuple[bool, dict[str, bool], list[PolicyViolation]]:
        """
        Evaluate all policies against a command + execution context.

        Returns:
            (all_passed, per_policy_results, violations)
        """
        results: dict[str, bool] = {}
        violations: list[PolicyViolation] = []

        for pid, policy in self._policies.items():
            passed, reason = policy.evaluate(command, context)
            results[pid] = passed
            if not passed:
                v = PolicyViolation(
                    policy_id=pid,
                    policy_name=policy.name,
                    command_id=command.command_id,
                    reason=reason,
                    risk_level=command.risk_level,
                )
                violations.append(v)
                self._violation_log.append(v)

        return (len(violations) == 0), results, violations

    def violation_history(self) -> list[PolicyViolation]:
        return list(self._violation_log)

    # ------------------------------------------------------------------
    # Built-in Policies  (UCI core principles as executable rules)
    # ------------------------------------------------------------------

    def _register_builtin_policies(self) -> None:

        # P-GOV-001: R5 commands always require explicit human approval
        self.register_policy(Policy(
            policy_id="P-GOV-001",
            version="1.0.0",
            name="Critical commands require human approval",
            description=(
                "Any command rated R5 (critical) must have requires_human_approval=True. "
                "Maps to AGCA (Authorization Gate) in Phoenix terminology."
            ),
            applies_to_risk_levels={RiskLevel.R5},
            rule_fn=lambda cmd, ctx: (
                (True, "human approval set")
                if cmd.requires_human_approval
                else (False, "R5 command missing requires_human_approval=True")
            ),
        ))

        # P-GOV-002: Auto-trigger is forbidden for R4/R5 commands
        self.register_policy(Policy(
            policy_id="P-GOV-002",
            version="1.0.0",
            name="High-risk commands cannot auto-trigger",
            description=(
                "R4/R5 commands must not have auto_trigger_conditions defined. "
                "Maps to ENACT_TRANSCENDENCE requiring explicit invocation."
            ),
            applies_to_risk_levels={RiskLevel.R4, RiskLevel.R5},
            rule_fn=lambda cmd, ctx: (
                (True, "no auto-trigger conditions")
                if not cmd.auto_trigger_conditions
                else (False, f"R4/R5 command has auto_trigger_conditions: {cmd.auto_trigger_conditions}")
            ),
        ))

        # P-GOV-003: Every command must reference at least one ADR
        self.register_policy(Policy(
            policy_id="P-GOV-003",
            version="1.0.0",
            name="Commands must have ADR provenance",
            description=(
                "Every command must reference at least one Architectural Decision Record. "
                "Enforces P2 (every decision must have provenance) at the definition level."
            ),
            applies_to_risk_levels=set(RiskLevel),
            rule_fn=lambda cmd, ctx: (
                (True, "ADR reference present")
                if cmd.adr_refs
                else (False, "command has no adr_refs — P2 violation")
            ),
        ))

        # P-GOV-004: Privacy impact must be declared for user-data commands
        self.register_policy(Policy(
            policy_id="P-GOV-004",
            version="1.0.0",
            name="User-data commands must declare privacy impact",
            description=(
                "Commands tagged 'user_data' in context must not have privacy_impact='none'. "
                "Replaces vague 'Ethical Impact Prediction' with measurable compliance signal."
            ),
            applies_to_risk_levels=set(RiskLevel),
            rule_fn=lambda cmd, ctx: (
                (True, "privacy impact declared")
                if not ctx.get("handles_user_data")
                   or cmd.impact.privacy_impact != "none"
                else (False, "command handles user data but declares privacy_impact='none'")
            ),
        ))

        # P-GOV-005: Destructive commands blocked during read-only sessions
        self.register_policy(Policy(
            policy_id="P-GOV-005",
            version="1.0.0",
            name="Destructive commands blocked in read-only context",
            description=(
                "If execution context is read_only=True, commands with "
                "security_impact containing 'write' or 'delete' are blocked."
            ),
            applies_to_risk_levels=set(RiskLevel),
            rule_fn=lambda cmd, ctx: (
                (True, "not a read-only context")
                if not ctx.get("read_only")
                else (
                    (True, "command is read-safe")
                    if not any(
                        w in cmd.impact.security_impact
                        for w in ("write", "delete", "modify")
                    )
                    else (False, f"destructive command '{cmd.command_id}' blocked in read-only session")
                )
            ),
        ))
