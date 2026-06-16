"""
artifact_anchor:
  id: GVRN.CRAWLER.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: GVRN
  celestial_class: STAR
  tier: GOVERNANCE
  state: ACTIVE
  ethos: SOVEREIGN_GOVERNANCE_COMPONENT
  relations: []
"""

# Phase 1: Discovery Engine
# Handles file crawling, path boundaries, and incremental exclusions

import os
import re
import datetime
from .config import DOMAIN_PREFIXES


class WorkspaceCrawler:
    def __init__(self, target_dir: str, tier_scope: str = None):
        self.target_dir = os.path.abspath(target_dir)
        self.tier_scope = tier_scope
        self.ignored_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            "venv",
            "env",
            ".agent",
            "_archive",
            ".archives",
            "_logs",
            "logs",
            ".mypy_cache",
            ".ruff_cache",
            "recovery",
            "incoming",
            ".trunk",
            ".vscode",
            "scratch",
            "artifacts",
            ".pytest_cache",
            "uam",
        }

    def is_in_scope(self, file_path: str) -> bool:
        """Applies path-boundaries and checks if file falls within active execution tier."""
        filename = os.path.basename(file_path)
        if not file_path.endswith((".py", ".js", ".ts", ".html", ".md")):
            return False
        if filename in ("validate_uam.py", "enforce_uam.py"):
            return False

        rel_path = os.path.relpath(file_path, self.target_dir).replace("\\", "/")

        if not self.tier_scope:
            # Default standard check skips narrative and story files under where_light_fades
            return "where_light_fades/" not in rel_path

        tier = self.tier_scope.lower()
        if tier == "tier1":
            # Tier 1 (Infrastructure & Tools): tools and governance directories
            return rel_path.startswith(("axion-core/tools/", "_governance/tools/"))
        elif tier == "tier2":
            # Tier 2 (Core Logic Code): source code excluding web charts/HTML
            return rel_path.startswith("axion-core/src/") and not rel_path.startswith(
                "axion-core/src/03_fabric/"
            )
        elif tier == "tier3":
            # Tier 3 (UI Presentation Templates): HTML/CSS/UI fabric files
            return rel_path.startswith("axion-core/src/03_fabric/")
        elif tier == "tier4":
            # Tier 4 (Extended Scope): Documentation/Game files (all else)
            return "where_light_fades/" in rel_path

        return False

    def infer_metadata(self, file_path: str) -> dict:
        """Infers a compliant UIP-V15 metadata dictionary for a file lacking an anchor."""
        filename = os.path.basename(file_path)
        base_name, ext = os.path.splitext(filename)
        rel_path = os.path.relpath(file_path, self.target_dir).replace("\\", "/")

        domain = "CORE"
        if rel_path.startswith("axion-core/src/03_fabric/"):
            domain = "FABRIC"
        elif rel_path.startswith(("axion-core/tools/", "infra/")):
            domain = "INFRA"
        elif rel_path.startswith("_governance/"):
            domain = "GVRN"
        elif "test" in rel_path.lower():
            domain = "TEST"
        elif "lore" in rel_path.lower():
            domain = "LORE"

        tier = "LOGIC"
        if ext in (".html", ".css"):
            tier = "PRESENTATION"
        elif rel_path.startswith(("axion-core/tools/", "infra/")):
            tier = "COMPUTE"
        elif ext == ".md" or rel_path.startswith("_governance/"):
            tier = "GOVERNANCE"

        prefix = DOMAIN_PREFIXES.get(domain, "CORE")
        clean_name = re.sub(r"[^A-Za-z0-9._-]", "_", base_name).upper()
        clean_name = re.sub(r"__+", "_", clean_name).strip("_.")
        if len(clean_name) > 30:
            clean_name = clean_name[:30].strip("_.")

        artifact_id = f"{prefix}.{clean_name}.001"
        ethos = f"SOVEREIGN_{tier}_COMPONENT"

        return {
            "id": artifact_id,
            "version": "v15.0 [OMEGA]",
            "provenance": datetime.date.today().isoformat(),
            "domain": domain,
            "celestial_class": "STAR",
            "tier": tier,
            "state": "ACTIVE",
            "ethos": ethos,
            "relations": [],
        }

    def discover_files(self) -> list[str]:
        """Walks the workspace directory tree and returns list of eligible absolute file paths."""
        matched_files = []
        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            for file in files:
                full_path = os.path.join(root, file)
                if self.is_in_scope(full_path):
                    matched_files.append(full_path)
        return sorted(matched_files)
