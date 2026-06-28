"""
phoenix_framework/__init__.py

Public API — bootstrap the full Phoenix framework in one call.

Usage:
    from phoenix_framework import PhoenixFramework

    fw = PhoenixFramework.build()
    result = fw.execute("CMD-QCL-001", {"query": "..."}, {"read_only": True})
"""

from __future__ import annotations
from typing import Any, Callable, Optional

from phoenix_framework.core.types import (
    ADR, RiskLevel, ImpactAssessment, ArtifactType,
    CommandDefinition, Decision, SELTEvent, OmniLogEntry
)
from phoenix_framework.core.principles import PRINCIPLES, assert_principle, PrincipleViolationError
from phoenix_framework.governance.engine import GovernanceEngine, Policy
from phoenix_framework.commands.registry import CommandRegistry, build_default_registry
from phoenix_framework.commands.executor import CommandExecutor, HumanApprovalRequired, PolicyBlockedError
from phoenix_framework.orchestration.dol import DecisionOrchestrationLayer
from phoenix_framework.telemetry.pipeline import SELTPipeline, OmniLog
from phoenix_framework.aistf.cycle import AISTFCycle


class PhoenixFramework:
    """
    Assembled Phoenix framework — the full Doc 4 governance stack.

    Internally wires:
        GovernanceEngine → DecisionOrchestrationLayer → CommandExecutor
                         → SELTPipeline → OmniLog → AISTFCycle
    """

    def __init__(
        self,
        registry: CommandRegistry,
        governance: GovernanceEngine,
        dol: DecisionOrchestrationLayer,
        selt: SELTPipeline,
        omni_log: OmniLog,
        aistf: AISTFCycle,
        executor: CommandExecutor,
    ):
        self.registry = registry
        self.governance = governance
        self.dol = dol
        self.selt = selt
        self.omni_log = omni_log
        self.aistf = aistf
        self._executor = executor

    @classmethod
    def build(cls, custom_registry: Optional[CommandRegistry] = None) -> "PhoenixFramework":
        """
        Bootstrap the framework with default components.
        Pass custom_registry to override the default command set.
        """
        registry  = custom_registry or build_default_registry()
        gov       = GovernanceEngine()
        dol       = DecisionOrchestrationLayer(gov)
        selt      = SELTPipeline()
        omni_log  = OmniLog(selt)
        aistf     = AISTFCycle(omni_log)
        executor  = CommandExecutor(registry, gov, dol, selt, omni_log, aistf)

        return cls(registry, gov, dol, selt, omni_log, aistf, executor)

    def execute(
        self,
        command_id: str,
        parameters: dict[str, Any],
        context: dict[str, Any],
        handler: Optional[Callable] = None,
        trace_id: Optional[str] = None,
        authorization_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Execute a command through the full governance stack."""
        return self._executor.execute(
            command_id=command_id,
            parameters=parameters,
            context=context,
            handler=handler,
            trace_id=trace_id,
            authorization_key=authorization_key,
        )

    def governance_kpis(self) -> dict:
        """Aggregate governance KPIs across OMNI-LOG and AISTF."""
        return {
            "dol": self.dol.compute_kpis(),
            "omni_log": self.omni_log.aggregate_kpis(),
            "aistf": self.aistf.summary(),
            "selt_trace_coverage": self.selt.compute_trace_coverage(),
        }

    def principles(self) -> list[dict]:
        """Return the architectural principles governing this instance."""
        return [
            {"id": p.id, "name": p.name, "enforcement": p.enforcement}
            for p in PRINCIPLES
        ]
