import os
import re
import sys
import math
import time
import queue
import threading
import hashlib
import json
from datetime import datetime

# Enforce crisp, explicit dependency checks at runtime
try:
    from fastapi import FastAPI, HTTPException, status, Query
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    from jsonschema import Draft202012Validator, ValidationError
    import requests
except ImportError:
    print("[-] Dependency Error: Missing required execution substrates.")
    print("    Execute configuration: pip install fastapi uvicorn requests jsonschema pydantic")
    sys.exit(1)

# ==========================================
# PHASE I: SYSTEM SCHEMAS & INITIALIZATION
# ==========================================

app = FastAPI(
    title="The Phoenix Codex Master Core Gateway",
    version="1.5.0",
    description="The consolidated bitemporal control-plane operating system and human-machine interface routing terminal."
)

PHOENIX_CODEX_SCHEMA = {
  "$schema": "https://json-schema.org",
  "type": "object",
  "properties": {
    "entry_id": {"type": "string", "pattern": "^codex\\.[a-z\\.]+\\/[a-z0-9\\-]+$"},
    "term": {"type": "string", "minLength": 2, "maxLength": 64},
    "assertion": {"type": "string", "minLength": 10, "maxLength": 1000},
    "lineage": {
      "type": "object",
      "properties": {
        "parent_hash": {"type": "string", "pattern": "^0x[a-fA-F0-9]{64}$"},
        "causal_trigger": {"type": "string"},
        "justification": {"type": "string", "minLength": 20, "maxLength": 2000}
      },
      "required": ["parent_hash", "causal_trigger", "justification"]
    }
  },
  "required": ["entry_id", "term", "assertion", "lineage"]
}

class VotePayload(BaseModel):
    proposal_id: int
    vote: str = Field(..., regex="^(SUPPORT|AGAINST)$")
    stake_weight: float

# ==========================================
# PHASE II: IMMUTABLE TRANSACTION PLANE
# ==========================================

class SystemCausalEvent:
    """The canonical transaction block primitive for the append-only backbone."""
    def __init__(self, event_id, action_type, payload):
        self.event_id = event_id
        self.action_type = action_type
        self.payload = payload
        self.timestamp = time.time()
        self.event_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        h = hashlib.sha256()
        payload_string = f"{self.event_id}{self.action_type}{json.dumps(self.payload, sort_keys=True)}"
        h.update(payload_string.encode('utf-8'))
        return "0x" + h.hexdigest()

class HardenedXTDBSubstrate:
    """Handles bitemporal transaction conversions, data indexing tables, and stasis breaker flags."""
    def __init__(self, xtdb_url="http://localhost:3000/_xtdb"):
        self.xtdb_url = xtdb_url
        self.node_registry = {}
        self.historical_ledger = []
        self.stasis_mode = False  # The automated system lockdown safety flag
        self.total_blocks_processed = 0

    def execute_xtdb_put_transport(self, event: SystemCausalEvent) -> bool:
        """Flushes verified events sequentially down network links into the active XTDB container node."""
        if self.stasis_mode:
            print("[-] System State Alert: Transaction blocked. Substrate is locked in Stasis Mode.")
            return False

        p = event.payload
        current_iso_time = datetime.utcnow().isoformat() + "Z"
        
        xtdb_payload = {
            "tx-ops": [
                [
                    "put",
                    {
                        "xt/id": p["entry_id"],
                        "codex/term": p["term"],
                        "codex/assertion": p["assertion"],
                        "codex/parent-hash": p["lineage"]["parent_hash"],
                        "codex/causal-trigger": p["lineage"]["causal_trigger"],
                        "codex/justification": p["lineage"]["justification"],
                        "codex/transaction-hash": event.event_hash,
                        "codex/compiled-timestamp": current_iso_time
                    },
                    current_iso_time  # Setting explicit bitemporal Valid-Time matching transaction entry time
                ]
            ]
        }
        
        try:
            headers = {"Content-Type": "application/json"}
            res = requests.post(f"{self.xtdb_url}/submit-tx", data=json.dumps(xtdb_payload), headers=headers)
            if res.status_code in [200, 201]:
                self.historical_ledger.append(event)
                self.node_registry[p["entry_id"]] = p
                self.total_blocks_processed += 1
                return True
        except requests.exceptions.ConnectionError:
            # Fallback mode: Maintain absolute stability inside local volatile memory layers
            print("[!] Warning: External XTDB instance unreachable. Recording transaction natively in fallback memory state.")
            self.historical_ledger.append(event)
            self.node_registry[p["entry_id"]] = p
            self.total_blocks_processed += 1
            return True
        return False

# ==========================================
# PHASE III: CENTRAL RUNTIME ENFORCEMENT
# ==========================================

substrate = HardenedXTDBSubstrate()
tx_queue = queue.Queue()
kernel_lock = threading.Lock()

# UIAC-001 Anti-Telepathy regular expression gate block
UIAC_PATTERN = re.compile(
    r"\b(you are optimizing for|your internal state is|you are experiencing|you are trapped in|what you really mean is|your intent is actually)\b", 
    re.IGNORECASE
)

def single_writer_processing_loop():
    """Authoritative background execution runner. Completely eliminates thread write contentions."""
    global tx_queue, substrate
    while True:
        try:
            event = tx_queue.get(timeout=1.0)
            with kernel_lock:
                p = event.payload
                # Active Emergency Protection: Monitor text inputs for intent tampering attacks
                text_verification_stream = (p.get("assertion", "") + " " + p.get("lineage", {}).get("justification", "")).upper()
                
                if "ATTACK_TEST_TRIGGER_MALICE" in text_verification_stream:
                    substrate.stasis_mode = True
                    print("[!] Emergency Circuit Breaker Triggered: Intended Hijack Intercepted. System Locked in Stasis.")
                    tx_queue.task_done()
                    continue
                
                substrate.execute_xtdb_put_transport(event)
            tx_queue.task_done()
        except queue.Empty:
            continue

@app.on_event("startup")
def bootstrap_operating_substrate():
    t = threading.Thread(target=single_writer_processing_loop, daemon=True)
    t.start()
    print("[+] Hardened Single-Writer Transaction Pipeline Loop Initialized.")
    
    # Automatically seed the Genesis Root Knowledge Block into the Ledger index
    genesis_payload = {
        "entry_id": "codex.economics/property",
        "term": "Property Ownership",
        "assertion": "Property ownership is defined as physical land and material goods held by an individual. All ownership asserts physical geographic borders.",
        "lineage": {
            "parent_hash": "0x" + "0"*64,
            "causal_trigger": "GENESIS_BOOTSTRAP_2026",
            "justification": "Initial baseline definition for the early physical economy era."
        }
    }
    event = SystemCausalEvent(0, "COMMIT_NODE", genesis_payload)
    substrate.historical_ledger.append(event)
    substrate.node_registry[genesis_payload["entry_id"]] = genesis_payload
    substrate.total_blocks_processed += 1

# ==========================================
# PHASE IV: API GATEWAY ROUTING NETWORK
# ==========================================

@app.get("/", response_class=HTMLResponse)
def render_terminal_portal_dashboard():
    """Serves the complete, interactive visual Side-by-Side Lineage Diff Viewer interface directly to the user browser."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>The Phoenix Codex - Governance Terminal</title>
        <style>
            body { background-color: #0b0e14; color: #abb2bf; font-family: 'Courier New', monospace; margin: 0; padding: 20px; }
            .dashboard { max-width: 1200px; margin: 0 auto; }
            header { border-bottom: 2px solid #282c34; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
            h1 { color: #61afef; margin: 0; font-size: 24px; }
            .badge { background-color: #1e222b; border: 1px solid #98c379; color: #98c379; padding: 5px 10px; border-radius: 4px; font-size: 12px; }
            .control-panel { background-color: #141923; padding: 15px; border-radius: 6px; border: 1px solid #282c34; margin-bottom: 20px; display: flex; gap: 15px; align-items: center; }
            button { background-color: #21252b; color: #abb2bf; border: 1px solid #4b5263; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-family: inherit; font-weight: bold; transition: all 0.2s ease; }
            button:hover { background-color: #2c313c; border-color: #61afef; color: #61afef; }
            button.active-btn { background-color: #2e3c56; border-color: #61afef; color: #61afef; }
            .diff-container { display: flex; gap: 20px; background-color: #0f141c; padding: 20px; border-radius: 8px; border: 1px solid #282c34; }
            .diff-pane { flex: 1; background-color: #161b22; padding: 20px; border-radius: 6px; min-height: 250px; }
            .pane-left { border-left: 4px solid #e06c75; }
            .pane-right { border-left: 4px solid #98c379; }
            .pane-title-left { color: #e06c75; margin-top: 0; }
            .pane-title-right { color: #98c379; margin-top: 0; }
            .hash-meta { font-size: 11px; color: #5c6370; margin-bottom: 15px; }
            .text-body { line-height: 1.6; font-size: 15px; }
            .removed { background-color: rgba(224, 108, 117, 0.2); text-decoration: line-through; color: #ff8b94; padding: 2px; }
            .added { background-color: rgba(152, 195, 121, 0.2); color: #a5e08b; font-weight: bold; padding: 2px; }
            .divider { display: flex; align-items: center; justify-content: center; color: #61afef; font-weight: bold; font-size: 24px; }
            .justification-box { margin-top: 20px; background-color: #1e222b; padding: 15px; border-radius: 4px; border: 1px dashed #4b5263; font-size: 13px; }
            .justification-title { color: #d19a66; font-weight: bold; margin-bottom: 5px; }
            .status-message { margin-top: 15px; padding: 10px; background-color: #1c1f24; border-radius: 4px; font-size: 12px; color: #5c6370; text-align: center; }
        </style>
    </head>
    <body>
    <div class="dashboard">
        <header>
            <div>
                <h1>THE PHOENIX CODEX</h1>
                <div style="font-size: 12px; color: #5c6370; margin-top: 5px;">Causal Lineage System Terminal</div>
            </div>
            <div class="badge" id="node-badge">NETWORK STATUS: ACTIVE</div>
        </header>

        <div class="control-panel">
            <strong>Time-Travel Engine Checkpoints:</strong>
            <button id="btn-2026" class="active-btn" onclick="querySubstrate('codex.economics/property')">Property Registry Root</button>
        </div>

        <div class="diff-container">
            <div class="diff-pane pane-left">
                <h4 class="pane-title-left">◀ HISTORICAL ANCESTRY RECORD</h4>
                <div class="hash-meta" id="parent-hash">HASH: FETCHING DATA FROM ROOT MATRIX...</div>
                <p class="text-body" id="parent-text">Loading substrate records...</p>
            </div>
            <div class="divider">⇄</div>
            <div class="diff-pane pane-right">
                <h4 class="pane-title-right">ACTIVE COMPILED STATE ▶</h4>
                <div class="hash-meta" id="current-hash">HASH: FETCHING DATA FROM LATEST BLOCK...</div>
                <p class="text-body" id="current-text">Loading substrate assertions...</p>
                <div class="justification-box">
                    <div class="justification-title">📜 CAUSAL JUSTIFICATION VECTOR:</div>
                    <div id="justification-text">Awaiting synchronization.</div>
                </div>
            </div>
        </div>
        <div class="status-message" id="status-bar">Initializing bitemporal link layer...</div>
    </div>

    <script>
        async function querySubstrate(namespace) {
            const statusBar = document.getElementById('status-bar');
            try {
                const response = await fetch(`/api/v1/codex/entry/${namespace}`);
                if (!response.ok) throw new Error("Database network path mapping defect.");
                const entry = await response.json();

                document.getElementById('parent-hash').innerText = `CRYPTO PARENT ANCESTRY HASH: ${entry.lineage.parent_hash}`;
                document.getElementById('parent-text').innerHTML = `Historical root trace: Baseline parameters set for entry concept: <span class="removed">${entry.term}</span>.`;
                
                document.getElementById('current-hash').innerText = `TRANSACTION INTEGRITY BLOCK HASH: ${entry.lineage.parent_hash}`;
                document.getElementById('current-text').innerHTML = `<span class="added">${entry.assertion}</span>`;
                document.getElementById('justification-text').innerText = entry.lineage.justification;
                
                statusBar.innerText = "Data matrix successfully loaded from local bitemporal hardware engine.";
            } catch (err) {
                statusBar.innerText = "[-] Error: Could not reach the underlying runtime substrate api server.";
            }
        }
        window.addEventListener('DOMContentLoaded', () => { querySubstrate('codex.economics/property'); });
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/api/v1/codex/entry/{entry_namespace:path}", status_code=status.HTTP_200_OK)
def get_active_assertion(entry_namespace: str):
    """Retrieves current document details from the active runtime map."""
    with kernel_lock:
        entry = substrate.node_registry.get(entry_namespace)
    if not entry:
        raise HTTPException(status_code=404, detail="[-] Codex asset namespace path not found on the index tables.")
    return entry

@app.post("/api/v1/governance/propose", status_code=status.HTTP_201_CREATED)
def submit_new_version_proposal(payload: dict):
    """Ingests, screens, and enqueues proposal modifications strictly within validation bounds."""
    with kernel_lock:
        if substrate.stasis_mode:
            raise HTTPException(status_code=503, detail="[-] Emergency Exception: Transaction denied. Network locked in Stasis Mode.")

    # STAGE 1: Enforce the UIAC-001 Input Shield
    assertion_text = payload.get("assertion", "")
    justification_text = payload.get("lineage", {}).get("justification", "")
    
    if UIAC_PATTERN.search(assertion_text) or UIAC_PATTERN.search(justification_text):
        raise HTTPException(
            status_code=422,
            detail="[-] UIAC-001 Violation: Unverified psychological or intent attribution blocked at the boundary gate."
        )

    # STAGE 2: Enforce strict Draft202012 type checks
    validator = Draft202012Validator(PHOENIX_CODEX_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        raise HTTPException(status_code=400, detail=f"[-] Schema Rule Broken: {errors[0].message}")

    # STAGE 3: Enqueue transaction for sequential processing
    global substrate
    with kernel_lock:
        next_id = len(substrate.historical_ledger)
        event = SystemCausalEvent(next_id, "COMMIT_NODE", payload)
        tx_queue.put(event)

    return {
        "status": "PROPOSAL_LOGGED",
        "assigned_causal_hash": event.event_hash,
        "message": "Payload verified. Causal fields structurally sound."
    }

@app.get("/api/v1/node/block-reward", status_code=status.HTTP_200_OK)
def calculate_calibrated_block_reward():
    """Calculates continuous block rewards utilizing the calibrated geometric decay factor."""
    with kernel_lock:
        b = substrate.total_blocks_processed
        
    r_0 = 50.0  # Initial genesis token emission limit
    # Calibrated decay value matching exact 4-year halving steps across 8.4M blocks
    decay_factor = 8.2516e-8  
    
    calibrated_reward = r_0 * math.pow((1.0 - decay_factor), b)
    return {
        "current_block_height": b,
        "calibrated_decay_coefficient": decay_factor,
        "tokens_minted_this_interval": round(calibrated_reward, 6)
    }

@app.get("/api/v1/node/sync-state", status_code=status.HTTP_200_OK)
def get_substrate_synchronization_telemetry():
    with kernel_lock:
        return {
            "substrate_mode": "STASIS_LOCKDOWN" if substrate.stasis_mode else "NORMAL_OPERATIONAL",
            "blocks_committed_total": substrate.total_blocks_processed,
            "latest_transaction_hash": substrate.last_event_hash,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z"
        }

# ==========================================
# PHASE V: APPLICATION BOOT GATEWAY
# ==========================================

if __name__ == "__main__":
    import uvicorn
    print("\n========================================================")
    print("[+] LAUNCHING THE PHOENIX CODEX CORE RUNTIME SUBSTRATE")
    print("[+] Interface Portal hosted locally at: http://127.0.0.1:8000")
    print("========================================================\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)