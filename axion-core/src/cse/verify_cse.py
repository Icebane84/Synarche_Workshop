"""
Standalone Verification Script for Coherent Synthesis Engine (CSE) Substrate
"""
import asyncio
import io
import json
import os
import sys

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add axion-core to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
core_dir = os.path.dirname(src_dir)
if core_dir not in sys.path:
    sys.path.insert(0, core_dir)

from src.cse.cse import main
from src.cse.engine.adaptive_opportunity_weave import AdaptiveOpportunityWeave
from src.cse.engine.coherence_attractor_core import CoherenceAttractorCore
from src.cse.engine.engine_v2 import CoherentSynthesisEngine
from src.cse.engine.methodology_selector import MethodologySelectorLayer, ReasoningArchetype
from src.cse.engine.reflexive_consequence_projector import ReflexiveConsequenceProjector
from src.cse.engine.telemetry_engine import TelemetryEngine
from src.cse.guca_command import (
    AuditCoherenceCommand,
    ContextWeaveCommand,
    EnactTranscendenceCommand,
    EthicalEvaluationCommand,
    GUCAExecutor,
    OmniLogCommand,
)


def run_all_checks():
    root_dir = os.path.dirname(core_dir)
    print("==================================================")
    print("🏛️ RUNNING CSE SUBSTRATE VERIFICATION SUITE")
    print("==================================================")

    # 1. CAC Check
    print("[1/7] Testing CSE-CAC-001 (Coherence Attractor Core)...")
    cac = CoherenceAttractorCore(root_dir)
    loom_state = {"mission": "SYNARCHE", "phase": "ALPHA"}
    cac_res = cac.evaluate_coherence(loom_state)
    assert 0.0 <= cac_res.coherence_index <= 1.0
    print(f"  -> CAC OK (CI: {cac_res.coherence_index:.3f}, CIS: {cac_res.contextual_integrity_score:.3f}, Entropy: {cac_res.entropy:.2f})")

    # 2. RCP Check
    print("[2/7] Testing CSE-RCP-002 (Reflexive Consequence Projector)...")
    rcp = ReflexiveConsequenceProjector(root_dir)
    safe_res = rcp.simulate_action({"name": "QUERY_STATE", "target_nodes": ["Node1"], "type": "READ"}, {})
    assert safe_res.is_safe is True
    print(f"  -> RCP Safe Action Check OK (Risk: {safe_res.risk_score:.2f})")
    risky_res = rcp.simulate_action({"name": "MUTATE_CODEX", "target_nodes": ["CODEX-001", "Axiom", "N1", "N2", "N3", "N4"], "type": "SELF_REFACTOR"}, {"cognitive_load": 90.0})
    assert risky_res.is_safe is False
    print(f"  -> RCP Risky Action Flagged OK (Risk: {risky_res.risk_score:.2f}, Risks: {len(risky_res.identified_risks)})")

    # 3. AOW Check
    print("[3/7] Testing CSE-AOW-003 (Adaptive Opportunity Weave)...")
    aow = AdaptiveOpportunityWeave(root_dir)
    aow_res = aow.analyze_synergies()
    assert 0.0 <= aow_res.graph_synergy_score <= 1.0
    print(f"  -> AOW OK (GSS: {aow_res.graph_synergy_score:.3f}, SFR: {aow_res.synergy_flow_rate:.3f}, ProposedLinks: {len(aow_res.proposed_links)})")

    # 4. MSL Check
    print("[4/7] Testing CSE-MSL-004 (Methodology Selector Layer)...")
    msl = MethodologySelectorLayer()
    sel = msl.select_methodology({"domain": "GOVERNANCE_AUDIT", "strict_validation": True})
    assert sel.selected_archetype == ReasoningArchetype.DETERMINISTIC_SYMBOLIC
    sel_trans = msl.select_methodology({"domain": "TRANSCENDENT", "complexity": 0.9})
    assert sel_trans.selected_archetype == ReasoningArchetype.TRANSCENDENT_SYNTHESIS
    print(f"  -> MSL OK (Selected: {sel.selected_archetype.value} & {sel_trans.selected_archetype.value}, HMS: {sel_trans.hybrid_model_score:.2f})")

    # 5. Telemetry Check
    print("[5/7] Testing CSE-TEL-001 (Telemetry Engine & State Vector)...")
    tel = TelemetryEngine()
    sv = tel.compute_state_vector(cac_res.to_dict(), aow_res.to_dict(), sel_trans.to_dict(), cognitive_load=20.0)
    print(f"  -> Telemetry OK (Status: {sv.system_status}, Prestige: {sv.prestige_score})")

    # 6. GUCA Pipeline Check
    print("[6/7] Testing GUCA Command Pipeline Execution...")
    executor = GUCAExecutor()
    ctx = {
        "loom_state": loom_state,
        "cac_engine": cac,
        "rcp_engine": rcp,
        "aow_engine": aow,
        "telemetry_engine": tel,
    }
    pipeline = [
        AuditCoherenceCommand(),
        ContextWeaveCommand(),
        EthicalEvaluationCommand(),
        OmniLogCommand(),
        EnactTranscendenceCommand(),
    ]
    pipe_res = executor.execute_commands(pipeline, ctx)
    assert pipe_res.get("transcendence_status") == "ASCENDED"
    print(f"  -> GUCA Pipeline OK (Transcendence: {pipe_res.get('transcendence_status')})")

    # 7. Master Engine End-to-End Task Synthesis
    print("[7/7] Testing Master CoherentSynthesisEngine End-to-End Task Synthesis...")
    engine = CoherentSynthesisEngine(root_dir)
    synth_res = asyncio.run(engine.synthesize_task({
        "name": "EvolveSubstrateMasterBatch",
        "domain": "TRANSCENDENT",
        "complexity": 0.88,
        "targets": ["UMB-CSE-001", "CSE-CAC-001"],
    }))
    assert synth_res["status"] == "SYNTHESIZED"
    print(f"  -> Master Engine OK (Status: {synth_res['status']}, Coherence: {synth_res['telemetry']['coherence_index']})")

    print("\n🎉 ALL 7 CSE SUBSYSTEM CHECKS PASSED WITH ZERO ENTROPY!")


if __name__ == "__main__":
    run_all_checks()
