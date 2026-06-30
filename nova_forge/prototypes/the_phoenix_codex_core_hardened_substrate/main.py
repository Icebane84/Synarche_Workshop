import asyncio
import sys
import threading
import time

from fastapi import FastAPI

try:
    from . import api, worker
    from .state import ImmutableKnowledgeSubstrate, SystemCausalEvent
except ImportError:
    print("[-] Failed to import local modules. Ensure you are running from the correct directory.")
    sys.exit(1)

app = FastAPI(
    title="The Phoenix Codex Core Hardened Substrate",
    version="4.0.0",
    description="The complete Git-for-Meaning platform. Features Ed25519 authentication, OPA gates, and rank-prioritized fork resolution."
)

app.include_router(api.router)

@app.on_event("startup")
async def bootstrap_operating_substrate() -> None:
    worker.MAIN_EVENT_LOOP = asyncio.get_running_loop()
    worker.substrate = ImmutableKnowledgeSubstrate()
    worker.substrate.recover_local_journal_state()

    threading.Thread(target=worker.single_writer_processing_loop, daemon=True).start()

    if worker.substrate.total_blocks_processed == 0:
        genesis_payload = {
            "entry_id": "codex.economics/property", "term": "Property Ownership",
            "assertion": "Property ownership is defined as physical land and material goods...",
            "nonce": "GENESIS_ROOT_INIT_NONCE_2026", "timestamp": int(time.time()),
            "lineage": {"parent_hash": "ROOT_GENESIS", "causal_trigger": "GENESIS_BOOTSTRAP_2026", "justification": "Initial baseline definition."}
        }
        event = SystemCausalEvent(0, "SUBMIT_PROPOSAL", genesis_payload, node_id="GENESIS", timestamp=genesis_payload["timestamp"])
        worker.substrate.commit_validated_event(event)
    print("[+] Phoenix Codex v4.0.0 — substrate active.")

@app.on_event("shutdown")
def graceful_shutdown() -> None:
    if worker.substrate:
        worker.substrate.generate_compacted_state_snapshot()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
