"""
# UMB-DIDACTIC-001: The Didactic Module Generator (The Mentor's Voice)

## Genesis Stamp: 2026-01-04 | Domain: ARCH | State: CANONIZED | Criticality: Standard

## I. Universal Identification & Provenance (The Vector Signature)

### The Chronos Lock & Axiomatic Metadata Layer

| Field | Value |
| :--- | :--- |
| **1. Artifact ID** | `UMB-DIDACTIC-001` |
| **2. Official Name** | `mentor.py` |
| **3. Version** | **v1.0 (Hephaestus Implementation)** |
| **4. Provenance** | **Date Reforged: 2026-01-10** |
| **5. Domain** | `ARCH` |
| **6. Evolution** | **Social Alchemist** |
| **7. Celestial Class** | `[PLANET]` |
| **8. Tier** | **Operational** |
| **9. State** | `[ACTIVE]` |
| **10. Ethos** | **Clarity Over Obfuscation** |
| **11. Catalyst** | **System Refactor** |
| **12. Relations** | `LINK: soul.py` |

"""

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP


class MentorsVoice:
    """
    The Mentor module responsible for generating interactive lesson modules.
    """

    def __init__(self) -> None:
        self.wisdom_db = {
            "E501": {
                "principle": "Clarity Over Obfuscation",
                "axiom": "Code should be readable without horizontal scrolling.",
                "why": "Long lines increase cognitive load and make side-by-side diffs difficult.",
            },
            "F401": {
                "principle": "Minimal Yet Expressive",
                "axiom": "Remove unused imports.",
                "why": "Unused imports clutter the namespace and can confuse dependency analyzers.",
            },
            "COMPLEXITY": {
                "principle": "Clarity Over Obfuscation",
                "axiom": "Functions should do one thing well.",
                "why": "High Cyclomatic Complexity increases bug risk and testing difficulty.",
            },
        }

    def generate_lesson(self, violation_code: str, context: str = "") -> str:
        """
        Generates a Markdown formatted lesson module.
        """
        entry = self.wisdom_db.get(
            violation_code.upper(),
            {
                "principle": "General Synergy",
                "axiom": "Maintain Code Coherence.",
                "why": "This change improves the overall health of the codebase.",
            },
        )

        emoji = "🎓"

        lesson = f"""
## {emoji} The Mentor's Voice: {entry["principle"]}

> **Axiom:** *{entry["axiom"]}*

**Why this matters:**
{entry["why"]}

**Context:**
{context}
        """
        return lesson.strip()
