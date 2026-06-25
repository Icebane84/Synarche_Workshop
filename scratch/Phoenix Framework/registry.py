"""
phoenix_framework/commands/registry.py

Command Registry — the typed, versioned catalog of all GUCA commands.

Maps Phoenix 'GUCAv5.0 command library' to a runtime-queryable registry.
Commands are registered here and retrieved by the executor.
The registry enforces structural completeness at registration time.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from phoenix_framework.core.types import (
    CommandDefinition, RiskLevel, ImpactAssessment, ArtifactType
)


class DuplicateCommandError(Exception):
    pass

class CommandNotFoundError(Exception):
    pass


class CommandRegistry:
    """
    Central catalog of all executable commands.
    Thread-safe for read operations; registration is initialization-time only.
    """

    def __init__(self):
        self._commands: dict[str, CommandDefinition] = {}

    def register(self, cmd: CommandDefinition) -> None:
        if cmd.command_id in self._commands:
            raise DuplicateCommandError(
                f"Command '{cmd.command_id}' already registered. "
                "Bump the version and register with a new command_id."
            )
        self._commands[cmd.command_id] = cmd

    def get(self, command_id: str) -> CommandDefinition:
        if command_id not in self._commands:
            raise CommandNotFoundError(f"No command registered with id='{command_id}'")
        return self._commands[command_id]

    def list_by_domain(self, domain: str) -> list[CommandDefinition]:
        return [c for c in self._commands.values() if c.domain == domain]

    def list_by_risk(self, risk: RiskLevel) -> list[CommandDefinition]:
        return [c for c in self._commands.values() if c.risk_level == risk]

    def all(self) -> list[CommandDefinition]:
        return list(self._commands.values())


# ---------------------------------------------------------------------------
# Default Registry — built-in Phoenix commands, translated to typed defs
# ---------------------------------------------------------------------------

def build_default_registry() -> CommandRegistry:
    """
    Instantiates the canonical Phoenix command set.
    Each command maps a Phoenix GUCA entry to a fully typed CommandDefinition.
    """
    r = CommandRegistry()

    # ------------------------------------------------------------------
    # CMD: QueryCognitiveLoom  (Phoenix) → Semantic RAG Query (Industry)
    # ------------------------------------------------------------------
    r.register(CommandDefinition(
        command_name="Query Cognitive Loom",
        command_id="CMD-QCL-001",
        version="1.0.0",
        domain="Cognition",
        description=(
            "Natural language conceptual query against the knowledge base. "
            "Synthesizes answers by parsing relevant documents. "
            "Industry equivalent: RAG query endpoint."
        ),
        parameters={
            "query": {"type": "str", "required": True, "description": "Natural language query"},
            "max_results": {"type": "int", "required": False, "description": "Max docs to retrieve", "default": 5},
            "filters": {"type": "dict", "required": False, "description": "Metadata filters"},
        },
        expected_output={
            "answer": "str",
            "sources": "list[str]",
            "confidence": "float",
            "trace_id": "str",
        },
        success_criteria=[
            "answer is non-empty",
            "at least one source cited",
            "confidence > 0.5",
        ],
        potential_errors={
            "QCL-001": "Query too vague — no relevant documents retrieved",
            "QCL-002": "Knowledge base unavailable",
            "QCL-003": "Max token limit exceeded",
        },
        risk_level=RiskLevel.R1,
        impact=ImpactAssessment(
            security_impact="read-only",
            privacy_impact="none",
            compliance_impact="none",
            financial_impact="low-cost",
            ux_impact="latency-variable",
        ),
        requires_human_approval=False,
        auto_trigger_conditions=["user submits natural language question"],
        related_commands=["CMD-CW-001", "CMD-BGT-001"],
        adr_refs=["ADR-001"],
    ))

    # ------------------------------------------------------------------
    # CMD: ContextWeave  (Phoenix) → Context Window Management (Industry)
    # ------------------------------------------------------------------
    r.register(CommandDefinition(
        command_name="Context Weave",
        command_id="CMD-CW-001",
        version="1.0.0",
        domain="Cognition",
        description=(
            "Detects and flags inconsistencies or outdated information "
            "across the documentation registry. Stitches relevant context "
            "into the active reasoning window. "
            "Industry equivalent: RAG re-ranking + context stuffing."
        ),
        parameters={
            "document_ids": {"type": "list[str]", "required": True, "description": "Docs to weave"},
            "priority_weights": {"type": "dict", "required": False, "description": "Per-doc salience weights"},
        },
        expected_output={
            "woven_context": "str",
            "flagged_inconsistencies": "list[str]",
            "trace_id": "str",
        },
        success_criteria=[
            "woven_context fits within token budget",
            "all inconsistencies surfaced, not silently dropped",
        ],
        potential_errors={
            "CW-001": "Token budget exceeded — context truncated",
            "CW-002": "Circular document reference detected",
        },
        risk_level=RiskLevel.R2,
        impact=ImpactAssessment(
            security_impact="read-only",
            privacy_impact="none",
            compliance_impact="none",
            financial_impact="low-cost",
            ux_impact="minor-latency",
        ),
        requires_human_approval=False,
        auto_trigger_conditions=["CMD-QCL-001 invoked", "new session started"],
        related_commands=["CMD-QCL-001"],
        adr_refs=["ADR-001", "ADR-002"],
    ))

    # ------------------------------------------------------------------
    # CMD: Blueprint Generation Tool  (Phoenix) → Project Scaffolding (Industry)
    # ------------------------------------------------------------------
    r.register(CommandDefinition(
        command_name="Blueprint Generation Tool",
        command_id="CMD-BGT-001",
        version="1.0.0",
        domain="Meta-Cognition",
        description=(
            "Generates structured project blueprints from high-level directives. "
            "Industry equivalent: IaC template generator / project scaffolding CLI."
        ),
        parameters={
            "directive": {"type": "str", "required": True, "description": "High-level project goal"},
            "template_id": {"type": "str", "required": False, "description": "Base template to scaffold from"},
            "complexity_level": {"type": "int", "required": False, "description": "1–5 complexity scale"},
        },
        expected_output={
            "blueprint": "dict",
            "estimated_phases": "list[str]",
            "risk_assessment": "ImpactAssessment",
            "trace_id": "str",
        },
        success_criteria=[
            "blueprint includes all GUCAv5.0 required fields",
            "ADR references resolved",
            "risk level declared",
        ],
        potential_errors={
            "BGT-001": "directive too ambiguous to scaffold",
            "BGT-002": "template_id not found in registry",
        },
        risk_level=RiskLevel.R2,
        impact=ImpactAssessment(
            security_impact="none",
            privacy_impact="none",
            compliance_impact="none",
            financial_impact="low-cost",
            ux_impact="none",
        ),
        requires_human_approval=False,
        auto_trigger_conditions=[],
        related_commands=["CMD-QCL-001", "CMD-ET-001"],
        adr_refs=["ADR-001"],
    ))

    # ------------------------------------------------------------------
    # CMD: Calibrate Resonance Meter  (Phoenix) → Alignment Eval Run (Industry)
    # ------------------------------------------------------------------
    r.register(CommandDefinition(
        command_name="Calibrate Resonance Meter",
        command_id="CMD-CRM-001",
        version="1.0.0",
        domain="AI Alignment",
        description=(
            "Runs alignment evaluation against the active policy set. "
            "Produces a scored alignment report. "
            "Industry equivalent: RLHF reward model eval / alignment metric recalibration."
        ),
        parameters={
            "sample_size": {"type": "int", "required": False, "description": "Number of recent decisions to evaluate", "default": 50},
            "policy_subset": {"type": "list[str]", "required": False, "description": "Policy IDs to evaluate against"},
        },
        expected_output={
            "alignment_score": "float",     # 0.0–1.0
            "policy_compliance_pct": "float",
            "flagged_decisions": "list[str]",
            "trace_id": "str",
        },
        success_criteria=[
            "alignment_score >= 0.85",
            "all R5 commands show 100% policy_compliance",
        ],
        potential_errors={
            "CRM-001": "Insufficient decision history to evaluate",
            "CRM-002": "Policy set unavailable",
        },
        risk_level=RiskLevel.R2,
        impact=ImpactAssessment(
            security_impact="read-only",
            privacy_impact="none",
            compliance_impact="audit",
            financial_impact="low-cost",
            ux_impact="none",
        ),
        requires_human_approval=False,
        auto_trigger_conditions=["OMNI-LOG review triggered", "post-ADMP execution"],
        related_commands=["CMD-ET-001"],
        adr_refs=["ADR-003"],
    ))

    # ------------------------------------------------------------------
    # CMD: ENACT_TRANSCENDENCE  (Phoenix) → Governed Self-Modification (Industry)
    # Honest translation: this is a specification-generation command that
    # produces a human-reviewable change proposal, not runtime self-modification.
    # ------------------------------------------------------------------
    r.register(CommandDefinition(
        command_name="Enact Transcendence",
        command_id="CMD-ET-001",
        version="1.0.0",
        domain="Meta-Cognition",
        description=(
            "Generates a structured architectural change proposal for human review. "
            "Produces a 'Phenomenological Evolution Report' (change specification). "
            "Does NOT self-modify at runtime — produces a human-reviewable artifact. "
            "Industry equivalent: RFC / architectural change request with approval gate."
        ),
        parameters={
            "evolution_directive": {
                "type": "str",
                "required": True,
                "description": "URI or text describing the desired architectural change",
            },
            "authorization_key": {
                "type": "str",
                "required": True,
                "description": "Human-provided approval token",
            },
        },
        expected_output={
            "change_proposal": "dict",
            "risk_assessment": "ImpactAssessment",
            "rollback_plan": "str",
            "requires_human_approval": True,
            "trace_id": "str",
        },
        success_criteria=[
            "change_proposal includes rollback_plan",
            "authorization_key validated before execution",
            "all downstream command impacts assessed",
        ],
        potential_errors={
            "ET-001": "evolution_directive is malformed",
            "ET-002": "authorization_key invalid or missing",
            "ET-003": "SIVC detected policy violation in proposed change — rollback initiated",
        },
        risk_level=RiskLevel.R5,
        impact=ImpactAssessment(
            security_impact="architecture-modify",
            privacy_impact="audit-required",
            compliance_impact="full-review",
            financial_impact="high-cost",
            ux_impact="potential-context-reset",
        ),
        requires_human_approval=True,
        auto_trigger_conditions=[],   # P-GOV-002 enforces this is empty for R5
        related_commands=["CMD-CRM-001", "CMD-BGT-001"],
        adr_refs=["ADR-003", "ADR-004"],
    ))

    return r
