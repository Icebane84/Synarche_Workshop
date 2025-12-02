"""# NLP-EMOTION-ANALYZER: Sentiment & Affective Context (Axion NLP Layer).

## Genesis Stamp: 2026-03-03 | Domain: NLP | State: ACTIVE | Criticality: Intelligence

# I. Universal Identification & Provenance (UIP-V13)

| Key | Value |
| :--- | :--- |
| **Artifact ID** | `NLP-EMOTION-ANALYZER-v1.0` |
| **Official Name** | `emotion_analyzer.py` |
| **Version** | **v1.0 [ALPHA]** |
| **Domain** | `NLP` |
| **Evolution** | **Cognitive Ascension** |
| **Celestial Class** | `[MOON]` |
| **Status (State)** | `[ACTIVE]` |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` |
| **Provenance** | `Date Reforged: 2026-03-03` |

---

# II. Axiomatic Governance & Purpose
To provide lightweight, lexicon-based emotional analysis of memory content and user interactions within Axion Prime.

# III. The Architectural Spine
- **Attributes**: `lexicons` (dict)
- **Methods**: `detect_emotions`

# V. Systemic Relationships & Impact
- `MemorySystem`: Uses this to tag memories with emotional context.
- `ExperienceLogger`: Provides the raw text for analysis.

# VI. RPG Framework Integration
- **Affective Resonance**: Matching the agent's response to the detected emotion increases resonance stats.

# VII. Actionable Prompt Packet
- "Analyze the emotional trajectory of the last 10 interactions."
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

    def __init__(self, lexicon: dict | None = None) -> None:
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
