import hashlib
import os
from pathlib import Path

def get_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_entry(file_path, artifact_id, domain, official_name, version="v15.0 [OMEGA]"):
    rel_path = os.path.relpath(file_path, "c:\\Users\\Chris\\Synarche_Workspace")
    # Normalize path separators for the registry
    rel_path = rel_path.replace("\\", "/")
    
    content_hash = get_hash(file_path)
    
    return f"""{artifact_id}:
  artifact_id: {artifact_id}
  content_hash: {content_hash}
  domain: {domain}
  official_name: {official_name}
  path: {rel_path}
  status: "[ACTIVE]"
  version: {version}
"""

ecs_files = {
    "__init__.py": ("ENG-ECS-INI-001", "ENG-ECS"),
    "world.py": ("CORE-FDE-ECS-WRLD-001", "ENG-ECS"),
    "synergy.py": ("ENG-ECS-SYN-001", "ENG-ECS"),
    "resonance.py": ("ENG-ECS-RES-001", "ENG-ECS"),
    "manager.py": ("ENG-ECS-MAN-001", "ENG-ECS"),
    "fde_test_harness.py": ("CORE-FDE-TEST-001", "ENG-ECS"),
    "entity_registry.py": ("CORE-FDE-ECS-REG-001", "ENG-ECS"),
    "ecs_scheduler.py": ("CORE-FDE-ECS-SCH-001", "ENG-ECS"),
    "ecs_hardened_core.py": ("CORE-FDE-ECS-006", "ENG-ECS"),
    "ecs_core.py": ("CORE-FDE-ECS-005", "ENG-ECS"),
    "component.py": ("ENG-ECS-STO-001", "ENG-ECS"),
}

log_files = {
    "__init__.py": ("PHX-LOG-INI-001", "PHX-LOG"),
    "logger_philosophical_framework.py": ("PHX-LOG-CORE-001", "PHX-LOG"),
    "phx_logging_protocol_setup.py": ("PHX-LOG-SET-001", "PHX-LOG"),
}

ref_files = {
    "__init__.py": ("SYS-REF-INI-001", "SYS-REF"),
    "refactor_protocol_axion.py": ("SYS-REF-CORE-001", "SYS-REF"),
    "rollback_core.py": ("SYS-REF-ROLL-001", "SYS-REF"),
    "parallel_executor_v2.py": ("SYS-REF-PAR-001", "SYS-REF"),
}

base_dir = "c:\\Users\\Chris\\Synarche_Workspace\\axion-core\\src"
target_groups = [
    (os.path.join(base_dir, "engine", "ecs"), ecs_files),
    (os.path.join(base_dir, "phoenix", "logging"), log_files),
    (os.path.join(base_dir, "system", "refactor"), ref_files),
]

with open("c:\\Users\\Chris\\Synarche_Workspace\\axion-core\\registry_updates.yaml", "w") as f:
    for dir_path, files in target_groups:
        d_path = Path(dir_path)
        for filename, (aid, domain) in files.items():
            file_path = d_path / filename
            if file_path.exists():
                f.write(generate_entry(str(file_path), aid, domain, filename))
                f.write("\n")

print("Generated registry_updates.yaml")
