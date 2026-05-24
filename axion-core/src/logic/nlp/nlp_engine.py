"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.nlp.engine`                | The Sovereign ID. |
| **Official Name** | `nlp_engine.py`                   | The Filename.     |
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
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    import spacy
    from sentence_transformers import SentenceTransformer

# Try to import optional dependencies
try:
    import spacy
    from spacy.cli import download as spacy_download

    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer

    TRANSFORMERS_AVAILABLE = True
except Exception:
    TRANSFORMERS_AVAILABLE = False

# Configure logging
log = logging.getLogger(__name__)

INITIAL_EMOTION_LEXICON: Dict[str, Dict[str, List[str]]] = {
    "keyword": {
        "happy": ["joy", "contentment"],
        "glad": ["joy"],
        "joyful": ["joy", "excitement"],
        "sad": ["sadness", "melancholy"],
        "unhappy": ["sadness"],
        "grief": ["sadness", "pain"],
        "angry": ["anger"],
        "furious": ["anger"],
        "irritated": ["anger", "frustration"],
        "afraid": ["fear"],
        "scared": ["fear", "anxiety"],
        "anxious": ["anxiety", "fear"],
        "surprised": ["surprise"],
        "amazed": ["surprise", "awe"],
        "disgusted": ["disgust"],
        "love": ["love", "joy"],
        "hate": ["anger", "disgust"],
        "hope": ["hope", "anticipation"],
        "lost": ["sadness", "confusion", "fear"],
        "fail": ["disappointment", "frustration", "sadness"],
    }
}


class NLPProcessor:
    """Core NLP processing unit using SpaCy for tokenization, lemmatization, and entity extraction.
    Provides fallbacks if SpaCy is unavailable.
    """

    def __init__(self, spacy_model_name: str = "en_core_web_sm") -> None:
        """Initializes the NLPProcessor.

        Args:
            spacy_model_name: The name of the SpaCy model to load.

        """
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(spacy_model_name)
            except OSError:
                try:
                    log.info(f"Downloading SpaCy model: {spacy_model_name}")
                    spacy_download(spacy_model_name)
                    self.nlp = spacy.load(spacy_model_name)
                except Exception:
                    log.exception(f"Failed to load SpaCy model: {spacy_model_name}")

    def tokenize(self, text: str) -> List[str]:
        """Splits text into individual tokens.

        Args:
            text: The string to tokenize.

        Returns:
            A list of tokens.

        """
        if not self.nlp:
            return text.split()
        doc = self.nlp(text)
        return [token.text for token in doc]

    def lemmatize(self, text: str) -> List[str]:
        """Reduces words to their base or dictionary form (lemma).

        Args:
            text: The string to lemmatize.

        Returns:
            A list of lemmas.

        """
        if not self.nlp:
            return text.lower().split()
        doc = self.nlp(text)
        return [token.lemma_ for token in doc if token.lemma_.strip()]

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """Identifies and categorizes named entities within the text.

        Args:
            text: The string to analyze.

        Returns:
            A list of (entity_text, entity_label) tuples.

        """
        if not self.nlp:
            return []
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]


class EmotionAnalyzer:
    """Detects emotional markers and intensity within text using a lexicon-based approach."""

    def __init__(
        self, lexicon: Optional[Dict[str, Dict[str, List[str]]]] = None
    ) -> None:
        """Initializes the EmotionAnalyzer.

        Args:
            lexicon: Optional custom lexicon mapping.

        """
        self.lexicons = lexicon or INITIAL_EMOTION_LEXICON

    def detect_emotions(self, text: str) -> Dict[str, float]:
        """Analyzes the input text for emotional triggers defined in the lexicon.

        Args:
            text: The input string.

        Returns:
            A dictionary mapping emotion names to detected intensity scores.

        """
        detected_emotions: Dict[str, float] = {}
        if not text:
            return detected_emotions
        normalized_text = text.lower()
        keyword_triggers = self.lexicons.get("keyword", {})
        for keyword, associated_emotions in keyword_triggers.items():
            if keyword in normalized_text:
                for emotion in associated_emotions:
                    if emotion not in detected_emotions:
                        detected_emotions[emotion] = 0.5
                    else:
                        detected_emotions[emotion] = min(
                            1.0, detected_emotions[emotion] + 0.1
                        )
        return detected_emotions


class AxionCognition:
    """Master cognitive interface that aggregates NLP, emotion, and semantic processing."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """Initializes the AxionCognition system.

        Args:
            model_name: The name of the sentence-transformers model for embeddings.

        """
        self.nlp = NLPProcessor()
        self.emotions = EmotionAnalyzer()
        self.embeddings = None
        if TRANSFORMERS_AVAILABLE:
            try:
                self.embeddings = SentenceTransformer(model_name)
            except Exception:
                log.exception(
                    f"Failed to load sentence-transformers model: {model_name}"
                )

    def process(self, text: str) -> Dict[str, Any]:
        """Performs a full cognitive scan of the provided text.

        Args:
            text: The string to process.

        Returns:
            A dictionary containing tokens, lemmas, entities, emotions, vectors, and efficiency scores.

        """
        tokens = self.nlp.tokenize(text)
        lemmas = self.nlp.lemmatize(text)
        entities = self.nlp.extract_entities(text)
        emotions = self.emotions.detect_emotions(text)
        vector = None
        if self.embeddings:
            try:
                vector = self.embeddings.encode(text).tolist()
            except Exception:
                log.exception("Semantic vector encoding failed.")
        efficiency = self.get_magician_efficiency(text)
        return {
            "tokens": tokens,
            "lemmas": lemmas,
            "entities": entities,
            "emotions": emotions,
            "vector": vector,
            "magician_efficiency": efficiency,
        }

    def get_magician_efficiency(self, text: str) -> float:
        """Calculates a 'Magician Efficiency' score based on the presence of key OMEGA terms.

        Args:
            text: The text to evaluate.

        Returns:
            A float representing the efficiency score.

        """
        score = 1.0
        normalized = text.lower()
        if "omega" in normalized:
            score += 0.5
        if "catalyst" in normalized:
            score += 0.3
        return round(max(0.1, score), 2)


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.nlp.engine VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: b66317b25fa07eaa
# ---
