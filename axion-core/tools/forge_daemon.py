"""---
# Block A: Universal Identification & Provenance (UIP-V15)
artifact_anchor:
  id: "INFR.FORGE.DAEMON.001"
  version: "v15.0 [OMEGA]"
  provenance: "2026-04-23"
  domain: "INFRA"
  celestial_class: "STAR"
  tier: "COMPUTE"
  state: "CANONIZED"
  ethos: "ZERO-ENTROPY"
  relations:
    - type: "DEPENDS_ON"
      node: "TOOL.Forge.SourceMap"
    - type: "DEPENDS_ON"
      node: "CODEX-LAW-03"
    - type: "SYNERGIZES"
      node: "GVRN.CI.ForgePR"
    - type: "SYNERGIZES"
      node: "NEXUS.Worker.Handshake".
---

TOOL.Forge.Daemon — The Live Compiler Daemon
=============================================
Canonical path: @system/ (axion-core/tools/forge_daemon.py)

Watches the workspace for file saves via watchdog, debounces and
re-executes forge_all.py, then broadcasts compile status to all
authenticated IDE WebSocket clients.

FIX v1.2.0: Replaced hardcoded relative path "tools/forge_all.py" with
FORGE_ROOT env var for Zero-Gravity Portability (CODEX-LAW-03).

Security Note (@shield/ROTATE): SYSTEMIC_SECRET / auth_token must be
moved to environment variables before production deployment.

Relations:
  UTILIZES:       TOOL.Forge.SourceMap
  SYNERGIZES_WITH: GVRN.CI.ForgePR
  BROADCASTS_TO:  NEXUS.Worker.Handshake (WebSocket clients)
  GOVERNED_BY:    CODEX-LAW-03

[OMNI-ARTIFACT-ANCHOR] ID: TOOL.Forge.Daemon VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-23
"""

import asyncio
import difflib
import json
import os
import ssl
import subprocess
import threading
import time

import websockets
from axion_core.src.cse.sourcemap import ForgeSourceMap  # type: ignore
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# PORTABILITY FIX: Resolve forge script via env var (CODEX-LAW-03)
FORGE_ROOT = os.environ.get("FORGE_ROOT", os.path.dirname(os.path.abspath(__file__)))
FORGE_SCRIPT = os.path.join(FORGE_ROOT, "tools", "forge_all.py")

# Global set of connected WebSocket IDE clients
CONNECTED_CLIENTS: set = set()


def create_ws_handler(expected_token: str, sourcemap: ForgeSourceMap):
    """Factory to create an authenticated WebSocket handler."""

    async def ws_handler(websocket):
        try:
            auth_message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            auth_data = json.loads(auth_message)
            if auth_data.get("token") != expected_token:
                print("[WS] Rejecting unauthorized connection attempt.")
                await websocket.close(code=1008, reason="Unauthorized")
                return
        except Exception as e:
            print(f"[WS] Authentication handshake failed: {e}")
            await websocket.close(code=1008, reason="Unauthorized")
            return

        CONNECTED_CLIENTS.add(websocket)
        print(f"[WS] IDE Client authenticated. Total clients: {len(CONNECTED_CLIENTS)}")
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get("action")
                if action in ["trace_hover", "trace_definition"]:
                    offset = data.get("offset")
                    req_id = data.get("id")
                    trace_result = sourcemap.trace_offset(offset)
                    if trace_result:
                        source_id, source_offset = trace_result
                        await websocket.send(
                            json.dumps(
                                {
                                    "status": f"{action}_result",
                                    "id": req_id,
                                    "source_id": source_id,
                                    "source_offset": source_offset,
                                }
                            )
                        )
        finally:
            CONNECTED_CLIENTS.remove(websocket)
            print("[WS] IDE Client disconnected.")

    return ws_handler


async def broadcast_message(message: str):
    """Broadcasts a real-time message to all connected IDEs."""
    if CONNECTED_CLIENTS:
        websockets.broadcast(CONNECTED_CLIENTS, message)


class DeltaHandler(FileSystemEventHandler):
    def __init__(
        self, filepath: str, sourcemap: ForgeSourceMap, loop: asyncio.AbstractEventLoop
    ):
        self.filepath = os.path.abspath(filepath)
        self.sourcemap = sourcemap
        self.last_content = self._read_file()
        self.loop = loop
        self._compile_timer = None
        self._compile_lock = threading.Lock()

    def _read_file(self) -> str:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] Failed to read {self.filepath}: {e}")
            return ""

    def on_modified(self, event):
        src_path = os.path.abspath(event.src_path)
        if src_path == self.filepath:
            new_content = self._read_file()
            if new_content != self.last_content:
                self._calculate_and_apply_delta(new_content)
                self.last_content = new_content
                self._trigger_recompile()
        elif src_path.endswith(".md"):
            print(f"[*] Detected layout change in {src_path}")
            self._trigger_recompile()

    def _trigger_recompile(self):
        with self._compile_lock:
            if self._compile_timer is not None:
                self._compile_timer.cancel()
            self._compile_timer = threading.Timer(1.5, self._run_build)
            self._compile_timer.start()

    def _run_build(self):
        try:
            print("[*] Automatically re-compiling and signing artifacts...")
            # PORTABILITY FIX: Uses FORGE_SCRIPT resolved from FORGE_ROOT env var
            result = subprocess.run(
                ["python", FORGE_SCRIPT], capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                print("[PASS] Artifacts re-compiled and signed successfully.")
                payload = json.dumps(
                    {
                        "status": "compile_success",
                        "artifact": "artifacts/Master_Shell.md",
                    }
                )
                asyncio.run_coroutine_threadsafe(broadcast_message(payload), self.loop)
            else:
                print(f"[FAIL] Auto-compilation failed:\n{result.stderr}")
                payload = json.dumps(
                    {
                        "status": "error",
                        "message": "Compilation Failed",
                        "traceback": result.stderr,
                    }
                )
                asyncio.run_coroutine_threadsafe(broadcast_message(payload), self.loop)
        except subprocess.TimeoutExpired:
            print("[FAIL] Compilation timed out.")
            payload = json.dumps(
                {"status": "error", "message": "Compilation Timed Out"}
            )
            asyncio.run_coroutine_threadsafe(broadcast_message(payload), self.loop)
        except Exception as e:
            print(f"[ERROR] Failed to execute build orchestrator: {e}")

    def _calculate_and_apply_delta(self, new_content: str):
        """Computes exact character insertion/deletion offsets and updates the SourceMap."""
        matcher = difflib.SequenceMatcher(None, self.last_content, new_content)
        opcodes = matcher.get_opcodes()
        edit_offset = 0
        try:
            for tag, i1, i2, j1, j2 in reversed(opcodes):
                if tag == "equal":
                    continue
                old_len = i2 - i1
                new_len = j2 - j1
                length_diff = new_len - old_len
                edit_offset = i1
                print(
                    f"[*] Detected '{tag}' at index {edit_offset} | delta: {length_diff}"
                )
                self.sourcemap.apply_delta_update(edit_offset, length_diff)
                payload = json.dumps(
                    {
                        "status": "update",
                        "tag": tag,
                        "offset": edit_offset,
                        "delta": length_diff,
                    }
                )
                asyncio.run_coroutine_threadsafe(broadcast_message(payload), self.loop)
            print("[PASS] SourceMap resynchronized via delta update.")
        except Exception as e:
            error_payload = json.dumps(
                {"status": "error", "message": str(e), "offset": edit_offset}
            )
            asyncio.run_coroutine_threadsafe(
                broadcast_message(error_payload), self.loop
            )
            print(f"[FAIL] Error updating sourcemap: {e}")


def run_ws_server(
    loop,
    sourcemap,
    host="0.0.0.0",
    port=8765,
    cert_path=None,
    key_path=None,
    auth_token="SECURE_TOKEN",
):
    """Runs the WebSocket server, optionally secured with TLS (WSS)."""
    asyncio.set_event_loop(loop)
    ssl_context = None
    if cert_path and key_path:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    handler = create_ws_handler(auth_token, sourcemap)
    start_server = websockets.serve(handler, host, port, ssl=ssl_context)
    loop.run_until_complete(start_server)
    protocol = "wss" if ssl_context else "ws"
    print(f"[ACTIVE] WebSocket Server listening on {protocol}://{host}:{port}")
    loop.run_forever()


def start_daemon(
    watch_file: str,
    sourcemap: ForgeSourceMap,
    watch_dir: str = None,
    host: str = "0.0.0.0",
    port: int = 8765,
    cert_path: str = None,
    key_path: str = None,
    auth_token: str = "SECURE_TOKEN",
):
    """Starts the Forge Daemon with optional remote binding and SSL."""
    ws_loop = asyncio.new_event_loop()
    ws_thread = threading.Thread(
        target=run_ws_server,
        args=(ws_loop, sourcemap, host, port, cert_path, key_path, auth_token),
        daemon=True,
    )
    ws_thread.start()

    event_handler = DeltaHandler(watch_file, sourcemap, ws_loop)
    observer = Observer()

    if watch_dir is None:
        watch_dir = os.path.dirname(os.path.abspath(watch_file))

    observer.schedule(event_handler, path=watch_dir, recursive=True)
    observer.start()
    print(f"[ACTIVE] Daemon listening for text edits on: {watch_dir} ...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Halting daemon...")
        observer.stop()
    observer.join()
