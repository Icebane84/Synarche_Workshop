# tools/visual_hud_daemon.py
import os
import sys
import time
import json
import socket
from datetime import datetime

WATCHED_DOMAIMS = {
    "🧠 MIND": "./.agent",
    "📜 LAW": "./_governance",
    "⚙️ ENGINE": "./axion-core",
    "🧪 LAB": "./nova_forge",
    "📖 NARRATIVE": "./where_light_fades"
}
HOST, PORT = "127.0.0.1", 9999

def execute_workspace_gaze():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"[HUD-DAEMON] Real-time visual tracking online. Target Port: {PORT}")
    
    file_registry_snapshot = {}
    
    # Initialize topological file map baseline
    for domain_name, target_path in WATCHED_DOMAIMS.items():
        if os.path.exists(target_path):
            for root, _, files in os.walk(target_path):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    try:
                        file_registry_snapshot[full_path] = os.path.getmtime(full_path)
                    except OSError:
                        pass

    while True:
        try:
            connection, _ = server.accept()
            print("[HUD-DAEMON] Visual monitoring viewport hooked successfully.")
            while True:
                time.sleep(0.25) # High-resolution update spacing
                
                for domain_name, target_path in WATCHED_DOMAIMS.items():
                    if not os.path.exists(target_path):
                        continue
                        
                    for root, _, files in os.walk(target_path):
                        for file_name in files:
                            full_path = os.path.join(root, file_name)
                            try:
                                current_mtime = os.path.getmtime(full_path)
                                
                                if full_path not in file_registry_snapshot:
                                    # Node addition detected
                                    event = {
                                        "domain": domain_name,
                                        "event": "CREATED",
                                        "path": full_path,
                                        "timestamp": datetime.isoformat(datetime.now())
                                    }
                                    connection.sendall((json.dumps(event) + "\n").encode())
                                    file_registry_snapshot[full_path] = current_mtime
                                    
                                elif current_mtime > file_registry_snapshot[full_path]:
                                    # Node mutation detected
                                    event = {
                                        "domain": domain_name,
                                        "event": "MUTATED",
                                        "path": full_path,
                                        "timestamp": datetime.isoformat(datetime.now())
                                    }
                                    connection.sendall((json.dumps(event) + "\n").encode())
                                    file_registry_snapshot[full_path] = current_mtime
                                    
                            except (OSError, BrokenPipeError):
                                break
        except Exception as error_msg:
            print(f"[HUD-DAEMON] Connection dropped: {error_msg}. Resetting pipeline...")
            time.sleep(1)

if __name__ == "__main__":
    execute_workspace_gaze()