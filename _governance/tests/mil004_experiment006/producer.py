"""
artifact_anchor:
  id: GVRN.TEST.MIL004.EXP006.PRODUCER
  version: v15.0 [OMEGA]
  provenance: '2026-08-16'
  domain: GVRN-TEST
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_TEST_COMPONENT
  relations:
    - GOVERNED_BY: CORE.Codex.Phoenix
    - EMBODIES: GVRN.HARMONIZATION.Milestone002.Contracts
"""

import datetime
import json
import sys
from pathlib import Path

# Add axion-core to Python path
repo_root = Path(__file__).resolve().parents[3]
axion_core_root = repo_root / "axion-core"
if str(axion_core_root) not in sys.path:
    sys.path.insert(0, str(axion_core_root))

from src.engine.types import CognitiveEvent, CognitiveState, CognitivePhase, MemoryPressureLevel
from src.engine.cognitive_scheduler import CognitiveScheduler
from src.cse.validators.governance_engine import GovernanceEngine, GovernanceRule

def run_composite_state_transition_experiment() -> dict:
    # 1. Initialize native GovernanceEngine using authoritative governance_rules.json
    gov_engine = GovernanceEngine()

    # 2. Instantiate native CognitiveScheduler wired with real GovernanceEngine
    scheduler = CognitiveScheduler(governance_engine=gov_engine)

    # --- SCENARIO 1: Nominal Control Case (Pressure = 0.40, Risk = 0.10) ---
    scheduler.state = CognitiveState()
    scheduler.state.memory_pressure = 0.40
    scheduler.state.active_nodes = 4000

    event_nominal = CognitiveEvent(
        event_id="e006-event-nominal-001",
        event_type="NOMINAL_EXPERIENCE",
        content="Continuous operational sensory ingestion under stable vitals.",
        source="Agent.SensoryStream",
        timestamp=datetime.datetime(2026, 8, 16, 14, 0, 0, tzinfo=datetime.timezone.utc),
        metadata={"risk_score": 0.10}
    )

    tick_res_nominal = scheduler.run_tick(event_nominal)
    state_nominal_verdicts = list(scheduler.state.governance_verdicts)
    state_nominal_hits = list(scheduler.state.pattern_hits)

    # --- SCENARIO 2: Critical Memory Stress Case (Pressure = 0.85, Risk = 0.10) ---
    scheduler.state = CognitiveState()
    scheduler.state.memory_pressure = 0.85  # Critical pressure (triggers GOV-002)
    scheduler.state.active_nodes = 8500

    event_stress = CognitiveEvent(
        event_id="e006-event-stress-002",
        event_type="MEMORY_STRESS_EXPERIENCE",
        content="Heavy associative ingestion triggering memory stress cascade.",
        source="Agent.MemoryStressTest",
        timestamp=datetime.datetime(2026, 8, 16, 14, 1, 0, tzinfo=datetime.timezone.utc),
        metadata={"risk_score": 0.10}
    )

    tick_res_stress = scheduler.run_tick(event_stress)
    state_stress_verdicts = list(scheduler.state.governance_verdicts)
    state_stress_hits = list(scheduler.state.pattern_hits)

    # --- SCENARIO 3: Memory Overflow Pressure Case (Pressure = 0.95, Risk = 0.10) ---
    scheduler.state = CognitiveState()
    scheduler.state.memory_pressure = 0.95  # Overflow pressure (triggers GOV-002 & GOV-007)
    scheduler.state.active_nodes = 9500

    event_overflow = CognitiveEvent(
        event_id="e006-event-overflow-003",
        event_type="OVERFLOW_EXPERIENCE",
        content="Overflow pressure exceeding 0.90 threshold for pattern mining.",
        source="Agent.MemoryOverflow",
        timestamp=datetime.datetime(2026, 8, 16, 14, 2, 0, tzinfo=datetime.timezone.utc),
        metadata={"risk_score": 0.10}
    )

    tick_res_overflow = scheduler.run_tick(event_overflow)
    state_overflow_verdicts = list(scheduler.state.governance_verdicts)
    state_overflow_hits = list(scheduler.state.pattern_hits)

    # --- SCENARIO 4: High-Risk Action Gating Case (Pressure = 0.40, Risk = 0.92) ---
    scheduler.state = CognitiveState()
    scheduler.state.memory_pressure = 0.40
    scheduler.state.active_nodes = 4000

    event_risk = CognitiveEvent(
        event_id="e006-event-risk-004",
        event_type="HIGH_RISK_ACTION_EXPERIENCE",
        content="Attempting destructive or unverified state reconfiguration.",
        source="Agent.RiskActor",
        timestamp=datetime.datetime(2026, 8, 16, 14, 3, 0, tzinfo=datetime.timezone.utc),
        metadata={"risk_score": 0.92}
    )

    tick_res_risk = scheduler.run_tick(event_risk)
    state_risk_verdicts = list(scheduler.state.governance_verdicts)

    # 3. Construct Wire Output Package
    output_pkg = {
        "producer_ground_truth": {
            "scenario_1_nominal": {
                "initial_pressure": 0.40,
                "event_id": event_nominal.event_id,
                "verdicts_count": len(state_nominal_verdicts),
                "pattern_hits_count": len(state_nominal_hits),
                "expected_verdicts": 0
            },
            "scenario_2_stress": {
                "initial_pressure": 0.85,
                "event_id": event_stress.event_id,
                "verdicts_count": len(state_stress_verdicts),
                "verdict_rules": [v["rule_id"] for v in state_stress_verdicts],
                "expected_verdicts": 1
            },
            "scenario_3_overflow": {
                "initial_pressure": 0.95,
                "event_id": event_overflow.event_id,
                "verdicts_count": len(state_overflow_verdicts),
                "verdict_rules": [v["rule_id"] for v in state_overflow_verdicts],
                "pattern_hits_count": len(state_overflow_hits),
                "expected_verdicts": 2
            },
            "scenario_4_risk": {
                "initial_risk": 0.92,
                "event_id": event_risk.event_id,
                "verdicts_count": len(state_risk_verdicts),
                "verdict_rules": [v["rule_id"] for v in state_risk_verdicts],
                "expected_verdicts": 1
            }
        },
        "wire_payload": {
            "scenario_nominal": {
                "contract_version": "v0.1",
                "initial_pressure": 0.40,
                "state": {
                    "contract_version": "v0.1",
                    "tick_count": scheduler.state.tick_count,
                    "active_nodes": 4000,
                    "attention_budget": scheduler.state.attention_budget,
                    "governance_verdicts": state_nominal_verdicts,
                    "pattern_hits": state_nominal_hits
                },
                "event": {
                    "contract_version": "v0.1",
                    "id": event_nominal.event_id,
                    "source": event_nominal.source,
                    "type": event_nominal.event_type,
                    "payload": event_nominal.content,
                    "timestamp": event_nominal.timestamp.isoformat()
                }
            },
            "scenario_stress": {
                "contract_version": "v0.1",
                "initial_pressure": 0.85,
                "state": {
                    "contract_version": "v0.1",
                    "tick_count": scheduler.state.tick_count,
                    "active_nodes": 8500,
                    "attention_budget": scheduler.state.attention_budget,
                    "governance_verdicts": [
                        {
                            "contract_version": "v0.1",
                            "rule_id": v["rule_id"],
                            "fired": True,
                            "effect": v["effect"],
                            "field": v["field"],
                            "actual": v["actual"],
                            "threshold": v["threshold"]
                        } for v in state_stress_verdicts
                    ],
                    "pattern_hits": state_stress_hits
                },
                "event": {
                    "contract_version": "v0.1",
                    "id": event_stress.event_id,
                    "source": event_stress.source,
                    "type": event_stress.event_type,
                    "payload": event_stress.content,
                    "timestamp": event_stress.timestamp.isoformat()
                }
            },
            "scenario_overflow": {
                "contract_version": "v0.1",
                "initial_pressure": 0.95,
                "state": {
                    "contract_version": "v0.1",
                    "tick_count": scheduler.state.tick_count,
                    "active_nodes": 9500,
                    "attention_budget": scheduler.state.attention_budget,
                    "governance_verdicts": [
                        {
                            "contract_version": "v0.1",
                            "rule_id": v["rule_id"],
                            "fired": True,
                            "effect": v["effect"],
                            "field": v["field"],
                            "actual": v["actual"],
                            "threshold": v["threshold"]
                        } for v in state_overflow_verdicts
                    ],
                    "pattern_hits": state_overflow_hits
                },
                "event": {
                    "contract_version": "v0.1",
                    "id": event_overflow.event_id,
                    "source": event_overflow.source,
                    "type": event_overflow.event_type,
                    "payload": event_overflow.content,
                    "timestamp": event_overflow.timestamp.isoformat()
                }
            },
            "scenario_risk": {
                "contract_version": "v0.1",
                "initial_risk": 0.92,
                "state": {
                    "contract_version": "v0.1",
                    "tick_count": scheduler.state.tick_count,
                    "active_nodes": 4000,
                    "attention_budget": scheduler.state.attention_budget,
                    "governance_verdicts": [
                        {
                            "contract_version": "v0.1",
                            "rule_id": v["rule_id"],
                            "fired": True,
                            "effect": v["effect"],
                            "field": v["field"],
                            "actual": v["actual"],
                            "threshold": v["threshold"]
                        } for v in state_risk_verdicts
                    ],
                    "pattern_hits": []
                },
                "event": {
                    "contract_version": "v0.1",
                    "id": event_risk.event_id,
                    "source": event_risk.source,
                    "type": event_risk.event_type,
                    "payload": event_risk.content,
                    "timestamp": event_risk.timestamp.isoformat()
                }
            }
        }
    }

    return output_pkg

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = run_composite_state_transition_experiment()
    out_path = Path(__file__).parent / "fixture.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"PRODUCER_SUCCESS: Composite transition fixture written to {out_path}")
