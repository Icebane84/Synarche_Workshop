# catalyst_weaver.py
# (Harvested & Enhanced for OMEGA v15.0)

import re
from typing import Any


class CatalystWeaver:
    """Logic layer for Automated Synergistic Linking (ASL)."""

    def __init__(self, synergy_threshold: float = 0.5) -> None:
        self.synergy_threshold = synergy_threshold

    def calculate_synergy_score(
        self, artifact_a: dict[str, Any], artifact_b: dict[str, Any]
    ) -> float:
        """Calculates a synergy score between two artifacts."""
        score = 0.0
        try:
            content_a = artifact_a.get("content", "") or ""
            content_b = artifact_b.get("content", "") or ""

            # Keyword Overlap
            keywords_a = set(self._extract_keywords(content_a))
            keywords_b = set(self._extract_keywords(content_b))
            overlap = keywords_a.intersection(keywords_b)
            if overlap:
                score += min(len(overlap) * 0.1, 0.4)

            # Metadata Alignment
            tags_a = set(artifact_a.get("tags", []))
            tags_b = set(artifact_b.get("tags", []))
            if tags_a.intersection(tags_b):
                score += 0.2

            # Explicit References
            id_b = artifact_b.get("id", "")
            if id_b and (f"[[{id_b}]]" in content_a or id_b in content_a):
                score += 0.4
        except Exception:
            return 0.0
        return min(score, 1.0)

    def weave(
        self, artifact_a: dict[str, Any], artifact_b: dict[str, Any]
    ) -> dict[str, Any]:
        """Weave two artifacts together by calculating synergy and identifying shared pivots."""
        score = self.calculate_synergy_score(artifact_a, artifact_b)
        keywords_a = set(self._extract_keywords(artifact_a.get("content", "")))
        keywords_b = set(self._extract_keywords(artifact_b.get("content", "")))
        pivots = list(keywords_a.intersection(keywords_b))

        return {
            "synergy_score": score,
            "pivots": pivots,
            "is_aligned": score >= self.synergy_threshold,
        }

    def _extract_keywords(self, text: str) -> list[str]:
        if not text:
            return []
        words = re.findall(r"\b[A-Z]\w*\b", text)
        return [w for w in words if len(w) > 3]
