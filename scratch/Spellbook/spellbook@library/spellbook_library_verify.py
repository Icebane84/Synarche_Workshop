#!/usr/bin/env python3
"""
spellbook_library_verify.py — a real @library port.

The Spellbook framework's @library port is currently specified as a JSON
block the model writes as prose alongside @bridge code — e.g. the boss
orchestrator doc's "integrity_deviation_rate": 0.00, asserted in the same
turn that @bridge called two methods that don't exist. That's not
telemetry; it's the model grading its own homework.

This script is what @library should actually be: it runs @bridge's header
and source through the MECS structural gate (ue_ast_auditor.py) and the API
surface gate (symbol_verifier.py), measures real wall-clock time for each,
computes violation counts from what those gates actually found, hashes the
audited files so the log is bound to the exact content it describes, and
ONLY THEN writes the telemetry JSON. If a gate fails, the log says so, in
full, with line numbers — it does not get to report a clean deviation rate
for content that didn't pass.

There is no self-report path. If you skip this script, you don't get a
@library log; you get nothing, which is the correct failure mode for
telemetry that was never measured.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent


def sha256_of(*paths: Path) -> str:
    h = hashlib.sha256()
    for p in paths:
        if p and p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()


def run_gate(cmd: list[str]) -> dict:
    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {"raw_stdout": proc.stdout, "raw_stderr": proc.stderr}
    return {"returncode": proc.returncode, "elapsed_seconds": round(elapsed, 4), "output": payload}


def main():
    parser = argparse.ArgumentParser(description="Real @library telemetry generator")
    parser.add_argument("--header", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--session-id", type=str, default="SPELLBOOK-LOCAL-SESSION")
    parser.add_argument("--applied-mask", type=str, default="UNSPECIFIED")
    args = parser.parse_args()

    if not args.header.exists():
        print(f"ERROR: header not found: {args.header}", file=sys.stderr)
        sys.exit(2)
    if not args.source.exists():
        print(f"ERROR: source not found: {args.source}", file=sys.stderr)
        sys.exit(2)

    content_hash = sha256_of(args.header, args.source)

    gate1 = run_gate([sys.executable, str(HERE / "ue_ast_auditor.py"),
                       str(args.header), str(args.source), "--json"])
    gate_api = run_gate([sys.executable, str(HERE / "symbol_verifier.py"),
                          "--header", str(args.header), "--source", str(args.source), "--json"])

    ast_violations = gate1["output"].get("violations", [])
    api_findings = gate_api["output"].get("findings", [])
    api_critical = [f for f in api_findings if f.get("status") == "CRITICAL"]
    api_unverified = [f for f in api_findings if f.get("status") == "UNVERIFIED"]

    total_checks = len(ast_violations) + len(api_findings)
    total_deviations = len(ast_violations) + len(api_critical)
    # Real ratio, not a placeholder. 0.00 only if there is something to have
    # checked AND nothing deviated. If nothing was checked, say so — don't
    # report a rate for zero denominator as if it were a clean pass.
    if total_checks == 0:
        integrity_deviation_rate = None
        integrity_note = "No manifest-tracked calls or AST-auditable constructs found — rate undefined, not zero."
    else:
        integrity_deviation_rate = round(total_deviations / total_checks, 4)
        integrity_note = None

    gates_passed = (gate1["returncode"] == 0) and (len(api_critical) == 0)

    library_log = {
        "audit_id": f"SRK-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{args.session_id}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "applied_mask": args.applied_mask,
        "content_sha256": content_hash,
        "verification_method": "measured: ue_ast_auditor.py + symbol_verifier.py subprocess execution",
        "telemetry_metrics": {
            "gate1_ast_audit_elapsed_seconds": gate1["elapsed_seconds"],
            "gate_api_verifier_elapsed_seconds": gate_api["elapsed_seconds"],
            "total_checks_run": total_checks,
            "total_deviations_found": total_deviations,
            "integrity_deviation_rate": integrity_deviation_rate,
            "integrity_deviation_rate_note": integrity_note,
        },
        "gates_passed": gates_passed,
        "ast_violations": ast_violations,
        "api_surface_findings": {
            "critical": api_critical,
            "unverified": api_unverified,
        },
    }

    print(json.dumps({"library_log": library_log}, indent=2))
    sys.exit(0 if gates_passed else 1)


if __name__ == "__main__":
    main()
