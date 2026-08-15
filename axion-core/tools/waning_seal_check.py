import sys
import os
import json
import hashlib
from datetime import datetime, timezone

# Rule IV: Standardize console encoding for Windows stability
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def verify_ledger_integrity(ledger_path):
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if not os.path.exists(ledger_path):
        return {"passed": True, "stale_count": 0, "results": []}
        
    with open(ledger_path, "r", encoding="utf-8") as f:
        try:
            ledger_data = json.load(f)
        except Exception as e:
            return {"passed": False, "stale_count": 1, "results": [], "error": f"Failed to parse JSON: {e}"}
            
    if not isinstance(ledger_data, dict) or "records" not in ledger_data:
        return {"passed": False, "stale_count": 1, "results": [], "error": "Ledger format must be a JSON object with 'records' key."}
    ledger = ledger_data["records"]
        
    results = []
    stale_count = 0
    for entry in ledger:
        rel_path = entry.get("artifact_path")
        expected_hash = entry.get("content_sha256")
        if not rel_path or not expected_hash:
            continue
            
        full_path = os.path.join(workspace_root, rel_path)
        if not os.path.exists(full_path):
            status = "STALE_VERIFICATION_VOID"
            stale_count += 1
        elif get_sha256(full_path) != expected_hash:
            status = "STALE_VERIFICATION_VOID"
            stale_count += 1
        else:
            status = "STILL_VALID"
            
        results.append({
            "artifact_path": rel_path,
            "status": status,
            "recorded_at": entry.get("verified_at", "UNKNOWN")
        })
        
    return {
        "passed": stale_count == 0,
        "stale_count": stale_count,
        "results": results
    }

def main():
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ledger_path = os.path.join(workspace_root, "_governance", "50_Logs", "LOG.MECS.LEDGER.json")
    
    report = verify_ledger_integrity(ledger_path)
    if "error" in report:
        print(f"CRITICAL: {report['error']}", file=sys.stderr)
        sys.exit(1)
        
    for res in report["results"]:
        if res["status"] == "STALE_VERIFICATION_VOID":
            print(f"STALE — VERIFICATION VOID, RE-RUN REQUIRED: {res['artifact_path']}")
        else:
            print(f"STILL_VALID: {res['artifact_path']}")
            
    print(f"\n--- [WANING SEAL DECAY CHECK] COMPLETE ---")
    print(f"Checked: {len(report['results'])} entries. Stale: {report['stale_count']}")
    if not report["passed"]:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
