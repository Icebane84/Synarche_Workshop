"""# TOOL-STAR-003: Catalyst Weaver Tester (Coherence Filter).

## I. Universal Identification & Provenance (The Vector Signature)
| Field                  | Value                                                    |
| :--------------------- | :------------------------------------------------------- |
| **1. Artifact ID**     | `TOOL-STAR-003`                                          |
| **2. Official Name**   | `test_weaver.py`                                         |
| **3. Version**         | **v11.1**                                                |
| **4. Provenance**      | **Reforged: 2026-01-30**                                 |
| **5. Domain**          | `OSLM`                                                   |
| **6. Evolution**       | **Cognitive Ascension**                                  |
| **7. Celestial Class** | `[PLANET]`                                               |
| **8. Tier**            | **Operational**                                          |
| **9. Status (State)**  | `[ACTIVE]`                                               |
| **10. Ethos**          | **Coherence Verification**                               |
| **11. Catalyst**       | **Test Execution**                                       |
| **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CHAR-AXION-001, WIELDS, The Star persona uses this tool for verification.
GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
TOOL-HPRI-006, TESTS, This tool specifically tests the Catalyst Weaver.

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Coherence Filter (The Star)
# Synergy Set: The Star's Radiance
# Primary Stat Buff: Perception (+10), Logic (+15)
# Passive Ability: The Guiding Light (Algorithm Verification)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

---

## IV. Actionable Prompt Packet (APP)
| Command ID | Action | Impact |
| :--- | :--- | :--- |
| `CMD: TEST_WEAVER` | Run Catalyst Tests | Algorithm Integrity |
| `⚡ EXECUTE: VERIFY_SYNERGY` | Deep Logic Audit | Logic Restoration |
"""

import os
import sys
import unittest

# Add src path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "..", "src"))

from hephaestus.lib.catalyst_weaver import CatalystWeaver


class TestCatalystWeaver(unittest.TestCase):
    def setUp(self) -> None:
        self.weaver = CatalystWeaver()

    def test_extension_alignment(self) -> None:
        # Test .ts and .css alignment
        art_a = {"id": "A", "official_name": "component.ts", "tags": [], "content": ""}
        art_b = {"id": "B", "official_name": "component.css", "tags": [], "content": ""}

        # 0.1 for extension alignment
        score = self.weaver.calculate_synergy_score(art_a, art_b)
        self.assertAlmostEqual(score, 0.1)

    def test_external_signal(self) -> None:
        art_a = {"id": "A", "content": "", "tags": []}
        art_b = {"id": "B", "content": "", "tags": []}

        # 0.3 from external signal
        score = self.weaver.calculate_synergy_score(art_a, art_b, external_signal=0.5)
        self.assertAlmostEqual(score, 0.3)

    def test_full_synergy(self) -> None:
        # 1. Keywords (Overlap "Phoenix", "Axion") -> 0.2
        # 2. Tabs (Overlap "Core") -> 0.2
        # 3. Reference ("B" in A) -> 0.2
        # 4. Extension (.py + .md) -> 0.1
        # 5. External Signal -> 0.3
        # Total = 1.0 (capped)

        art_a = {
            "id": "A",
            "official_name": "script.py",
            "tags": ["Core"],
            "content": "Referencing artifact B here. Phoenix Axion.",
        }
        art_b = {
            "id": "B",
            "official_name": "docs.md",
            "tags": ["Core"],
            "content": "Phoenix Axion is great.",
        }

        score = self.weaver.calculate_synergy_score(art_a, art_b, external_signal=1.0)
        self.assertGreaterEqual(score, 1.0)

    def test_weave_threshold(self) -> None:
        art_a = {"id": "A", "content": "", "tags": []}
        art_b = {"id": "B", "content": "", "tags": []}

        # Score 0.0 -> No Link
        link = self.weaver.weave(art_a, art_b)
        self.assertIsNone(link)

        # Score 0.5 (via external) -> Link
        link = self.weaver.weave(
            art_a, art_b, external_signal=0.6
        )  # 0.3 max? Wait, allow signal to match threshold logic.
        # Max external signal is 0.3. So 0.3 alone is not enough for 0.5 threshold.
        # Need at least 0.2 more from somewhere.

        # Let's add tags for +0.2
        art_a["tags"] = ["Shared"]
        art_b["tags"] = ["Shared"]
        # Score = 0.2 (tags) + 0.3 (external) = 0.5

        link = self.weaver.weave(art_a, art_b, external_signal=1.0)
        self.assertIsNotNone(link)
        self.assertEqual(link["synergy_score"], 0.5)


if __name__ == "__main__":
    unittest.main()
