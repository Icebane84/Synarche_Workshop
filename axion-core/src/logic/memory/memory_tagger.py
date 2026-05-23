"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.memory.tagger`                | The Sovereign ID. |
| **Official Name** | `memory_tagger.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |

# ---

## **Block B: State Vector (AGP-001)**

# | State Field   | Value     |
# | :------------ | :-------- |
# | **Coherence** | {resonance}     |
# | **Resonance** | {resonance}     |
# | **Stability** | Stable  |

# ---

### **Block C: Risk & Mitigation (AGP-002)**

# | Risk                 | Mitigation                |
# | :------------------- | :------------------------ |
# | **Logic Drift**      | Strict Linter Enforcement |
# | **Semantic Decay**   | Axiomatic Compass Audit   |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**
"""

import logging
import string
from collections import Counter
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple

# Synarche Imports
try:
    from ..nlp.nlp_engine import NLPProcessor
except ImportError:
    # Fallback for standalone or if path structure differs in tests
    try:
        from nlp.nlp_processor import NLPProcessor  # type: ignore
    except ImportError:
        NLPProcessor = Any  # type: ignore

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    pass

# Configure logging for this module
log = logging.getLogger(__name__)

# Basic English stop words
DEFAULT_STOP_WORDS: Set[str] = {
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "couldn",
    "didn",
    "doesn",
    "hadn",
    "hasn",
    "haven",
    "isn",
    "ma",
    "mightn",
    "mustn",
    "needn",
    "shan",
    "shouldn",
    "wasn",
    "weren",
    "won",
    "wouldn",
}


class MemoryTagger:
    """Responsible for applying high-fidelity tags (Topic Keywords, Entities)
    to memory content using the core NLP layer.
    """

    def __init__(
        self,
        nlp_processor: Optional[Any] = None,
        stop_words: Optional[Set[str]] = None,
    ) -> None:
        """Initializes the MemoryTagger.

        Args:
            nlp_processor: An instance of the NLPProcessor.
            stop_words: An optional set of stop words. If None, uses a default set.

        """
        if nlp_processor is None:
            log.warning(
                "NLPProcessor not provided to MemoryTagger. Attempting lazy initialization."
            )
            try:
                from ..nlp.nlp_engine import NLPProcessor as CoreNLP

                self.nlp = CoreNLP()
            except ImportError:
                log.error("Could not import CoreNLP for lazy initialization.")
                self.nlp = None
        else:
            self.nlp = nlp_processor

        self.stop_words = stop_words if stop_words is not None else DEFAULT_STOP_WORDS
        log.info("MemoryTagger initialized.")

    def _extract_topic_keywords(self, text_content: str, top_n: int = 5) -> List[str]:
        """Internal helper method for topic keyword extraction logic.
        Uses lemmatization, stop word removal, and frequency counting.

        Args:
            text_content: The text to process.
            top_n: Number of keywords to return.

        Returns:
            A list of keywords.

        """
        if self.nlp is None or not hasattr(self.nlp, "nlp"):
            log.error("NLPProcessor not available for keyword extraction.")
            return []

        # Lemmatize via core NLP
        try:
            lemmas = self.nlp.lemmatize(text_content)
            if not lemmas:
                return []
        except Exception as e:
            log.error(f"Error during lemmatization for keyword extraction: {e}")
            return []

        # Filter stop words and punctuation
        try:
            filtered_lemmas = [
                lemma.lower()
                for lemma in lemmas
                if lemma.lower() not in self.stop_words
                and lemma not in string.punctuation
                and lemma.strip()
            ]
        except Exception as e:
            log.error(f"Error during lemma filtering: {e}")
            return []

        if not filtered_lemmas:
            return []

        try:
            frequency = Counter(filtered_lemmas)
            top_keywords = [lemma for lemma, count in frequency.most_common(top_n)]
            return top_keywords
        except Exception as e:
            log.error(f"Error during keyword frequency calculation: {e}")
            return []

    def _extract_entities(self, text_content: str) -> List[Tuple[str, str]]:
        """Extracts entities using the NLPProcessor.

        Args:
            text_content: The text to process.

        Returns:
            A list of (entity, label) tuples.

        """
        if self.nlp is None:
            return []

        try:
            entities = self.nlp.extract_entities(text_content)
            return entities if entities is not None else []
        except Exception as e:
            log.error(f"Error during entity extraction: {e}")
            return []

    def apply_tags(self, memory_content: str) -> Dict[str, List[Any]]:
        """Applies Topic Keyword and Entity tags to the provided memory content.

        Args:
            memory_content: The text content of the memory.

        Returns:
            A dictionary containing 'topic_keywords' and 'entities'.

        """
        if not isinstance(memory_content, str) or not memory_content:
            return {}

        try:
            keywords = self._extract_topic_keywords(memory_content)
            entities_with_labels = self._extract_entities(memory_content)

            tags_dict = {"topic_keywords": keywords, "entities": entities_with_labels}
            log.debug(f"Applied tags: {tags_dict}")
            return tags_dict
        except Exception as e:
            log.error(f"Unexpected error in apply_tags: {e}")
            return {}


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.memory.tagger VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 3ab119ff8847e0cf
# ---
