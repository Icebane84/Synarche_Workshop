"""
phoenix_framework/core/types.py

Core type definitions — the canonical data contracts for the entire framework.
Every Phoenix artifact, command, and decision is typed here first.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional
import uuid


# ---------------------------------------------------------------------------
# Risk Classification  (replaces abstract "Critical/High" labels)
# ---------------------------------------------------------------------------

class RiskLevel(Enum):
    R1 = "informational"
    R2 = "low"
    R3 = "moderate"
    R4 = "high"
    R5 = "critical"


# ---------------------------------------------------------------------------
# Impact Assessment  (replaces "Ethical Impact Prediction")
# Concrete, measurable axes that can actually be instrumented.
# ---------------------------------------------------------------------------

@dataclass
class ImpactAssessment:
    security_impact: str       # e.g. "none", "read-only", "privilege-escalation"
    privacy_impact: str        # e.g. "none", "pii-read", "pii-write"
    compliance_impact: str     # e.g. "none", "gdpr", "hipaa"
    financial_impact: str      # e.g. "none", "low-cost", "high-cost"
    ux_impact: str             # e.g. "none", "latency-spike", "context-reset"

    def as_dict(self) -> dict:
        return {
            "security": self.security_impact,
            "privacy": self.privacy_impact,
            "compliance": self.compliance_impact,
            "financial": self.financial_impact,
            "ux": self.ux_impact,
        }


# ---------------------------------------------------------------------------
# Artifact Types  (separates documents from runtime from knowledge stores)
# ---------------------------------------------------------------------------

class ArtifactType(Enum):
    GOVERNANCE   = "governance"    # Documents: UMB, AOP, ADR
    RUNTIME      = "runtime"       # Execute: Commands, Policy Engine, DOL
    KNOWLEDGE    = "knowledge"     # Store state: SELT, Knowledge Graph, Memory


# ---------------------------------------------------------------------------
# Architectural Decision Record  (ADR — root of every traceability chain)
# ---------------------------------------------------------------------------

@dataclass
class ADR:
    """
    Architectural Decision Record.
    Maps to Phoenix 'Governing Ethos' + 'UMB' documents.
    Becomes the anchor for the full traceability chain:
        ADR → GUCA command → SELT event → OMNI-LOG entry → AISTF recommendation
    """
    adr_id: str
    title: str
    context: str
    decision: str
    consequences: str
    status: str = "accepted"      # proposed | accepted | deprecated | superseded
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.adr_id.startswith("ADR-"):
            raise ValueError(f"ADR IDs must start with 'ADR-', got: {self.adr_id}")


# ---------------------------------------------------------------------------
# GUCA Command Definition  (the Phoenix 'command' as an API contract)
# ---------------------------------------------------------------------------

@dataclass
class CommandDefinition:
    """
    Replaces the GUCA template fields with typed, executable Python dataclass.
    GUCA_VERSION, PRIMARY_DOMAIN_ALIGNMENT, etc. are preserved as metadata.
    What changes: every field is now machine-readable, not prose.
    """
    command_name: str
    command_id: str
    version: str
    domain: str                          # Cognition | Alignment | Meta-Cognition | Synergistic
    description: str
    parameters: dict[str, Any]          # param_name → {type, required, description}
    expected_output: dict[str, Any]
    success_criteria: list[str]
    potential_errors: dict[str, str]     # ERROR_CODE → description
    risk_level: RiskLevel
    impact: ImpactAssessment
    requires_human_approval: bool
    auto_trigger_conditions: list[str]   # empty = never auto-triggers
    related_commands: list[str]
    adr_refs: list[str]                  # which ADRs govern this command
    artifact_type: ArtifactType = ArtifactType.RUNTIME

    def requires_approval_for_risk(self) -> bool:
        return self.risk_level in (RiskLevel.R4, RiskLevel.R5) or self.requires_human_approval


# ---------------------------------------------------------------------------
# Decision  (output of the Decision Orchestration Layer)
# ---------------------------------------------------------------------------

@dataclass
class Decision:
    """
    The concrete output of the CSE, now called Decision Orchestration Layer.
    Every decision carries a trace_id linking back through the system.
    """
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_id: str = ""
    action: str = ""
    approved: bool = False
    confidence: float = 0.0            # 0.0–1.0
    justification: str = ""
    risk_level: RiskLevel = RiskLevel.R1
    impact: Optional[ImpactAssessment] = None
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    policy_results: dict[str, bool] = field(default_factory=dict)
    requires_human_review: bool = False


# ---------------------------------------------------------------------------
# SELT Event  (Structured Event Log & Telemetry — the observability record)
# ---------------------------------------------------------------------------

@dataclass
class SELTEvent:
    """
    Structured Event Log & Telemetry entry.
    Maps to Phoenix 'SELT logs' but enforces typed fields.
    Every command execution emits at least one SELT event.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    command_id: str = ""
    adr_ref: str = ""
    event_type: str = ""              # COMMAND_START | COMMAND_SUCCESS | COMMAND_FAIL | POLICY_BLOCK | HUMAN_GATE
    payload: dict[str, Any] = field(default_factory=dict)
    outcome: str = ""                 # success | failure | pending | blocked
    duration_ms: Optional[float] = None
    risk_level: RiskLevel = RiskLevel.R1
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# OMNI-LOG Entry  (After-action synthesis — one per command execution cycle)
# ---------------------------------------------------------------------------

@dataclass
class OmniLogEntry:
    """
    Post-execution analytical record.
    Maps to Phoenix 'OMNI_LOG Report'.
    Feeds the AISTF continuous improvement cycle.
    """
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    command_id: str = ""
    decision: Optional[Decision] = None
    selt_events: list[SELTEvent] = field(default_factory=list)
    outcome_summary: str = ""
    lessons_learned: list[str] = field(default_factory=list)
    aistf_recommendations: list[str] = field(default_factory=list)
    governance_violations: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Governance KPIs computed at write time
    command_success: bool = False
    trace_coverage_pct: float = 0.0
    policy_compliance: bool = True
