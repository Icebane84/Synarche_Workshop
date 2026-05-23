#!/usr/bin/env python3
"""# TOOL-HPRI-002: The Context Weave (Cognitive Loom).

## I. Universal Identification & Provenance
| Attribute | Value |
| :--- | :--- |
| **Artifact ID** | `TOOL-HPRI-002` |
| **Official Name** | `context_weave.py` |
| **Version** | **v11.0** |
| **Domain** | `SYNG` |
| **Evolution** | **Cognitive Ascension** |
| **Signal (ESF)** | `ESF-ALPHA` |
| **Status (State)** | `[ACTIVE]` |
| **Tier** | **Strategic** |
| **Celestial Class** | `[STAR]` |
| **Governance** | `GVRN-SYNERGY-001` |
| **Upstream** | `Ingestion Engine` |
| **Downstream** | `Tarot Forge UI` |
| **Provenance** | `Genesis Stamp: 2026-01-25` |
| **Relations** | `Governed by GVRN-SYNERGY-001` |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Synthesis Engine (The High Priestess)
# Synergy Set: The Oracle's Eye
# Primary Stat Buff: Wisdom (+25)
# Passive Ability: Pattern Recognition (Keyword Extraction)
# Cognitive Load Cost: High
# XP Award Value: 150 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: WEAVE_CONTEXT` | Extract Keywords | Generate Meta-Tags |
| `⚡ EXECUTE: SYNTHESIZE` | Abstract Summary | Create High-Level View |
"""

import logging
import re
import sys
from collections import Counter
from pathlib import Path

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

STOP_WORDS = {
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "i",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
    "is",
    "are",
    "was",
    "were",
    "has",
}


def weave_context(file_path: Path) -> None:
    """Analyzes a text file to extract key themes (frequency analysis).
    This acts as a 'Context Loom', spinning raw text into structured keywords.
    """
    if not file_path.exists():
        logger.error(f"Target file not found: {file_path}")
        return

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        logger.exception(f"Failed to read file: {e}")
        return

    # 1. Tokenize & Clean
    # Lowercase, remove non-alphanumeric (keep spaces), split
    cleaned = re.sub(r"[^a-z0-9\s]", "", content.lower())
    tokens = cleaned.split()

    # 2. Filter Stop Words
    keywords = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

    # 3. Frequency Analysis
    freq = Counter(keywords)
    top_terms = freq.most_common(20)

    # 4. Output The Weave
    logger.info("\n" + "~" * 40)
    logger.info("       CONTEXT WEAVE PATTERN       ")
    logger.info("~" * 40)
    logger.info(f"Target: {file_path.name}")
    logger.info(f"Total Token Count: {len(tokens)}")
    logger.info(f"Unique Term Count: {len(freq)}")
    logger.info("-" * 40)
    logger.info("DOMINANT THREADS (Top Keywords):")

    for term, count in top_terms:
        # Visualizing frequency density
        bar = "|" * (count // 2 if count > 0 else 1)  # Scale bar
        logger.info(f"  {term:<15} : {count:>3} {bar}")

    logger.info("-" * 40)
    logger.info("Context Synthesized.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python context_weave.py <text_file_path>")
        sys.exit(1)

    weave_context(Path(sys.argv[1]))
