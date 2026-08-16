"""
Master Runner for MIL-003 Experiment 003:
Executes MemoryEntry Serialization -> MemoryNodeContract_v0_1 Deserialization -> Attention Formula Parity.
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
    print("PHOENIX SYNARCHE — MIL-003 / EXPERIMENT 003: STATE & DERIVATION PROOF")
    print("Target: Python MemoryEntry -> Wire -> TypeScript MemoryNodeContract_v0_1")
    print("=" * 80)

    # 1. Execute Producer
    print("\n[STEP 1] Executing Python Memory Producer & PAD-SIP Decay...")
    p_proc = subprocess.run([python_exe, str(producer_script)], capture_output=True, text=True, encoding="utf-8")
    print(p_proc.stdout)
    if p_proc.returncode != 0:
        print(f"PRODUCER_ERROR: {p_proc.stderr}")
        sys.exit(1)

    # 2. Execute Consumer
    print("\n[STEP 2] Executing Node.js MemoryNode Consumer & Formula Verifier...")
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
        print(f"  • Persisted State Preserved: {results['boundary_integrity']['persisted_state_preserved']}")
        print(f"  • Derived Non-Authority Proven: {results['boundary_integrity']['derived_state_non_authority_proven']}")
        print(f"  • Lifecycle Rules Deterministic: {results['boundary_integrity']['lifecycle_rules_deterministic']}")
        print(f"  • PAD-SIP Formula Parity: {results['boundary_integrity']['mathematical_formula_parity']}")
        print(f"Score: {results['passed_count']} / {results['total_assertions']} assertions passed.")
        print("=" * 80)

if __name__ == "__main__":
    run()
