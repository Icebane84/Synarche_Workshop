"""
## **[ARTIFACT START]**

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.resonance.scanner`                | The Sovereign ID. |
| **Official Name** | `resonance_scanner.py`                   | The Filename.     |
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

import math
import re
from pathlib import Path
from typing import Dict, List, Set, Any

RESONANCE_MARKERS: List[str] = [
    "UMB-",
    "AOP-",
    "GUCA-",
    "CODEX-",
    "Phoenix-Class",
    "Synarche",
]

VALID_EXTENSIONS: Set[str] = {".md", ".json", ".ts", ".tsx", ".py"}


def is_aligned(file_path: Path) -> bool:
    """
    Checks if a file is aligned based on Resonance Markers and header integrity.

    Args:
        file_path: The path to the file to check.

    Returns:
        True if aligned, False otherwise.
    """
    try:
        # Check filename first
        if any(marker in file_path.name for marker in RESONANCE_MARKERS):
            return True

        # Check content
        if file_path.is_file():
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(marker in content for marker in RESONANCE_MARKERS):
                return True

            # Check for UIP headers
            if "Identification Lock" in content or "ARTIFACT START" in content:
                return True

    except Exception:
        return False
    return False


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates cosine similarity between two text blocks based on term frequency.

    Args:
        text1: First text block.
        text2: Second text block.

    Returns:
        Cosine similarity score (0.0 to 1.0).
    """

    def extract_terms(text: str) -> List[str]:
        """Convert text substrate into a list of normalized terms."""
        words = re.findall(r"\b\w{4,}\b", text.lower())
        stop_words = {"this", "that", "with", "from", "your", "have", "will"}
        return [w for w in words if w not in stop_words]

    terms1 = extract_terms(text1)
    terms2 = extract_terms(text2)

    if not terms1 or not terms2:
        return 0.0

    def get_freq(terms: List[str]) -> Dict[str, int]:
        """Compute term frequency distribution."""
        freq: Dict[str, int] = {}
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

# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.resonance.scanner VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: c357324dd52f06fb
# ---
