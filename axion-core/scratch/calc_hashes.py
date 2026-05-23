import hashlib
from pathlib import Path


def get_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


root = Path(r"c:\Users\Chris\Synarche_Workspace\axion-core")
files = [
    root / "activate_axion.py",
    root / "forge" / "rnc_engine.py",
    root / "forge" / "cse_engine.py",
]

for f in files:
    if f.exists():
        print(f"{f.name}: {get_hash(f)}")
    else:
        print(f"{f.name}: NOT FOUND")
