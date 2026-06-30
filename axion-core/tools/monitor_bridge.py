# tools/monitor_bridge.py
import os
import sys
import time
import json
import socket
from datetime import datetime

TARGET_DIRS = ["./src", "./data", "./tools"]
HOST, PORT = "127.0.0.1", 9999

def watch_channels():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[SIGNALS] Monitoring daemon online. Port locked: {PORT}")
    
    # Simple snapshot state tracking matrix
    snap = {}
    for d in TARGET_DIRS:
        if os.path.exists(d):
            for r, _, files in os.walk(d):
                for f in files:
                    p = os.path.join(r, f)
                    try: snap[p] = os.path.getmtime(p)
                    except OSError: pass

    while True:
        try:
            conn, _ = server.accept()
            print("[SIGNALS] Visual monitoring cockpit attached.")
            while True:
                time.sleep(0.5)  # Poll spacing block
                curr_time = time.time()
                
                for d in TARGET_DIRS:
                    if not os.path.exists(d): continue
                    for r, _, files in os.walk(d):
                        for f in files:
                            p = os.path.join(r, f)
                            try:
                                mtime = os.path.getmtime(p)
                                if p not in snap:
                                    event = {"event": "CREATED", "path": p, "timestamp": datetime.isoformat(datetime.now())}
                                    conn.sendall((json.dumps(event) + "\n").encode())
                                    snap[p] = mtime
                                elif mtime > snap[p]:
                                    event = {"event": "MUTATED", "path": p, "timestamp": datetime.isoformat(datetime.now())}
                                    conn.sendall((json.dumps(event) + "\n").encode())
                                    snap[p] = mtime
                            except (OSError, BrokenPipeError):
                                break
        except Exception as e:
            print(f"[EXCEPTION] Socket dropped: {e}")
            time.sleep(2)

if __name__ == "__main__":
    watch_channels()