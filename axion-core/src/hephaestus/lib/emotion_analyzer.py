# emotion_analyzer.py
# (Harvested & Enhanced for OMEGA v15.0)

import logging
import sys

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
        "shadow self": ["anxiety", "fear", "dread"],
        "oathbringer": ["unease", "power", "fear"],
        "inner flame": ["hope", "resilience", "determination"],
    },
    "concept": {
        "family": ["love", "belonging", "stress"],
        "betrayal": ["anger", "sadness", "pain"],
        "resilience": ["hope", "determination", "strength"]
    }
}

class EmotionAnalyzer:
    """Analyzes text to detect potential emotional context and narrative resonance."""

    def __init__(self, lexicon: dict | None = None) -> None:
        self.lexicons = lexicon if lexicon is not None else INITIAL_EMOTION_LEXICON
        if not isinstance(self.lexicons, dict) or "keyword" not in self.lexicons:
            log.warning("WARN [EmotionAnalyzer]: Invalid lexicon structure.")

    def detect_emotions(self, text: str) -> dict[str, float]:
        """Detects emotions in the input text based on keyword triggers."""
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
