import asyncio
import hashlib
import json
import queue
import time
import traceback
from datetime import datetime

from .config import NODE_PRIORITY_RANKING, REPLAY_WINDOW_SECONDS
from .state import ImmutableKnowledgeSubstrate, SystemCausalEvent

# Globals shared between api and worker
substrate: ImmutableKnowledgeSubstrate | None = None
tx_queue: queue.Queue = queue.Queue(maxsize=10000)
active_sockets: set = set()
_sockets_lock = asyncio.Lock()
MAIN_EVENT_LOOP: asyncio.AbstractEventLoop | None = None

def _derive_fork_nonce(original_nonce: str) -> str:
    return hashlib.sha256(f"FORK:{original_nonce}".encode()).hexdigest()[:32]

def _is_valid_task(task: dict, current_time: float) -> bool:
    """Validates a task from the queue against freshness and nonce replay."""
    payload = task.get("payload", {})
    if abs(current_time - payload.get("timestamp", 0)) > REPLAY_WINDOW_SECONDS:
        return False
    if substrate and payload.get("nonce") in substrate.seen_nonces:
        return False
    if substrate and substrate.is_stasis_active():
        return False
    return True

def _handle_fork_logic(task: dict) -> bool:
    """
    Processes potential forks before a proposal is committed.
    Returns True if the task was handled as a fork, False otherwise.
    """
    if not substrate: return True

    p, node_origin = task["payload"], task.get("node_id", "LOCAL")
    entry_id, declared_parent = p.get("entry_id"), p.get("lineage", {}).get("parent_hash")

    if declared_parent == "ROOT_GENESIS" or entry_id not in substrate.node_registry:
        return False

    graph = substrate.node_registry[entry_id]
    current_tip_hash = graph.refs.get("main")

    if not current_tip_hash or declared_parent == current_tip_hash:
        return False

    if declared_parent not in graph.commits:
        print(f"[-] Fork Rejected: parent '{declared_parent}' not in DAG.")
        return True

    tip_block = graph.commits[current_tip_hash]
    try: tip_ts = datetime.fromisoformat(tip_block["compiled_timestamp"].replace("Z", "+00:00")).timestamp()
    except (ValueError, KeyError): tip_ts = 0.0

    incoming_ts = float(p.get("timestamp", 0))
    local_node_weight = NODE_PRIORITY_RANKING.get(tip_block.get("causal_trigger", "").replace("FORK_ISOLATION_", ""), 0)
    incoming_node_weight = NODE_PRIORITY_RANKING.get(node_origin, 0)

    if incoming_ts > tip_ts or (incoming_ts == tip_ts and incoming_node_weight > local_node_weight):
        print("[-] Branch Isolated: committing fork ref.")
        fork_id = substrate.total_blocks_processed
        fork_hash = hashlib.sha256(f"{fork_id}REGISTER_FORK{node_origin}{json.dumps(p, sort_keys=True)}".encode()).hexdigest()
        fork_nonce = _derive_fork_nonce(p["nonce"])

        compiled_block = {
            "entry_id": entry_id, "term": p["term"], "assertion": p["assertion"],
            "parent_hash": declared_parent, "causal_trigger": f"FORK_ISOLATION_{node_origin}",
            "justification": p["lineage"]["justification"], "event_hash": f"0x{fork_hash}",
            "compiled_timestamp": datetime.utcfromtimestamp(incoming_ts).isoformat() + "Z",
        }
        fork_payload = {
            "entry_id": entry_id, "branch_name": f"refs/forks/{fork_hash[:8]}",
            "compiled_block": compiled_block, "timestamp": p["timestamp"], "nonce": fork_nonce,
        }
        ev = SystemCausalEvent(fork_id, "REGISTER_FORK", fork_payload, node_id=node_origin, timestamp=p["timestamp"])
        if substrate.commit_validated_event(ev):
            gossip = json.dumps({"action_type": "REGISTER_FORK", "payload": fork_payload, "node_id": node_origin})
            asyncio.run(broadcast_to_peers(gossip))
    else:
        print("[-] Stale Fork Rejected or lost tie-breaker.")

    return True

async def broadcast_to_peers(message: str):
    """Safely broadcast a message to all connected websocket peers."""
    async with _sockets_lock:
        disconnected_sockets = set()
        for sock in active_sockets:
            try:
                await sock.send_text(message)
            except Exception:
                disconnected_sockets.add(sock)
        for sock in disconnected_sockets:
            active_sockets.discard(sock)

def single_writer_processing_loop():
    """Authoritative single-writer thread. All substrate mutations happen here."""
    global substrate
    if not substrate: return

    while True:
        try: task = tx_queue.get(timeout=1.0)
        except queue.Empty: continue

        try:
            action_type, p, node_origin = task["action_type"], task["payload"], task.get("node_id", "LOCAL")

            if not _is_valid_task(task, time.time()):
                continue

            if action_type == "SUBMIT_PROPOSAL":
                if _handle_fork_logic(task):
                    continue

            next_id = substrate.total_blocks_processed
            ev = SystemCausalEvent(next_id, action_type, p, node_id=node_origin, timestamp=p["timestamp"])

            if substrate.commit_validated_event(ev):
                if node_origin == "LOCAL":
                    gossip = json.dumps({"action_type": action_type, "payload": p, "node_id": "LOCAL"})
                    asyncio.run(broadcast_to_peers(gossip))

            if substrate.total_blocks_processed % 1000 == 0:
                substrate.generate_compacted_state_snapshot()

        except Exception:
            traceback.print_exc()
        finally:
            tx_queue.task_done()
