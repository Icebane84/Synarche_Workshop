"""
## **[ARTIFACT START]**
## **Block A: The Identification Lock (UIP-V15)**
| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.nlp.engine`                | The Sovereign ID. |
| **Official Name** | `nlp_engine.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |
## **[ARTIFACT END]**
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
    }
}

class NLPProcessor:
    def __init__(self, spacy_model_name: str = "en_core_web_sm") -> None:
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(spacy_model_name)
            except OSError:
                try:
                    spacy_download(spacy_model_name)
                    self.nlp = spacy.load(spacy_model_name)
                except Exception:
                    log.exception("Failed to load SpaCy model")

    def tokenize(self, text: str) -> list[str]:
        if not self.nlp:
            return text.split()
        doc = self.nlp(text)
        return [token.text for token in doc]

    def lemmatize(self, text: str) -> list[str]:
        if not self.nlp:
            return text.lower().split()
        doc = self.nlp(text)
        return [token.lemma_ for token in doc if token.lemma_.strip()]

    def extract_entities(self, text: str) -> list[tuple[str, str]]:
        if not self.nlp:
            return []
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

class EmotionAnalyzer:
    def __init__(self, lexicon: dict | None = None) -> None:
        self.lexicons = lexicon or INITIAL_EMOTION_LEXICON

    def detect_emotions(self, text: str) -> dict[str, float]:
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
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.nlp = NLPProcessor()
        self.emotions = EmotionAnalyzer()
        self.embeddings = None
        if TRANSFORMERS_AVAILABLE:
            try:
                self.embeddings = SentenceTransformer(model_name)
            except Exception:
                log.exception("Failed to load sentence-transformers")

    def process(self, text: str) -> dict[str, Any]:
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
        score = 1.0
        normalized = text.lower()
        if "omega" in normalized: score += 0.5
        if "catalyst" in normalized: score += 0.3
        return round(max(0.1, score), 2)

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.nlp.engine VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: b66317b25fa07eaa
