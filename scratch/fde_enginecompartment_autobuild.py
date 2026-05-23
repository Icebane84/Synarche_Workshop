from pathlib import Path

# --- DIRECTORY MAP ---
FDE_STRUCTURE = {
    "gvrn": ["law_validator.py", "selt_logger.py"],
    "core": [
        "engine_runtime.py",
        "chunk_executor.py",
        "rollback_core.py",
        "delta_packet.py",
    ],
    "ecs": [
        "entity_registry.py",
        "archetype_storage.py",
        "world.py",
        "commit_layer.py",
        "ecs_scheduler.py",
    ],
    "dag": ["dag_compiler.py", "system_signature.py"],
    "systems": ["base_system.py", "movement_system.py", "input_system.py"],
    "bridge": ["godot_translation_layer.py"],
    "demo": ["fde_test_harness.py"],
    "docs": ["PRS_INDEX.md", "README.md"],
}

ROOT_DIR = "fde_engine"


def generate_header(filename: str, module_path: str) -> str:
    """Generates the standardized Phoenix Artifact Identification Block."""
    domain = module_path.split("/")[1].upper() if "/" in module_path else "ROOT"

    return f'''"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID** | `CORE-FDE-{domain}-{filename.split(".")[0].upper()}` | The Sovereign ID. |
| **Official Name** | `{filename}`                  | The Filename.     |
| **Version** | **v1.0 [BASELINE]** | The Standard.     |
| **Domain** | `{domain}`                    | The Subject.      |
| **Status** | `[ACTIVE]`                    | The Lifecycle.    |

**Ethos:** Absolute Determinism. Zero Logic Drift.
"""

'''


def forge_repository():
    print(f"[INIT] Forging Sovereign Node: {ROOT_DIR}...")
    root_path = Path(ROOT_DIR)
    root_path.mkdir(exist_ok=True)

    for directory, files in FDE_STRUCTURE.items():
        dir_path = root_path / directory
        dir_path.mkdir(exist_ok=True)
        print(f"  [+] Created Directory: {dir_path}")

        for file in files:
            file_path = dir_path / file

            # Special handling for markdown files
            if file.endswith(".md"):
                content = f"# {file.replace('.md', '').replace('_', ' ').title()}\n\nInitialized via PHOENIX-FDE-FORGE."
            else:
                relative_mod_path = f"{ROOT_DIR}/{directory}/{file}"
                content = generate_header(file, relative_mod_path)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"      -> Forged Artifact: {file}")

    # Generate top-level README
    readme_path = root_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(
            "# The Phoenix Full Deterministic Engine (FDE)\n\n"
            "An Archetype-driven, DAG-compiled, Rollback-enabled simulation core.\n"
            "Governed by the Synarche. Built for absolute temporal control.\n"
        )
    print("      -> Forged Artifact: README.md")

    print(f"\n[SUCCESS] FDE Repository successfully materialized at ./{ROOT_DIR}/")


if __name__ == "__main__":
    forge_repository()
