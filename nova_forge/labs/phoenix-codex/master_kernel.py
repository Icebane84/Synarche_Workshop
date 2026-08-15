"""
master_kernel.py — Phoenix Codex Operational Kernel
=====================================================

The authoritative lifecycle controller for the hardened substrate. Sits
between main.py (FastAPI bootstrap) and worker.py (single-writer loop),
owning the scheduled maintenance tasks that keep the substrate healthy
over long-running deployments.

Responsibilities:
  - Periodic nonce-store pruning (prevent unbounded growth of seen_nonces)
  - Proposal expiry sweeps (auto-expire VOTING proposals past VOTING_TIMEOUT)
  - Health telemetry heartbeats (broadcast substrate vitals to peers)
  - Signal-trap integration (SIGTERM / SIGINT -> graceful snapshot + shutdown)
  - Canary self-check on startup (validates substrate invariants)

Architecture contract:
  - All reads/writes to substrate go through substrate.lock (RLock)
  - Peer broadcasts are dispatched via MAIN_EVENT_LOOP.call_soon_threadsafe
  - This module MUST be imported by main.py and its `start()` coroutine
    awaited inside the FastAPI @app.on_event("startup") handler.

Version: 4.0.0-kernel
"""

import asyncio
import json
import signal
import traceback
import time
from datetime import datetime, timezone

from .config import REPLAY_WINDOW_SECONDS, VOTING_TIMEOUT_SECONDS
from . import worker

# -- Tunable intervals --------------------------------------------------------

NONCE_PURGE_INTERVAL_SECONDS: int = 60        # How often to evict expired nonces
PROPOSAL_EXPIRY_INTERVAL_SECONDS: int = 120   # How often to sweep stale proposals
HEARTBEAT_INTERVAL_SECONDS: int = 30          # How often to broadcast health to peers
CANARY_STARTUP_DELAY_SECONDS: float = 2.0     # Grace period before first canary check

# -- Internal state -----------------------------------------------------------

_kernel_tasks: list[asyncio.Task] = []
_shutdown_event: asyncio.Event | None = None


# =============================================================================
# MAINTENANCE COROUTINES
# =============================================================================

async def _nonce_purge_loop() -> None:
    """
    Periodically evicts nonces older than REPLAY_WINDOW_SECONDS from
    substrate.seen_nonces to prevent unbounded memory growth.

    Without this, a long-running node accumulates every nonce ever seen,
    which is a linear memory leak proportional to total transaction volume.
    """
    assert _shutdown_event is not None
    while not _shutdown_event.is_set():
        await asyncio.sleep(NONCE_PURGE_INTERVAL_SECONDS)
        if not worker.substrate:
            continue
        try:
            worker.substrate.purge_expired_nonces(time.time())
        except Exception:
            traceback.print_exc()


async def _proposal_expiry_loop() -> None:
    """
    Sweeps the proposal_registry and auto-expires any VOTING proposals
    that have exceeded VOTING_TIMEOUT_SECONDS.

    Resolves OPEN-2 from the v3.9.0 patch log: proposals that receive no
    finalize call were stuck in VOTING state indefinitely.
    """
    assert _shutdown_event is not None
    while not _shutdown_event.is_set():
        await asyncio.sleep(PROPOSAL_EXPIRY_INTERVAL_SECONDS)
        if not worker.substrate:
            continue
        try:
            current_time = time.time()
            expired_ids: list[int] = []
            with worker.substrate.lock:
                for pid, prop in worker.substrate.proposal_registry.items():
                    if (
                        prop["status"] == "VOTING"
                        and current_time - prop["unix_created"] > VOTING_TIMEOUT_SECONDS
                    ):
                        prop["status"] = "EXPIRED"
                        expired_ids.append(pid)
            if expired_ids:
                print(f"[KERNEL] Expired {len(expired_ids)} proposal(s): {expired_ids}")
        except Exception:
            traceback.print_exc()


async def _heartbeat_loop() -> None:
    """
    Broadcasts a compact substrate health snapshot to all connected peers
    at a regular interval. Allows remote nodes to detect stale primaries
    and monitor block height without polling HTTP endpoints.

    Packet format:
      { "action_type": "HEARTBEAT", "payload": { ...vitals... } }
    """
    assert _shutdown_event is not None
    while not _shutdown_event.is_set():
        await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
        if not worker.substrate or not worker.active_sockets:
            continue
        try:
            with worker.substrate.lock:
                vitals = {
                    "block_height": worker.substrate.total_blocks_processed,
                    "global_state_root": worker.substrate.global_state_root,
                    "is_stasis": worker.substrate.is_stasis_active(),
                    "peers_connected": len(worker.active_sockets),
                    "proposal_count": len(worker.substrate.proposal_registry),
                    "dlq_depth": len(worker.substrate.dead_letter_queue),
                    "kernel_timestamp": datetime.now(timezone.utc).isoformat(),
                }
            packet = json.dumps({"action_type": "HEARTBEAT", "payload": vitals})
            await worker.broadcast_to_peers(packet)
        except Exception:
            traceback.print_exc()


# =============================================================================
# STARTUP CANARY
# =============================================================================

async def _canary_check() -> None:
    """
    Runs a structural integrity check on the substrate shortly after startup.
    Validates:
      - Global state root is not the zero-hash sentinel (genesis committed)
      - Merkle leaf count is consistent with total_blocks_processed
      - Ledger is non-empty if blocks have been processed

    A failed canary logs a warning but does NOT halt the server — it is an
    observability signal, not a hard gate.
    """
    await asyncio.sleep(CANARY_STARTUP_DELAY_SECONDS)
    if not worker.substrate:
        print("[KERNEL] WARNING: Canary: substrate not initialized at check time.")
        return
    try:
        with worker.substrate.lock:
            zero_root = "0x" + "0" * 64
            height = worker.substrate.total_blocks_processed
            merkle_leaves = worker.substrate.merkle.leaf_count
            state_root = worker.substrate.global_state_root

        issues: list[str] = []
        if height > 0 and state_root == zero_root:
            issues.append("global_state_root is zero-sentinel despite height > 0")
        if height > 0 and merkle_leaves == 0:
            issues.append("merkle leaf count is 0 despite height > 0")
        if height > 0 and merkle_leaves != height:
            issues.append(
                f"merkle leaf count ({merkle_leaves}) != block height ({height})"
            )

        if issues:
            print("[KERNEL] WARNING: Canary FAILED — substrate invariant violations:")
            for issue in issues:
                print(f"           - {issue}")
        else:
            print(
                f"[KERNEL] OK: Canary passed — "
                f"height={height}, merkle_leaves={merkle_leaves}, "
                f"root={state_root[:18]}..."
            )
    except Exception:
        print("[KERNEL] WARNING: Canary raised exception:")
        traceback.print_exc()


# =============================================================================
# SIGNAL HANDLING
# =============================================================================

def _install_signal_handlers(loop: asyncio.AbstractEventLoop) -> None:
    """
    Installs SIGTERM and SIGINT handlers that trigger a clean shutdown:
    flush the snapshot, set the shutdown event, then let the server exit.

    Windows note: SIGTERM is not reliably delivered on Windows but SIGINT
    (Ctrl+C) is. Both are registered for correctness on Linux/macOS.
    """
    def _handle_signal(sig_name: str) -> None:
        print(f"\n[KERNEL] Signal {sig_name} received — initiating graceful shutdown.")
        if worker.substrate:
            print("[KERNEL] Flushing compacted snapshot...")
            worker.substrate.generate_compacted_state_snapshot()
            print("[KERNEL] Snapshot saved.")
        if _shutdown_event and not _shutdown_event.is_set():
            loop.call_soon_threadsafe(_shutdown_event.set)

    try:
        loop.add_signal_handler(signal.SIGTERM, lambda: _handle_signal("SIGTERM"))
        loop.add_signal_handler(signal.SIGINT,  lambda: _handle_signal("SIGINT"))
    except NotImplementedError:
        # Windows ProactorEventLoop does not support add_signal_handler
        print(
            "[KERNEL] Signal handlers not available on this platform (Windows). "
            "Use Ctrl+C for graceful shutdown."
        )


# =============================================================================
# PUBLIC API — called from main.py
# =============================================================================

async def start(loop: asyncio.AbstractEventLoop) -> None:
    """
    Starts all kernel maintenance coroutines as background asyncio Tasks.
    Must be awaited inside the FastAPI startup event handler, after the
    substrate and worker thread are initialized.

    Args:
        loop: The running event loop (from asyncio.get_running_loop() in startup).

    Example (in main.py)::

        from . import master_kernel

        @app.on_event("startup")
        async def bootstrap_operating_substrate() -> None:
            loop = asyncio.get_running_loop()
            worker.MAIN_EVENT_LOOP = loop
            worker.substrate = ImmutableKnowledgeSubstrate()
            worker.substrate.recover_local_journal_state()
            threading.Thread(target=worker.single_writer_processing_loop, daemon=True).start()
            # ... genesis block ...
            await master_kernel.start(loop)   # <-- mount the kernel
    """
    global _shutdown_event
    _shutdown_event = asyncio.Event()

    _install_signal_handlers(loop)

    _kernel_tasks.extend([
        asyncio.create_task(_nonce_purge_loop(),     name="kernel.nonce_purge"),
        asyncio.create_task(_proposal_expiry_loop(), name="kernel.proposal_expiry"),
        asyncio.create_task(_heartbeat_loop(),       name="kernel.heartbeat"),
        asyncio.create_task(_canary_check(),         name="kernel.canary"),
    ])

    print(
        f"[KERNEL] Phoenix Kernel v4.0.0 active — "
        f"{len(_kernel_tasks)} maintenance tasks scheduled."
    )


async def stop() -> None:
    """
    Cancels all running kernel tasks cleanly.
    Called from the FastAPI shutdown event handler.

    Example (in main.py)::

        @app.on_event("shutdown")
        async def graceful_shutdown() -> None:
            await master_kernel.stop()
            if worker.substrate:
                worker.substrate.generate_compacted_state_snapshot()
    """
    if _shutdown_event:
        _shutdown_event.set()

    for task in _kernel_tasks:
        if not task.done():
            task.cancel()

    if _kernel_tasks:
        await asyncio.gather(*_kernel_tasks, return_exceptions=True)
        _kernel_tasks.clear()

    print("[KERNEL] All kernel tasks stopped.")
