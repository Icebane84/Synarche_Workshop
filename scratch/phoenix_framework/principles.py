"""
phoenix_framework/core/principles.py

Architectural Principles — the invariants of the Phoenix framework.
These are not documentation. They are enforced at runtime.

Maps to Doc 4's "constitutional laws" above the governance stack.
Every component checks these before executing.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ArchitecturalPrinciple:
    id: str
    name: str
    description: str
    enforcement: str    # how the system enforces this principle in code


# The Five Invariants — frozen at framework initialization
PRINCIPLES: tuple[ArchitecturalPrinciple, ...] = (
    ArchitecturalPrinciple(
        id="P1",
        name="Every action must be traceable",
        description="No command executes without a trace_id linking ADR → GUCA → SELT → OMNI-LOG.",
        enforcement="CommandExecutor.execute() raises MissingTraceError if trace_id is absent.",
    ),
    ArchitecturalPrinciple(
        id="P2",
        name="Every decision must have provenance",
        description="Every Decision carries the policy results and ADR references that produced it.",
        enforcement="DecisionOrchestrationLayer.decide() populates policy_results before returning.",
    ),
    ArchitecturalPrinciple(
        id="P3",
        name="Every automation must be observable",
        description="Every auto-triggered command emits SELT events before and after execution.",
        enforcement="CommandExecutor wraps all execution in SELT emit calls via context manager.",
    ),
    ArchitecturalPrinciple(
        id="P4",
        name="Every recommendation must be reviewable",
        description="AISTF recommendations are stored in OMNI-LOG and never silently applied.",
        enforcement="AISTFCycle.recommend() writes to OmniLogEntry, never mutates CommandRegistry.",
    ),
    ArchitecturalPrinciple(
        id="P5",
        name="Every governance rule must be versioned",
        description="Policies carry a semantic version. The GovernanceEngine rejects unversioned rules.",
        enforcement="GovernanceEngine.register_policy() raises UnversionedPolicyError if version is absent.",
    ),
)


class PrincipleViolationError(Exception):
    """Raised when an action violates a core architectural principle."""
    def __init__(self, principle: ArchitecturalPrinciple, detail: str):
        self.principle = principle
        self.detail = detail
        super().__init__(
            f"[{principle.id}] {principle.name} — {detail}\n"
            f"Enforcement: {principle.enforcement}"
        )


def assert_principle(principle_id: str, condition: bool, detail: str) -> None:
    """
    Runtime enforcement of an architectural principle.
    Call at the top of any method that must satisfy an invariant.

    Usage:
        assert_principle("P1", trace_id is not None, "trace_id was None in execute()")
    """
    principle = next((p for p in PRINCIPLES if p.id == principle_id), None)
    if principle is None:
        raise ValueError(f"Unknown principle ID: {principle_id}")
    if not condition:
        raise PrincipleViolationError(principle, detail)
