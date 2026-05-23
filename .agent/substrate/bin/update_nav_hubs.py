import os
from datetime import datetime

"""
[OMNI-ANCHOR] ID: SYNG.TOOL.UpdateNavHubs VER: v15.0 [OMEGA] STATUS: ACTIVE
Domain: SYNERGY
Purpose: Auto-generate README Navigation Hubs for skills and workflows.
"""

BASE_DIR = os.path.join(".agent")


def update_readme(path, title, items, item_type) -> None:
    readme_content = f"""# {title}

Auto-generated Navigation Hub for {item_type}.
Last Sync: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📂 Available {item_type}

"""
    for item in sorted(items):
        readme_content += f"- **{item}**\n"

    readme_content += (
        "\n---\n`[OMNI-ANCHOR] ID: SYNG.NAV.Hub VER: v15.0 [OMEGA] STATUS: ACTIVE`"
    )

    with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"[+] Updated README: {os.path.join(path, 'README.md')}")


def sync_hubs() -> None:
    # Sync Skill Hubs
    skills_root = os.path.join(BASE_DIR, "skills")
    for domain in os.listdir(skills_root):
        domain_path = os.path.join(skills_root, domain)
        if os.path.isdir(domain_path):
            skills = [
                d
                for d in os.listdir(domain_path)
                if os.path.isdir(os.path.join(domain_path, d))
            ]
            update_readme(
                domain_path, f"Skills: {domain.capitalize()}", skills, "Skills"
            )

    # Sync Workflow Hubs
    workflows_root = os.path.join(BASE_DIR, "workflows")
    for category in os.listdir(workflows_root):
        category_path = os.path.join(workflows_root, category)
        if os.path.isdir(category_path):
            workflows = [
                f.replace(".md", "")
                for f in os.listdir(category_path)
                if f.endswith(".md") and f != "README.md"
            ]
            update_readme(
                category_path,
                f"Workflows: {category.capitalize()}",
                workflows,
                "Workflows",
            )


if __name__ == "__main__":
    sync_hubs()
