"""
Master Runner for MIL-003 Experiment 005:
Executes Governance Evaluation, Verdict Reporting Boundary, and Execution Separation Proof.
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
    print("PHOENIX SYNARCHE — MIL-003 / EXPERIMENT 005: GOVERNANCE VERDICT PROOF")
    print("Target: GovernanceVerdict -> Wire -> GovernanceVerdictContract_v0_1")
    print("=" * 80)

    # 1. Execute Producer
    print("\n[STEP 1] Executing Python Governance Evaluation & Verdict Producer...")
    p_proc = subprocess.run([python_exe, str(producer_script)], capture_output=True, text=True, encoding="utf-8")
    print(p_proc.stdout)
    if p_proc.returncode != 0:
        print(f"PRODUCER_ERROR: {p_proc.stderr}")
        sys.exit(1)

    # 2. Execute Consumer
    print("\n[STEP 2] Executing Node.js Governance Verdict Consumer & Non-Execution Verifier...")
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
        print(f"Boundary Integrity:")
        print(f"  • Verdict Reporting Parity: {results['boundary_integrity']['verdict_reporting_parity_proven']}")
        print(f"  • Evaluation != Execution Separation: {results['boundary_integrity']['evaluation_vs_execution_separation_proven']}")
        print(f"  • Drift Extension Isolated: {results['boundary_integrity']['drift_extension_isolated']}")
        print(f"  • Negative Rejection Proven: {results['boundary_integrity']['negative_rejection_proven']}")
        print(f"Score: {results['passed_count']} / {results['total_assertions']} assertions passed.")
        print("=" * 80)

if __name__ == "__main__":
    run()
