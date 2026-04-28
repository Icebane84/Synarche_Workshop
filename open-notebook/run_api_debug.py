
import subprocess
import time
import os
import sys

print("Starting debug wrapper...")
log_path = r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook\api_debug.log"
python_exe = r"c:\Users\Chris\Synarche_Workspace\.venv\Scripts\python.exe"

env = os.environ.copy()
env['PYTHONUNBUFFERED'] = '1'
env['API_RELOAD'] = 'false'  # Disable reload to simplify

print(f"Logging to {log_path}")

with open(log_path, "w") as log_file:
    print("Launching subprocess...", file=log_file)
    try:
        process = subprocess.Popen(
            [python_exe, "run_api.py"],
            stdout=log_file,
            stderr=log_file,
            cwd=r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook",
            env=env
        )
        print(f"Subprocess launched with PID {process.pid}")
    except Exception as e:
        print(f"Failed to launch: {e}")
        sys.exit(1)
    
    # Monitor for 10 seconds
    for i in range(10):
        ret = process.poll()
        if ret is not None:
            print(f"Process ended prematurely with code {ret}")
            break
        time.sleep(1)
        print(f"Server is running... {i+1}")

print("Wrapper execution complete.")
