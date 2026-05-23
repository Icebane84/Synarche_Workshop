#!/usr/bin/env python3
"""# TOOL-STAR-005: Weaver Engine (Coherence Core).

## I. Universal Identification & Provenance
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `TOOL-STAR-005` |
| **Official Name** | `weaver_engine.py` |
| **Version** | **v1.1** |
| **Celestial Class** | `[STAR]` |
| **Governance** | `GVRN-SYNERGY-001` |
"""

import json
import logging
import os
import re
from typing import Any

logger = logging.getLogger(__name__)


class ASLWeaverEngine:
    """Passively analyzes or actively forges celestial links."""

    def __init__(self, config_path: str, root_dir: str) -> None:
        self.root_dir = os.path.abspath(root_dir)
        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

        self.artifact_map: dict[str, str] = {}  # ID -> AbsPath
        self.classes: dict[str, str] = {}  # ID -> Class
        self.prs_id = self.config["relations"]["prs_id"]

    def scan(self) -> None:
        """Indexes artifacts across configured directories."""
        id_pattern = re.compile(self.config["patterns"]["artifact_id"], re.I)
        class_pattern = re.compile(self.config["patterns"]["celestial_class"], re.I)

        for subdir in self.config["search_dirs"]:
            target = os.path.join(self.root_dir, subdir)
            if not os.path.exists(target):
                continue

            for root, _, files in os.walk(target):
                for file in files:
                    if file.endswith(".md"):
                        self._ingest_file(
                            os.path.join(root, file), id_pattern, class_pattern
                        )

    def _ingest_file(
        self, path: str, id_pattern: re.Pattern, class_pattern: re.Pattern
    ) -> None:
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            id_match = id_pattern.search(content)
            if id_match:
                art_id = id_match.group(1).strip()
                self.artifact_map[art_id] = path

                class_match = class_pattern.search(content)
                if class_match:
                    self.classes[art_id] = class_match.group(1).strip()
        except Exception:
            logger.exception(f"Engine failed to ingest {path}")

    def plan_weave(self) -> dict[str, list[str]]:
        """Generates a list of suggested link injections without modifying source."""
        forge_plan: dict[str, list[str]] = {}

        for art_id, _path in self.artifact_map.items():
            if self.prs_id in art_id or "OSLM" in art_id:
                continue

            suggested_links = self._analyze_artifact_coherence(art_id)
            if suggested_links:
                forge_plan[art_id] = suggested_links

        return forge_plan

    def _analyze_artifact_coherence(self, art_id: str) -> list[str]:
        path = self.artifact_map[art_id]
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        suggestions = []
        celestial_class = self.classes.get(art_id, "UNKNOWN")

        # Check PRS Link
        if self.prs_id not in content:
            suggestions.append(f"MISSING_LINK: {self.prs_id}")

        # Check Moon -> Parent Planet Planet
        if celestial_class == "MOON":
            parent_id = self._find_parent_planet(art_id, content)
            if parent_id and parent_id not in content:
                suggestions.append(f"MISSING_PARENT: {parent_id}")

        return suggestions

    def _find_parent_planet(self, art_id: str, content: str) -> str | None:
        gov_match = re.search(self.config["patterns"]["governance"], content)
        if gov_match:
            gov_id = gov_match.group(1).strip()
            if self.classes.get(gov_id) == "PLANET":
                return gov_id

        for p_id, p_class in self.classes.items():
            if p_class == "PLANET" and p_id in art_id and p_id != art_id:
                return p_id
        return None

    def execute_forge(self, forge_plan: dict[str, list[str]]) -> int:
        """Applies the forge plan to the filesystem."""
        updated = 0
        for art_id, suggestions in forge_plan.items():
            path = self.artifact_map[art_id]
            if self._apply_suggestions(path, suggestions):
                updated += 1
        return updated

    def _apply_suggestions(self, path: str, suggestions: list[str]) -> bool:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()

        modified = False
        new_lines = []
        for line in lines:
            if "Relations" in line:
                for suggestion in suggestions:
                    target_id = suggestion.split(": ")[-1]
                    injected_line = self._inject_link_logic(line, target_id)
                    if injected_line != line:
                        line = injected_line
                        modified = True
            new_lines.append(line)

        if modified:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        return modified

    def _inject_link_logic(self, line: str, target_id: str) -> str:
        # Avoid duplicate injection
        existing_ids = set(re.findall(self.config["patterns"]["id_match"], line))
        if target_id in existing_ids:
            return line

        if "|" in line:
            parts = line.split("|")
            for i, p in enumerate(parts):
                if "Relations" in p:
                    val = parts[i + 1].strip()
                    if val in ["N/A", "", "Pending Integration"]:
                        parts[i + 1] = f" `LINK: {target_id}` "
                    else:
                        parts[i + 1] = f" `LINK: {target_id}`, {val} "
                    return "|".join(parts)
        return line.strip() + f" `LINK: {target_id}`\n"

    def audit_lis(self) -> dict[str, Any]:
        """Calculates LIS and returns detailed audit metrics."""
        total_links = 0
        valid_links = 0
        id_pattern = re.compile(self.config["patterns"]["id_match"])

        for art_id, path in self.artifact_map.items():
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            links = id_pattern.findall(content)
            for link in links:
                if link == art_id:
                    continue
                total_links += 1
                if link in self.artifact_map or any(
                    link in existing for existing in self.artifact_map
                ):
                    valid_links += 1

        score = (valid_links / total_links * 100) if total_links > 0 else 100.0
        return {
            "lis_score": f"{score:.2f}%",
            "metrics": {
                "total_artifacts": len(self.artifact_map),
                "total_links": total_links,
                "valid_links": valid_links,
            },
        }
