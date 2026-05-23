"""# TOOL-EMPR-003: The Scaffolding Engine (Emperor's Decree).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-EMPR-003`                                          |
| **2. Official Name**   | `scaffold_engine.py`                                     |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `ARCH`                                                   |
| **6. Evolution**       | **Purposeful Drive**                                     |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Structure**                                            |
| **11. Catalyst**       | **Project Initialization**                               |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Emperor persona uses this tool for project scaffolding.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Schema Forge (The Emperor)
# Synergy Set: The Imperial Standard
# Primary Stat Buff: Authority (+15), Order (+10)
# Passive Ability: The Architect's Grid (Standardization)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: SCAFFOLD` | Create Project Structure | Rapid Alignment |
| `⚡ EXECUTE: INIT_GIT` | Init Git & Ignore | Security & Tracking |
"""

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("ScaffoldEngine")

# --- Constants ---
DEFAULT_TEMPLATE_PATH = Path("templates/default_structure.json")


class ScaffoldEngine:
    def __init__(
        self,
        template_path: Path,
        target_dir: Path,
        project_name: str,
        dry_run: bool = False,
    ) -> None:
        self.template_path = template_path
        self.target_dir = target_dir
        self.project_name = project_name
        self.dry_run = dry_run
        self.structure: dict[str, Any] = {}
        self.file_contents: dict[str, str] = {}

    def load_template(self) -> None:
        """Loads the JSON template."""
        if not self.template_path.exists():
            logger.error(f"❌ [ERROR] Template not found: {self.template_path}")
            sys.exit(1)

        try:
            with open(self.template_path, encoding="utf-8") as f:
                data = json.load(f)
                self.structure = data.get("structure", {})
                self.file_contents = data.get("file_contents", {})
            logger.info(f"📘 [LOADED] Template sourced from {self.template_path}")
        except json.JSONDecodeError:
            logger.exception("❌ [ERROR] Invalid JSON in template")
            sys.exit(1)

    def ignite(self) -> None:
        """Starts the scaffolding process."""
        logger.info(
            f"\n⚡ [IGNITION] HEPHAESTUS ENGINE START (Dry Run: {self.dry_run})"
        )
        logger.info(f"   Target:      {self.target_dir}")
        logger.info(f"   Project:     {self.project_name}")
        logger.info("-" * 50)

        # Create root if it doesn't exist
        if not self.dry_run:
            self.target_dir.mkdir(parents=True, exist_ok=True)
        else:
            logger.info(f"🔍 [DRY-RUN] Root Directory: {self.target_dir}")

        self._build_tree(self.target_dir, self.structure)

        logger.info("-" * 50)
        logger.info("✨ [COMPLETE] Scaffolding Process Finalized.")

    def _replace_vars(self, text: str) -> str:
        """Global replacement of placeholders.
        Ensures all instances of {{PROJECT_NAME}} are replaced.
        """
        return text.replace("{{PROJECT_NAME}}", self.project_name)

    def _process_directory(self, current_path: Path, content: dict | list) -> None:
        """Handles directory creation and recursion."""
        if not self.dry_run:
            if not current_path.exists():
                current_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"📂 [CREATED] Dir:  {current_path}")
            else:
                logger.info(f"📂 [EXISTS]  Dir:  {current_path}")
        else:
            logger.info(f"🔍 [DRY-RUN] Dir:  {current_path}")

        self._build_tree(current_path, content)

    def _process_file_item(self, current_path: Path, item: str) -> None:
        """Handles individual file creation from list item."""
        safe_name = self._replace_vars(item)
        file_path = current_path / safe_name
        self._create_file(file_path, item)

    def _build_tree(self, current_path: Path, structure: Any) -> None:
        """Recursively builds the directory tree."""
        # Case 1: Structure is a Dict (Directory key -> Sub-content)
        if isinstance(structure, dict):
            for name, content in structure.items():
                safe_name = self._replace_vars(name)
                next_path = current_path / safe_name

                if isinstance(content, (dict, list)):
                    self._process_directory(next_path, content)
                else:
                    # Key-Value pair where value might be content directly (rare but possible)
                    pass

        # Case 2: Structure is a List (Files or Sub-structures)
        elif isinstance(structure, list):
            for item in structure:
                if isinstance(item, str):
                    self._process_file_item(current_path, item)
                elif isinstance(item, dict):
                    # Recursive dict inside list
                    self._build_tree(current_path, item)

    def _create_file(self, path: Path, key: str) -> None:
        """Creates a file, injecting content if defined."""
        if self.dry_run:
            logger.info(f"🔍 [DRY-RUN] File: {path}")
            return

        if path.exists():
            logger.info(f"📄 [EXISTS]  File: {path}")
            return

        content = ""
        # Check if we have a template for this file content
        if key in self.file_contents:
            raw_content = self.file_contents[key]
            content = self._replace_vars(raw_content)
            # Validation check
            if "{{" in content and "}}" in content:
                logger.warning(
                    f"⚠️  [WARNING] Unreplaced placeholders detected in {path.name}"
                )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"✅ [CREATED] File: {path}")

    def init_git(self) -> None:
        """Initializes a git repository."""
        if self.dry_run:
            logger.info("🔍 [DRY-RUN] Would initialize Git repository.")
            return

        gitignore_path = self.target_dir / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, "w") as f:
                f.write("*.pyc\n__pycache__/\n.env\n")
            logger.info("🛡️  [SECURED] .gitignore created")

        try:
            subprocess.run(
                ["git", "init", str(self.target_dir)],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            logger.info("🌳 [ROOTED] Git repository initialized.")
        except Exception:
            logger.exception("❌ [ERROR] Failed to init git")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synarche Scaffolding Engine")
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE_PATH,
        help="Path to JSON template",
    )
    parser.add_argument("--target", type=Path, required=True, help="Target directory")
    parser.add_argument(
        "--name",
        type=str,
        default="SynarcheDetails",
        help="Project Name for replacements",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    parser.add_argument("--git", action="store_true", help="Initialize Git repository")

    args = parser.parse_args()

    # Resolve paths
    base_path = Path.cwd()
    template_path = (
        args.template if args.template.is_absolute() else base_path / args.template
    )
    target_path = args.target if args.target.is_absolute() else base_path / args.target

    engine = ScaffoldEngine(template_path, target_path, args.name, args.dry_run)
    engine.load_template()
    engine.ignite()

    if args.git:
        engine.init_git()


if __name__ == "__main__":
    main()
