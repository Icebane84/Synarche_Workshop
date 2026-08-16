"""
Master Runner for MIL-004 Experiment 006:
Executes Composite State Transition Proof across CognitiveEvent -> CognitiveScheduler -> GovernanceVerdict.
"""

import json
import subprocess
import sys
from pathlib import Path

def run():
    sys.stdout.reconfigure(encoding="utf-8")
    script_dir = Path(__file__).parent
    producer_script = script_dir / "producer.py"
    consumer_script = script_dir / "consumer.mjs"
    results_file = script_dir / "results.json"

    python_exe = r"C:\DevEnvironments\master_env\Scripts\python.exe"

    print("=" * 80)
    print("PHOENIX SYNARCHE — MIL-004 / EXPERIMENT 006: COMPOSITE STATE TRANSITION PROOF")
    print("Target: CognitiveEvent -> CognitiveScheduler -> CognitiveState -> GovernanceVerdict")
    print("=" * 80)

    # 1. Execute Producer
    print("\n[STEP 1] Executing Python Native CognitiveScheduler Composite Loop...")
    p_proc = subprocess.run([python_exe, str(producer_script)], capture_output=True, text=True, encoding="utf-8")
    print(p_proc.stdout)
    if p_proc.returncode != 0:
        print(f"PRODUCER_ERROR: {p_proc.stderr}")
        sys.exit(1)

    # 2. Execute Consumer
    print("\n[STEP 2] Executing Node.js Multi-Contract Semantic Invariant Verifier...")
    c_proc = subprocess.run(["node", str(consumer_script)], capture_output=True, text=True, encoding="utf-8")
    print(c_proc.stdout)
    if c_proc.returncode != 0:
        print(f"CONSUMER_ERROR: {c_proc.stderr}")
        sys.exit(1)

    # 3. Output Results
    if results_file.exists():
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)

        print("\n[STEP 3] Empirical Verification Matrix:")
        print("-" * 80)
        for a in results["assertions"]:
            status_icon = "✓" if a["status"] == "PASSED" else "✗"
            print(f"  {status_icon} [{a['status']}] {a['name']}")
        print("-" * 80)
        print(f"Overall Result: {results['overall_status']}")
        print(f"Composite Invariants:")
        print(f"  • State-Dependent Causality: {results['composite_invariants']['state_dependent_causality_proven']}")
        print(f"  • Control Case Non-Firing:   {results['composite_invariants']['control_case_non_firing_proven']}")
        print(f"  • Governance Effect Propagation: {results['composite_invariants']['governance_side_effect_propagation_proven']}")
        print(f"  • Sibling Contract Conformance:  {results['composite_invariants']['sibling_contract_conformance_proven']}")
        print(f"  • Multi-Contract Semantic Integrity: {results['composite_invariants']['multi_contract_semantic_integrity_proven']}")
        print(f"Score: {results['passed_count']} / {results['total_assertions']} assertions passed.")
        print("=" * 80)

if __name__ == "__main__":
    run()
