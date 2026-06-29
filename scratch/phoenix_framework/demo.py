"""
demo.py — End-to-end Phoenix Framework demonstration

Shows the full governance stack in action:
    1. Framework bootstrap
    2. Low-risk command (passes governance)
    3. High-risk command (triggers human approval gate)
    4. Policy-blocked command (read-only violation)
    5. Governance KPIs
    6. Traceability chain: ADR → CMD → SELT → OMNI-LOG → AISTF
    7. AISTF recommendation review cycle
"""

import sys
import json
sys.path.insert(0, "/home/claude")

from phoenix_framework import PhoenixFramework, HumanApprovalRequired, PolicyBlockedError
from phoenix_framework.core.types import RiskLevel


def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ============================================================
# 1. Bootstrap
# ============================================================
separator("1. Bootstrapping Phoenix Framework")

fw = PhoenixFramework.build()
print("✓ Framework initialized")
print(f"  Commands registered : {len(fw.registry.all())}")
print(f"  Policies active     : {len(fw.governance._policies)}")
print(f"  Principles enforced :")
for p in fw.principles():
    print(f"    [{p['id']}] {p['name']}")


# ============================================================
# 2. Low-risk command — CMD-QCL-001 (Query Cognitive Loom)
# ============================================================
separator("2. Low-Risk Command: CMD-QCL-001 (Query Cognitive Loom)")

def mock_rag_handler(params, ctx):
    """Simulates a RAG retrieval."""
    return {
        "answer": f"Retrieved context for: {params['query']}",
        "sources": ["ADR-001", "UMB-ARCH-002"],
        "confidence": 0.91,
    }

result = fw.execute(
    command_id="CMD-QCL-001",
    parameters={"query": "What is the current architecture decision?"},
    context={"read_only": True, "session_id": "demo-001"},
    handler=mock_rag_handler,
    trace_id="TRACE-DEMO-001",
)

d = result["decision"]
print(f"  Trace ID     : {result['trace_id']}")
print(f"  Approved     : {d.approved}")
print(f"  Confidence   : {d.confidence:.2%}")
print(f"  Risk Level   : {d.risk_level.value}")
print(f"  Result       : {result['result']}")
print(f"\n  OMNI-LOG Summary:")
entry = result["omni_log_entry"]
print(f"    {entry.outcome_summary}")
if entry.lessons_learned:
    for lesson in entry.lessons_learned:
        print(f"    ✓ {lesson}")


# ============================================================
# 3. High-risk command — CMD-ET-001 (Enact Transcendence / R5)
# ============================================================
separator("3. R5 Command: CMD-ET-001 (Enact Transcendence) — Requires Human Approval")

try:
    fw.execute(
        command_id="CMD-ET-001",
        parameters={
            "evolution_directive": "Refactor the DOL risk scoring formula",
            "authorization_key": "",   # missing — intentional
        },
        context={"session_id": "demo-002"},
        trace_id="TRACE-DEMO-002",
    )
except HumanApprovalRequired as e:
    print(f"  ⚠  HumanApprovalRequired raised (expected):")
    print(f"     {e}")
    print(f"\n  Decision detail:")
    print(f"     Risk Level         : {e.decision.risk_level.value}")
    print(f"     Requires Review    : {e.decision.requires_human_review}")
    print(f"     Justification      :\n")
    for line in e.decision.justification.split("\n"):
        print(f"       {line}")

# Now re-submit with authorization
print("\n  Re-submitting with authorization_key...")
result_et = fw.execute(
    command_id="CMD-ET-001",
    parameters={
        "evolution_directive": "Refactor the DOL risk scoring formula",
        "authorization_key": "HUMAN-AUTH-TOKEN-XK9",
    },
    context={"session_id": "demo-002"},
    trace_id="TRACE-DEMO-002B",
    authorization_key="HUMAN-AUTH-TOKEN-XK9",
    handler=lambda p, c: {"change_proposal": "Draft RFC: DOL risk scoring v2", "rollback_plan": "revert to v1"},
)
print(f"  ✓ Approved after human gate: {result_et['decision'].approved}")
print(f"  Result: {result_et['result']}")


# ============================================================
# 4. Policy-blocked command — write op in read-only context
# ============================================================
separator("4. Policy Block: Write Command in Read-Only Context")

from phoenix_framework.core.types import ImpactAssessment, ArtifactType
from phoenix_framework.commands.registry import CommandDefinition

# Register a write-capable command for demo purposes
write_cmd = CommandDefinition(
    command_name="Delete User Record",
    command_id="CMD-DEL-001",
    version="1.0.0",
    domain="Data Management",
    description="Deletes a user record from the knowledge base.",
    parameters={"user_id": {"type": "str", "required": True}},
    expected_output={"deleted": "bool"},
    success_criteria=["record removed from store"],
    potential_errors={"DEL-001": "user_id not found"},
    risk_level=RiskLevel.R4,
    impact=ImpactAssessment(
        security_impact="delete",
        privacy_impact="pii-delete",
        compliance_impact="gdpr",
        financial_impact="none",
        ux_impact="irreversible",
    ),
    requires_human_approval=True,
    auto_trigger_conditions=[],
    related_commands=[],
    adr_refs=["ADR-002"],
)
fw.registry.register(write_cmd)

try:
    fw.execute(
        command_id="CMD-DEL-001",
        parameters={"user_id": "user-123"},
        context={"read_only": True, "session_id": "demo-003"},
        trace_id="TRACE-DEMO-003",
    )
except HumanApprovalRequired as e:
    print(f"  ⚠  HumanApprovalRequired (R4, expected before policy check).")
    # Re-submit with authorization to reach the policy check
    try:
        fw.execute(
            command_id="CMD-DEL-001",
            parameters={"user_id": "user-123"},
            context={"read_only": True, "session_id": "demo-003"},
            trace_id="TRACE-DEMO-003B",
            authorization_key="HUMAN-AUTH-TOKEN-XK9",
        )
    except PolicyBlockedError as pe:
        print(f"  ✓  PolicyBlockedError raised (expected):")
        print(f"     Violated policies: {pe.violations}")
        print(f"     Decision approved: {pe.decision.approved}")


# ============================================================
# 5. Traceability chain inspection
# ============================================================
separator("5. Traceability Chain — TRACE-DEMO-001")

trace_id = "TRACE-DEMO-001"
selt_events = fw.selt.events_for_trace(trace_id)
print(f"  SELT events for trace '{trace_id}':")
for evt in selt_events:
    print(f"    [{evt.event_type:25s}] outcome={evt.outcome:8s}  risk={evt.risk_level.value}")

omni_entries = [e for e in fw.omni_log.recent(20) if e.trace_id == trace_id]
if omni_entries:
    e = omni_entries[0]
    print(f"\n  OMNI-LOG entry:")
    print(f"    Outcome         : {e.outcome_summary}")
    print(f"    Policy compliant: {e.policy_compliance}")
    print(f"    Trace coverage  : {e.trace_coverage_pct:.0%}")
    if e.aistf_recommendations:
        print(f"    AISTF recs      :")
        for rec in e.aistf_recommendations:
            print(f"      → {rec}")


# ============================================================
# 6. Governance KPIs
# ============================================================
separator("6. Governance KPIs")

kpis = fw.governance_kpis()
print("  DOL KPIs:")
for k, v in kpis["dol"].items():
    val = f"{v:.2%}" if isinstance(v, float) and k != "decision_count" else v
    print(f"    {k:35s}: {val}")

print("\n  OMNI-LOG Aggregate:")
for k, v in kpis["omni_log"].items():
    val = f"{v:.2%}" if isinstance(v, float) and "rate" in k else v
    print(f"    {k:35s}: {val}")

print(f"\n  SELT Trace Coverage: {kpis['selt_trace_coverage']:.0%}")

print("\n  AISTF Cycle Summary:")
for k, v in kpis["aistf"].items():
    print(f"    {k:35s}: {v}")


# ============================================================
# 7. AISTF Recommendation Review
# ============================================================
separator("7. AISTF — Pending Recommendations")

pending = fw.aistf.pending_recommendations()
if pending:
    for rec in pending:
        print(f"  [{rec.rec_id}] {rec.priority.upper()} | {rec.category}")
        print(f"    {rec.recommendation}")
    # Accept first recommendation
    first = pending[0]
    fw.aistf.accept(first.rec_id, reviewer_id="human-reviewer-001")
    print(f"\n  ✓ Accepted '{first.rec_id}' (adoption rate: {fw.aistf.recommendation_adoption_rate():.0%})")
else:
    print("  No pending recommendations in this run.")

separator("Demo Complete")
print("  All five architectural principles enforced:")
for p in fw.principles():
    print(f"    [{p['id']}] {p['name']}")
print()
