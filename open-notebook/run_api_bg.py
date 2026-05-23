import os
import subprocess
import time

env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"

with open("api_server.log", "w") as log_file:
    print("Launching subprocess...", file=log_file)
    process = subprocess.Popen(
        [r"c:\Users\Chris\Synarche_Workspace\.venv\Scripts\python.exe", "run_api.py"],
        stdout=log_file,
        stderr=log_file,
        cwd=r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook",
        env=env,
        creationflags=subprocess.CREATE_NEW_CONSOLE,  # Use this on Windows to detach
    )

    # Monitor for 5 seconds
    for _i in range(5):
        if process.poll() is not None:
            break
        time.sleep(1)
