"""
artifact_anchor:
  id: TEST.TEST_CSE.001
  version: v15.0 [OMEGA]
  provenance: '2026-08-13'
  domain: TEST
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
"""

import asyncio
import io
import json
import os
import pytest

from .cse import async_main
from .engine.adaptive_opportunity_weave import AdaptiveOpportunityWeave
from .engine.coherence_attractor_core import CoherenceAttractorCore
from .engine.engine_v2 import CoherentSynthesisEngine
from .engine.methodology_selector import MethodologySelectorLayer, ReasoningArchetype
from .engine.reflexive_consequence_projector import ReflexiveConsequenceProjector
from .engine.telemetry_engine import TelemetryEngine
from .guca_command import (
    AuditCoherenceCommand,
    ContextWeaveCommand,
    EnactTranscendenceCommand,
    EthicalEvaluationCommand,
    GUCAExecutor,
    OmniLogCommand,
)


@pytest.fixture
def root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_cse_cli_bridge_synthesis(monkeypatch, capsys):
    """BDD: Validates the stdin -> cse.py -> stdout JSON pipeline."""
    mock_payload = {
        "blockId": "test-uuid-001",
        "data": {"element": "button", "actionType": "CLICK"},
    }
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(mock_payload)))
    asyncio.run(async_main())
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["status"] == "SYNTHESIZED"
    assert result["processedData"]["actionType"] == "CLICK"


def test_coherence_attractor_core(root_dir):
    """Validates CAC-001 calculates Coherence Index and Dissonance Quests properly."""
    cac = CoherenceAttractorCore(root_dir)
    loom_state = {"mission": "TEST_MISSION", "phase": "ALPHA"}
    result = cac.evaluate_coherence(loom_state)
    assert 0.0 <= result.coherence_index <= 1.0
    assert 0.0 <= result.contextual_integrity_score <= 1.0
    assert isinstance(result.dissonances, list)
    assert isinstance(result.dissonance_quests, list)


def test_reflexive_consequence_projector(root_dir):
    """Validates RCP-002 simulates consequence risks and flags high-impact mutations."""
    rcp = ReflexiveConsequenceProjector(root_dir)
    safe_action = {"name": "READ_STATE", "target_nodes": ["NodeA"], "type": "READ"}
    safe_res = rcp.simulate_action(safe_action, {})
    assert safe_res.is_safe is True
    assert safe_res.risk_score < 0.6

    risky_action = {
        "name": "REFACTOR_CODEX",
        "target_nodes": ["CODEX-001", "AxiomLock", "N1", "N2", "N3", "N4"],
        "type": "SELF_REFACTOR",
    }
    risky_res = rcp.simulate_action(risky_action, {"cognitive_load": 95.0})
    assert risky_res.is_safe is False
    assert len(risky_res.identified_risks) > 0


def test_adaptive_opportunity_weave(root_dir):
    """Validates AOW-003 computes GSS, SFR, and proposes reciprocal links."""
    aow = AdaptiveOpportunityWeave(root_dir)
    res = aow.analyze_synergies()
    assert 0.0 <= res.graph_synergy_score <= 1.0
    assert 0.0 <= res.synergy_flow_rate <= 1.0
    assert res.total_nodes > 0
    assert isinstance(res.proposed_links, list)


def test_methodology_selector():
    """Validates MSL-004 dynamic archetype routing (Athena's Gambit)."""
    msl = MethodologySelectorLayer()
    gov_task = {"domain": "GOVERNANCE_AUDIT", "strict_validation": True}
    gov_res = msl.select_methodology(gov_task)
    assert gov_res.selected_archetype == ReasoningArchetype.DETERMINISTIC_SYMBOLIC

    sec_task = {"domain": "SECURITY_REDTEAM"}
    sec_res = msl.select_methodology(sec_task)
    assert sec_res.selected_archetype == ReasoningArchetype.ETHICAL_REDTEAM

    trans_task = {"domain": "NARRATIVE_SYNTHESIS", "complexity": 0.95}
    trans_res = msl.select_methodology(trans_task)
    assert trans_res.selected_archetype == ReasoningArchetype.TRANSCENDENT_SYNTHESIS


def test_telemetry_engine():
    """Validates TEL-001 generates complete State Vector (V_State)."""
    tel = TelemetryEngine()
    sv = tel.compute_state_vector(
        cac_result={"coherence_index": 0.95, "entropy": 0.0, "dissonances": []},
        aow_result={"synergy_flow_rate": 0.92, "graph_synergy_score": 0.90},
        msl_result={"hybrid_model_score": 0.94},
        cognitive_load=22.0,
    )
    assert sv.system_status == "TRANSCENDENT"
    assert sv.coherence_index == 0.95
    assert sv.prestige_score == 1000


def test_guca_pipeline_execution(root_dir):
    """Validates GUCA executor runs the Phoenix Protocol command pipeline."""
    executor = GUCAExecutor()
    context = {
        "loom_state": {"mission": "SYNARCHE", "phase": "BETA"},
        "cac_engine": CoherenceAttractorCore(root_dir),
        "rcp_engine": ReflexiveConsequenceProjector(root_dir),
        "aow_engine": AdaptiveOpportunityWeave(root_dir),
        "telemetry_engine": TelemetryEngine(),
    }
    pipeline = [
        AuditCoherenceCommand(),
        ContextWeaveCommand(),
        EthicalEvaluationCommand(),
        OmniLogCommand(),
        EnactTranscendenceCommand(),
    ]
    res = executor.execute_commands(pipeline, context)
    assert "omni_log_report" in res
    assert res.get("transcendence_status") == "ASCENDED"


@pytest.mark.asyncio
async def test_full_engine_synthesize_task(root_dir):
    """Validates end-to-end task synthesis loop in engine_v2.py."""
    engine = CoherentSynthesisEngine(root_dir)
    task_spec = {
        "name": "EvolveCoreTopology",
        "domain": "TRANSCENDENT",
        "complexity": 0.85,
        "targets": ["UMB-CSE-001"],
    }
    result = await engine.synthesize_task(task_spec)
    assert result["status"] == "SYNTHESIZED"
    assert "telemetry" in result
    assert result["pipeline_summary"]["transcendence_status"] == "ASCENDED"
