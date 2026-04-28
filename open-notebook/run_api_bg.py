
import subprocess
import time
import os

print("Starting run_api_bg.py wrapper...")

env = os.environ.copy()
env['PYTHONUNBUFFERED'] = '1'

with open("api_server.log", "w") as log_file:
    print("Launching subprocess...", file=log_file)
    process = subprocess.Popen(
        [r"c:\Users\Chris\Synarche_Workspace\.venv\Scripts\python.exe", "run_api.py"],
        stdout=log_file,
        stderr=log_file,
        cwd=r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook",
        env=env,
        creationflags=subprocess.CREATE_NEW_CONSOLE  # Use this on Windows to detach
    )
    print(f"Subprocess launched with PID {process.pid}")
    
    # Monitor for 5 seconds
    for i in range(5):
        if process.poll() is not None:
            print(f"Process ended prematurely with code {process.returncode}")
            break
        time.sleep(1)
        print(f"Server is running... {i+1}")

print("Wrapper execution complete.")
