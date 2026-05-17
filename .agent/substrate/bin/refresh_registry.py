import os
from datetime import datetime

import yaml

"""
[OMNI-ANCHOR] ID: SYNG.TOOL.RefreshRegistry VER: v15.0 [OMEGA] STATUS: ACTIVE
Domain: SYNERGY
Purpose: Auto-scan and index skills and workflows into registries.
"""

# Absolute Path Calibration: Resolve .agent directory relative to this script
# refresh_registry.py is in .agent/substrate/bin/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Traversal: bin -> substrate -> .agent
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
# Sync Root: parent of .agent
SYNC_ROOT = os.path.dirname(BASE_DIR)

# Sovereign Constants
OMNI_IGNORE = "README.md"


def normalize_path(abs_path):
    """Converts an absolute path to a root-relative modular path."""
    rel = os.path.relpath(abs_path, SYNC_ROOT).replace("\\", "/")
    return f"/{rel}" if not rel.startswith("/") else rel


def scan_skills() -> None:
    skills_root = os.path.join(BASE_DIR, "skills")
    print(f"[*] Scanning skills in {skills_root}...")

    # Iterate through domain subdirectories (core, lang, etc.)
    for domain in os.listdir(skills_root):
        domain_path = os.path.join(skills_root, domain)
        if not os.path.isdir(domain_path) or domain == OMNI_IGNORE:
            continue

        registry = {
            "domain": domain.upper(),
            "last_updated": datetime.now().isoformat(),
            "skills": [],
        }

        for skill_dir in os.listdir(domain_path):
            skill_path = os.path.join(domain_path, skill_dir)
            if os.path.isdir(skill_path):
                skill_file = os.path.join(skill_path, "SKILL.md")
                has_doc = os.path.exists(skill_file)
                registry["skills"].append(
                    {
                        "id": skill_dir,
                        "path": normalize_path(skill_path),
                        "documented": has_doc,
                    }
                )

        registry_file = os.path.join(domain_path, "registry.yaml")
        with open(registry_file, "w", encoding="utf-8") as f:
            yaml.dump(registry, f, default_flow_style=False)
        print(f"[+] Updated registry: {registry_file}")


def scan_workflows() -> None:
    workflows_root = os.path.join(BASE_DIR, "workflows")
    print(f"[*] Scanning workflows in {workflows_root}...")

    for category in os.listdir(workflows_root):
        category_path = os.path.join(workflows_root, category)
        if not os.path.isdir(category_path) or category == OMNI_IGNORE:
            continue

        registry = {
            "category": category.upper(),
            "last_updated": datetime.now().isoformat(),
            "workflows": [],
        }

        for wf_file in os.listdir(category_path):
            if wf_file.endswith(".md") and wf_file != OMNI_IGNORE:
                registry["workflows"].append(
                    {
                        "id": wf_file.replace(".md", ""),
                        "path": normalize_path(os.path.join(category_path, wf_file)),
                    }
                )

        registry_file = os.path.join(category_path, "registry.yaml")
        with open(registry_file, "w", encoding="utf-8") as f:
            yaml.dump(registry, f, default_flow_style=False)
        print(f"[+] Updated registry: {registry_file}")


if __name__ == "__main__":
    scan_skills()
    scan_workflows()
