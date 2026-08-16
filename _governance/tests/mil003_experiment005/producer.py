"""
artifact_anchor:
  id: GVRN.TEST.MIL003.EXP005.PRODUCER
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

import json
import sys
from pathlib import Path

# Add axion-core to Python path
repo_root = Path(__file__).resolve().parents[3]
axion_core_root = repo_root / "axion-core"
if str(axion_core_root) not in sys.path:
    sys.path.insert(0, str(axion_core_root))

from src.cse.validators.governance_engine import GovernanceRule, GovernanceVerdict

def create_and_serialize_governance_verdicts() -> dict:
    # 1. Define Rule: Pressure Gate (GOV-MEM-001)
    rule_pressure = GovernanceRule(
        rule_id="GOV-MEM-001",
        name="MemoryPressureGate",
        description="Gate non-critical cognitive tasks when memory pressure exceeds 0.75",
        field="memory_pressure",
        op="gt",
        value=0.75,
        effect="block_action",
        priority=80
    )

    # 2. Case A: Condition Triggered (State Pressure = 0.80 > 0.75)
    context_triggered = {"memory_pressure": 0.80, "tick_count": 142}
    fired_a = rule_pressure.evaluate(context_triggered)
    verdict_a = GovernanceVerdict(
        rule_id=rule_pressure.rule_id,
        effect=rule_pressure.effect,
        field=rule_pressure.field,
        actual=context_triggered["memory_pressure"],
        threshold=rule_pressure.value
    )

    # 3. Case B: Condition False (State Pressure = 0.50 <= 0.75)
    context_nominal = {"memory_pressure": 0.50, "tick_count": 143}
    fired_b = rule_pressure.evaluate(context_nominal)

    # 4. Case C: Context Drift Extension Case
    verdict_drift = {
        "contract_version": "v0.1",
        "rule_id": "GOV-LAW-002",
        "fired": True,
        "effect": "flag_dissonance",
        "field": "mission_alignment",
        "actual": "DRIFT_DETECTED",
        "threshold": "SYNARCHE",
        "extensions": {
            "drift": {
                "target_mission": "SYNARCHE",
                "findings": ["MISSION_DRIFT: Loom(SYNARCHE) != Law(UNDEFINED)"]
            }
        }
    }

    output_pkg = {
        "producer_ground_truth": {
            "case_a": {
                "rule_id": rule_pressure.rule_id,
                "fired": fired_a,
                "effect": rule_pressure.effect,
                "field": rule_pressure.field,
                "actual": 0.80,
                "threshold": 0.75,
                "expected_behavior": "VERDICT_ISSUED_NO_AUTOMATIC_EXECUTION"
            },
            "case_b": {
                "rule_id": rule_pressure.rule_id,
                "fired": fired_b,
                "field": rule_pressure.field,
                "actual": 0.50,
                "threshold": 0.75,
                "expected_behavior": "CONDITION_NOT_MET_NO_VERDICT"
            },
            "case_c": {
                "rule_id": "GOV-LAW-002",
                "fired": True,
                "effect": "flag_dissonance",
                "target_mission": "SYNARCHE"
            }
        },
        "wire_payload": {
            "verdict_triggered": {
                "contract_version": "v0.1",
                "rule_id": verdict_a.rule_id,
                "fired": fired_a,
                "effect": verdict_a.effect,
                "field": verdict_a.field,
                "actual": verdict_a.actual,
                "threshold": verdict_a.threshold
            },
            "rule_nominal_result": {
                "contract_version": "v0.1",
                "rule_id": rule_pressure.rule_id,
                "fired": fired_b,
                "effect": rule_pressure.effect,
                "field": rule_pressure.field,
                "actual": 0.50,
                "threshold": rule_pressure.value
            },
            "verdict_drift": verdict_drift
        }
    }

    return output_pkg

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = create_and_serialize_governance_verdicts()
    out_path = Path(__file__).parent / "fixture.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"PRODUCER_SUCCESS: Governance fixture written to {out_path}")
