import os
from datetime import datetime
from typing import Any

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


def normalize_path(abs_path: str) -> str:
    """Converts an absolute path to a root-relative modular path."""
    rel = os.path.relpath(abs_path, SYNC_ROOT).replace("\\", "/")
    return f"/{rel}" if not rel.startswith("/") else rel


def scan_skills() -> None:
    skills_root = os.path.join(BASE_DIR, "skills")
    print(f"[*] Scanning skills in {skills_root}...")

    # Iterate through subdirectories
    for item in os.listdir(skills_root):
        item_path = os.path.join(skills_root, item)
        if not os.path.isdir(item_path) or item == OMNI_IGNORE:
            continue

        # Check if this item is a top-level skill itself
        skill_file = os.path.join(item_path, "SKILL.md")
        if not os.path.exists(skill_file):
            skill_file = os.path.join(item_path, "skill.md")

        if os.path.exists(skill_file):
            # It's an individual top-level skill
            registry = {
                "skill": item,
                "last_updated": datetime.now().isoformat(),
                "path": normalize_path(item_path),
                "documented": True,
            }
            registry_file = os.path.join(item_path, "registry.yaml")
            with open(registry_file, "w", encoding="utf-8") as f:
                yaml.dump(registry, f, default_flow_style=False)
            print(f"[+] Updated top-level skill registry: {registry_file}")
        else:
            # It's a domain directory containing nested skills
            skills_list: list[dict[str, Any]] = []

            for skill_dir in os.listdir(item_path):
                skill_path = os.path.join(item_path, skill_dir)
                if os.path.isdir(skill_path):
                    skill_f = os.path.join(skill_path, "SKILL.md")
                    if not os.path.exists(skill_f):
                        skill_f = os.path.join(skill_path, "skill.md")
                    has_doc = os.path.exists(skill_f)
                    skills_list.append(
                        {
                            "id": skill_dir,
                            "path": normalize_path(skill_path),
                            "documented": has_doc,
                        }
                    )

            registry = {
                "domain": item.upper(),
                "last_updated": datetime.now().isoformat(),
                "skills": skills_list,
            }

            registry_file = os.path.join(item_path, "registry.yaml")
            with open(registry_file, "w", encoding="utf-8") as f:
                yaml.dump(registry, f, default_flow_style=False)
            print(f"[+] Updated domain registry: {registry_file}")


def scan_workflows() -> None:
    workflows_root = os.path.join(BASE_DIR, "workflows")
    print(f"[*] Scanning workflows in {workflows_root}...")

    for category in os.listdir(workflows_root):
        category_path = os.path.join(workflows_root, category)
        if not os.path.isdir(category_path) or category == OMNI_IGNORE:
            continue

        workflows_list: list[dict[str, Any]] = []

        for wf_file in os.listdir(category_path):
            if wf_file.endswith(".md") and wf_file != OMNI_IGNORE:
                workflows_list.append(
                    {
                        "id": wf_file.replace(".md", ""),
                        "path": normalize_path(os.path.join(category_path, wf_file)),
                    }
                )

        registry = {
            "category": category.upper(),
            "last_updated": datetime.now().isoformat(),
            "workflows": workflows_list,
        }

        registry_file = os.path.join(category_path, "registry.yaml")
        with open(registry_file, "w", encoding="utf-8") as f:
            yaml.dump(registry, f, default_flow_style=False)
        print(f"[+] Updated registry: {registry_file}")


if __name__ == "__main__":
    scan_skills()
    scan_workflows()
