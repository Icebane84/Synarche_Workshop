"""
### **Block A: The Identification Lock (UIP-V15)**

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-HEPH-RESO-SCAN-001`     | The Sovereign ID. |
| **Official Name**   | `resonance_scanner.py`        | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-HEPHAESTUS`             | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Structural Integrity`         | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Resonance Geometry (Law 28)**
> Implemented from Blueprint `GVRN.REG.ResonanceGeometry.md`.
> Ethos: The Frequency is High; The Alignment is Truth.
"""

import math
import re
from pathlib import Path

RESONANCE_MARKERS = [
    "UMB-",
    "AOP-",
    "GUCA-",
    "CODEX-",
    "Phoenix-Class",
    "Synarche",
]

VALID_EXTENSIONS = {".md", ".json", ".ts", ".tsx", ".py"}


def is_aligned(file_path: Path) -> bool:
    """Checks if a file is aligned based on Resonance Markers and integrity."""
    try:
        if any(marker in file_path.name for marker in RESONANCE_MARKERS):
            return True

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in content for marker in RESONANCE_MARKERS):
            return True

        # Optional: Add structural check for UIP headers
        if "Identification Lock" in content or "ARTIFACT START" in content:
            return True

    except Exception:
        return False
    return False


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculates cosine similarity between two text blocks."""

    def extract_terms(text: str) -> list[str]:
        """Convert text substrate into a list of normalized, non-stopword terms."""
        words = re.findall(r"\b\w{4,}\b", text.lower())
        stop_words = {"this", "that", "with", "from", "your", "have", "will"}
        return [w for w in words if w not in stop_words]

    terms1 = extract_terms(text1)
    terms2 = extract_terms(text2)

    if not terms1 or not terms2:
        return 0.0

    def get_freq(terms: list[str]) -> dict[str, int]:
        """Compute term frequency distribution for the given terms."""
        freq = {}
        for t in terms:
            freq[t] = freq.get(t, 0) + 1
        return freq

    v1, v2 = get_freq(terms1), get_freq(terms2)
    intersection = set(v1.keys()) & set(v2.keys())
    numerator = sum(v1[x] * v2[x] for x in intersection)
    sum1 = sum(x**2 for x in v1.values())
    sum2 = sum(x**2 for x in v2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    return float(numerator) / denominator if denominator else 0.0
