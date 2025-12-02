import json
import os
from pathlib import Path

# --- CONFIGURATION ---
ROOT_DIR = "Synarche_Workspace"

STRUCTURE = {
    "_governance": ["synarche_core.json", "DOC-STD-001.md", "PROT-AI-001.md"],
    "nova-forge": {
        ".blueprints": [],
        "src": ["backend", "frontend"],
        "tests": [],
        "docs": [],
    },
    "where-light-fades": {
        "world-bible": [],
        "characters": [],
        "drafts": [],
        "archived": [],
    },
    "axion-core": {"src": [], "dist": []},
}


def create_structure(base_path: Path, structure: dict) -> None:
    """
    Recursively builds the directory tree.
    """
    for name, content in structure.items():
        path = base_path / name
        _ensure_directory(path)

        if isinstance(content, list):
            _handle_file_list(path, content)
        elif isinstance(content, dict):
            create_structure(path, content)


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    print(f"[CREATED] Directory: {path}")


def _handle_file_list(path: Path, files: list) -> None:
    for file_name in files:
        if "." in file_name:
            _create_and_seed_file(path, file_name)


def _create_and_seed_file(path: Path, file_name: str) -> None:
    file_path = path / file_name
    if not file_path.exists():
        file_path.touch()
        print(f"   + [SEEDED] File: {file_name}")

        if file_name == "synarche_core.json":
            write_catalyst(file_path)


def write_catalyst(path: Path) -> None:
    """
    Injects the 'Synarche Core' data into the JSON file.
    This ensures the file isn't just empty, but functional.
    """
    core_data = {
        "bundle_id": "SYNARCHE-MASTER-V1",
        "protocols": ["DOC-STD-001", "PHOENIX-VOICE"],
        "status": "ACTIVE",
    }
    with open(path, "w") as f:
        json.dump(core_data, f, indent=2)
    print("   + [INJECTED] Master Catalyst payload written.")


# --- EXECUTION ---

if __name__ == "__main__":
    root_path = Path(os.getcwd()) / ROOT_DIR
    print(f"Initializing Synarche Repository Standard at: {root_path}\n")
    create_structure(root_path, STRUCTURE)
    print("\n[COMPLETE] Environment Terraform Successful.")
