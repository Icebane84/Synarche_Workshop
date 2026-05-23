"""# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-HPRI-002`                                |
| **2. Official Name**   | `context_weave.py`                             |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `SYNG` (Synergy)                               |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[STAR]`                                       |
| **8. Tier**            | **Foundational**                               |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Pattern Recognition**                        |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `LINK: [UMB-LOOM-001]`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |.

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| UMB-LOOM-001 | FEEDS | Provides context for the Cognitive Loom. |
| CORE-CODEX-001 | GOVERNS | This tool is governed by the Supreme Law. |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Synthesis Engine (The High Priestess)
# Synergy Set: The Oracle's Eye
# Primary Stat Buff: Wisdom (+25)
# Passive Ability: Pattern Recognition (Keyword Extraction)
# Cognitive Load Cost: High
# XP Award Value: 150 XP
"""

import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

# Configure Logging to STDOUT
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ContextWeave")

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

    # 4. Compile Results
    report_data = {
        "target": str(file_path.resolve()),
        "token_count": len(tokens),
        "unique_terms": len(freq),
        "top_keywords": [{"term": t, "count": c} for t, c in top_terms],
    }

    # 5. Output The Weave
    logger.info("\n" + "~" * 40)
    logger.info("       CONTEXT WEAVE PATTERN       ")
    logger.info("~" * 40)
    logger.info(f"Target: {file_path.name}")
    logger.info(f"Total Token Count: {len(tokens)}")
    logger.info(f"Unique Term Count: {len(freq)}")
    logger.info("-" * 40)
    logger.info("DOMINANT THREADS (Top Keywords):")

    for term, count in top_terms:
        bar = "|" * (count // 2 if count > 0 else 1)
        logger.info(f"  {term:<15} : {count:>3} {bar}")

    logger.info("-" * 40)
    logger.info("Context Synthesized.")

    # 6. Save Report
    workspace_root = file_path
    while (
        workspace_root.parent != workspace_root
        and not (workspace_root / "axion-core").exists()
    ):
        workspace_root = workspace_root.parent

    log_dir = workspace_root / "_logs"
    if log_dir.exists():
        log_path = log_dir / "context_weave_report.json"
        try:
            with open(log_path, "w") as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"\nAudit saved to {log_path.relative_to(workspace_root)}")
        except Exception:
            logger.exception("Failed to save audit log")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python context_weave.py <text_file_path>")
        sys.exit(1)

    weave_context(Path(sys.argv[1]))
