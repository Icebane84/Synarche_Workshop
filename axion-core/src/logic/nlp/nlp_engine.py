"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-NLP-001`          | The Sovereign ID. |
| **Official Name**   | `nlp_engine.py`               | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-NLP`              | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Semantic Resonance (Law 28)**
> Implemented from Blueprint `GVRN.REG.SemanticResonance.md`.
> Ethos: The Word is Seed; The Understanding is Fruit.
"""

import logging
from typing import TYPE_CHECKING, Any

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
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Configure logging
log = logging.getLogger(__name__)

# --- EMOTION LEXICON ---
INITIAL_EMOTION_LEXICON = {
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
        # WLF Specific examples
        "shadow self": ["anxiety", "fear", "dread"],
        "oathbringer": ["unease", "power", "fear"],
        "inner flame": ["hope", "resilience", "determination"],
        "valerius": ["suspicion", "unease", "respect"],
        "serafina": ["compassion", "trust", "hope"],
        "garrett": ["loyalty", "pragmatism", "concern"],
    },
    "concept": {
        "family": ["love", "belonging", "stress"],
        "betrayal": ["anger", "sadness", "pain"],
        "resilience": ["hope", "determination", "strength"],
    },
    "contextual": {
        "dark forest": ["fear", "mystery", "unease"],
        "battle": ["fear", "anger", "excitement", "determination"],
    },
}


class NLPProcessor:
    """Handles core NLP tasks like tokenization and entity extraction."""

    def __init__(self, spacy_model_name: str = "en_core_web_sm") -> None:
        self.model_name = spacy_model_name
        self.nlp: spacy.language.Language | None = None
        if SPACY_AVAILABLE:
            self._load_spacy_model(self.model_name)
        else:
            log.warning("spaCy not installed. NLP functionality will be limited.")

    def _load_spacy_model(self, model_name: str) -> bool:
        """Attempt to load or download the SpaCy model."""
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            log.warning(f"spaCy model {model_name} not found. Attempting download...")
            try:
                spacy_download(model_name)
                self.nlp = spacy.load(model_name)
                return True
            except Exception:
                log.exception("Failed to load SpaCy model")
                return False
        else:
            return True

    def tokenize(self, text: str) -> list[str]:
        """Convert input text into a list of atomic tokens."""
        if not self.nlp:
            return text.split()
        doc = self.nlp(text)
        return [token.text for token in doc]

    def lemmatize(self, text: str) -> list[str]:
        """Reduce words to their canonical base form (lemmas)."""
        if not self.nlp:
            return text.lower().split()
        doc = self.nlp(text)
        return [token.lemma_ for token in doc if token.lemma_.strip()]

    def extract_entities(self, text: str) -> list[tuple[str, str]]:
        """Extract named entities (People, Places, Orgs) from the text substrate."""
        if not self.nlp:
            return []
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]


class EmotionAnalyzer:
    """Analyzes text for emotional resonance."""

    def __init__(self, lexicon: dict | None = None) -> None:
        self.lexicons = lexicon or INITIAL_EMOTION_LEXICON

    def detect_emotions(self, text: str) -> dict[str, float]:
        """Analyze text for emotional triggers and resonance intensities."""
        detected_emotions: dict[str, float] = {}
        if not text:
            return detected_emotions

        normalized_text = text.lower()
        keyword_triggers = self.lexicons.get("keyword", {})

        for keyword, associated_emotions in keyword_triggers.items():
            if keyword in normalized_text:
                for emotion in associated_emotions:
                    if emotion not in detected_emotions:
                        detected_emotions[emotion] = 0.5
        return detected_emotions


class AxionCognition:
    """Core NLP engine for Axion, handling embeddings, NER, and sentiment."""

    LONG_TEXT_THRESHOLD = 20

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.nlp = NLPProcessor()
        self.emotions = EmotionAnalyzer()
        self.embeddings: SentenceTransformer | None = None
        if TRANSFORMERS_AVAILABLE:
            try:
                self.embeddings = SentenceTransformer(model_name)
            except Exception:
                log.exception("Failed to load sentence-transformers")

    def process(self, text: str) -> dict[str, Any]:
        """Full cognitive processing of input text."""
        tokens = self.nlp.tokenize(text)
        lemmas = self.nlp.lemmatize(text)
        entities = self.nlp.extract_entities(text)
        emotions = self.emotions.detect_emotions(text)

        vector = None
        if self.embeddings:
            try:
                vector = self.embeddings.encode(text).tolist()
            except Exception:
                log.exception("Vector search encoding failed")

        # Calculate Magician Efficiency based on Intent/Signal
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
        """Calculates the 'Magician' efficiency multiplier based on detected intent.
        High alignment with 'Omega' concepts or clear structure yields higher scores.
        """
        score = 1.0
        normalized = text.lower()
        lemmas = set(self.nlp.lemmatize(text))

        # Intent triggers (using lemmas for better coverage, e.g., 'solution' -> 'solve')
        if "omega" in normalized:
            score += 0.5
        if "catalyst" in normalized:
            score += 0.3
        if "manifest" in normalized or "manifest" in lemmas:
            score += 0.2
        if "solve" in normalized or "solution" in normalized or "solve" in lemmas:
            score += 0.2

        # Penalty for ambiguity
        if "?" in text and len(text) < self.LONG_TEXT_THRESHOLD:
            score -= 0.2

        return round(max(0.1, score), 2)
