"""
Master Runner for MIL-003 Experiment 002:
Executes Live Runtime Consumption of EventContract_v0_1 via NexusSignalBusClient.
"""

import json
import subprocess
import sys
from pathlib import Path

def run():
    sys.stdout.reconfigure(encoding="utf-8")
    script_dir = Path(__file__).parent
    ts_runner = script_dir / "experiment002.ts"
    results_file = script_dir / "results.json"

    print("=" * 80)
    print("PHOENIX SYNARCHE — MIL-003 / EXPERIMENT 002: RUNTIME INGESTION PROOF")
    print("Target: EventContract_v0_1 -> Adapter -> Live NexusSignalBusClient")
    print("=" * 80)

    # Execute with Node.js native TypeScript stripping
    cmd = ["node", "--experimental-strip-types", str(ts_runner)]
    print("\n[STEP 1] Executing Live NexusSignalBus Ingestion Harness...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(proc.stdout)
    if proc.returncode != 0:
        print(f"EXPERIMENT_ERROR: {proc.stderr}")
        sys.exit(1)

    # Read and output verification matrix
    if results_file.exists():
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)

        print("\n[STEP 2] Empirical Verification Matrix:")
        print("-" * 80)
        for a in results["assertions"]:
            status_icon = "✓" if a["status"] == "PASSED" else "✗"
            print(f"  {status_icon} [{a['status']}] {a['name']}")
        print("-" * 80)
        print(f"Overall Result: {results['overall_status']}")
        print(f"Boundary Integrity:")
        print(f"  • Acceptance Proven: {results['boundary_integrity']['acceptance_proven']}")
        print(f"  • Rejection Proven:  {results['boundary_integrity']['rejection_proven']}")
        print(f"  • Semantic Preservation: {results['boundary_integrity']['semantic_preservation_proven']}")
        print(f"Score: {results['passed_count']} / {results['total_assertions']} assertions passed.")
        print("=" * 80)

if __name__ == "__main__":
    run()
