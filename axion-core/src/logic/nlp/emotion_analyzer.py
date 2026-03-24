"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-LOGIC-EMO-ANLZ-001`     | The Sovereign ID. |
| **Official Name**   | `emotion_analyzer.py`         | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-LOGIC-NLP`              | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Affective resonance (Law 28)**
> Implemented from Blueprint `GVRN.REG.AffectiveResonance.md`.
> Ethos: The Feeling is Seed; The Harmony is Truth.
"""

import logging

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
        "success": ["joy", "pride", "fulfillment"],
        "victory": ["joy", "triumph", "exhilaration"],
    }
}


class EmotionAnalyzer:
    """Analyzes text to detect potential emotional context based on predefined
    lexicons and triggers.
    """

    def __init__(self, lexicon: dict[str, dict[str, list[str]]] | None = None) -> None:
        self.lexicons = lexicon if lexicon is not None else INITIAL_EMOTION_LEXICON
        if not isinstance(self.lexicons, dict) or "keyword" not in self.lexicons:
            log.warning("Invalid or missing 'keyword' triggers in lexicon.")
            if not isinstance(self.lexicons, dict):
                self.lexicons = {}
            if "keyword" not in self.lexicons:
                self.lexicons["keyword"] = {}
        log.info("EmotionAnalyzer initialized.")

    def detect_emotions(self, text: str) -> dict[str, float]:
        """Detects emotions in the input text based on keyword triggers.
        Returns a dict of {emotion: intensity}.
        """
        detected_emotions: dict[str, float] = {}
        if not isinstance(text, str) or not text:
            return detected_emotions

        try:
            normalized_text = text.lower()
            keyword_triggers = self.lexicons.get("keyword", {})

            for keyword, associated_emotions in keyword_triggers.items():
                if keyword in normalized_text:
                    for emotion in associated_emotions:
                        if not isinstance(emotion, str):
                            continue
                        if emotion not in detected_emotions:
                            detected_emotions[emotion] = 0.5

            return detected_emotions

        except Exception as e:
            log.exception(f"Unexpected error during emotion detection: {e}")
            return {}
