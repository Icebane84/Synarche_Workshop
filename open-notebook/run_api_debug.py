import os
import subprocess
import sys
import time

log_path = (
    r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook\api_debug.log"
)
python_exe = r"c:\Users\Chris\Synarche_Workspace\.venv\Scripts\python.exe"

env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"
env["API_RELOAD"] = "false"  # Disable reload to simplify


with open(log_path, "w") as log_file:
    print("Launching subprocess...", file=log_file)
    try:
        process = subprocess.Popen(
            [python_exe, "run_api.py"],
            stdout=log_file,
            stderr=log_file,
            cwd=r"c:\Users\Chris\Synarche_Workspace\open-notebook\open_notebook",
            env=env,
        )
    except Exception as e:
        sys.exit(1)

    # Monitor for 10 seconds
    for _i in range(10):
        ret = process.poll()
        if ret is not None:
            break
        time.sleep(1)
