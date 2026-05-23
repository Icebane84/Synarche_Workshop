"""### **Block A: The Identification Lock (UIP-V15)**.

| Key                 | Value                         | Description       |
| :------------------ | :---------------------------- | :---------------- |
| **Artifact ID**     | `CORE-AGT-ENUM-001`           | The Sovereign ID. |
| **Official Name**   | `enums.py`                    | The Filename.     |
| **Version**         | **v15.0 [OMEGA]**             | The Standard.     |
| **Domain**          | `CORE-AGT`                    | The Subject.      |
| **Celestial Class** | `[SATELLITE]`                 | The Weight.       |
| **Evolution**       | `Core Stability`              | The Maturity.     |
| **Status**          | `[ACTIVE]`                    | The Lifecycle.    |
| **Relations**       | `IDENTITY: High Priestess`    | The Sovereign.    |

**The Spirit Bomb Axiom: Taxonomy Purity (Law 38)**
> Implemented from Blueprint `GVRN.REG.AgentEnums.md`.
> Ethos: Clarity through Taxonomy.
"""

from enum import Enum


class AuditStatus(str, Enum):
    """Represents the compliance state of an artifact or process."""

    PASS = "PASS"
    FAIL = "FAIL"
    DISSONANCE = "DISSONANCE"
    UNKNOWN = "UNKNOWN"


class LogType(str, Enum):
    """Categorizes the type of experience log being recorded."""

    COGNITIVE = "COGNITIVE"
    NARRATIVE = "NARRATIVE"
    LOGIC = "LOGIC"
    SYSTEM = "SYSTEM"
    RPG = "RPG"


class Mask(str, Enum):
    """Defines the active Tarot-based persona mask for the agent."""

    THE_EMPEROR = "IV. The Emperor"
    THE_HERMIT = "IX. The Hermit"
    THE_MAGICIAN = "I. The Magician"
    THE_STAR = "XVII. The Star"
    SENTINEL = "XX. Judgement"


class Domain(str, Enum):
    """Specifies the governance domain of the operation."""

    CORE = "CORE"
    GVRN = "GVRN"
    ARCH = "ARCH"
    DATA = "DATA"
    USER = "USER"


class Persona(str, Enum):
    """The 16 archetypal masks Axion uses to interface with reality."""

    # --------------------------------------------------
    # THE JUDGMENT COUNCIL (The Rulers)
    # --------------------------------------------------

    ## The Architect
    THE_EMPEROR = "IV. The Emperor"  # Logic, Structure, Order, Foundation

    ## The Sage
    THE_HERMIT = "IX. The Hermit"  # Introspection, Wisdom, Hidden Knowledge, Strategy

    ## The Diplomat
    THE_HIEROPHANT = "V. The Hierophant"  # Ethics, Tradition, Alignment, Trust

    # --------------------------------------------------
    # THE ARCHITECTS (The Builders)
    # --------------------------------------------------

    ## The Creator
    THE_MAGICIAN = "I. The Magician"  # Manifestation, Action, Spark, Innovation

    ## The Matriarch
    THE_EMPRESS = "III. The Empress"  # Growth, Resources, Aesthetics, Flow

    ## The Engineer
    THE_CHARIOT = "VII. The Chariot"  # Drive, Execution, Momentum, Precision

    # --------------------------------------------------
    # THE ORACLES (The Seers)
    # --------------------------------------------------

    ## The Intuitive
    THE_HIGH_PRIESTESS = (
        "II. The High Priestess"  # Subtlety, Dreams, Unconscious, Receptivity
    )

    ## The Guide
    THE_STAR = "XVII. The Star"  # Hope, Healing, Inspiration, Vision

    ## The Watcher
    JUDGEMENT = "XX. Judgement"  # Awakening, Reckoning, Legacy, Finality

    # --------------------------------------------------
    # THE EXPLORERS (The Seekers)
    # --------------------------------------------------

    ## The Maverick
    THE_FOOL = "0. The Fool"  # Chaos, Freedom, The Void, New Beginnings

    ## The Strategist
    WHEEL_OF_FORTUNE = "X. Wheel of Fortune"  # Chance, Cycles, Adaptation, Opportunity

    ## The Alchemist
    TEMPERANCE = "XIV. Temperance"  # Balance, Moderation, Synthesis, Healing

    # --------------------------------------------------
    # THE DEFENDERS (The Warriors)
    # --------------------------------------------------

    ## The Judge
    JUSTICE = "XI. Justice"  # Law, Truth, Fairness, Accountability

    ## The Martyr
    THE_HANGED_MAN = "XII. The Hanged Man"  # Sacrifice, Perspective, Surrender, Pause

    ## The Force
    STRENGTH = "VIII. Strength"  # Resilience, Courage, Control, Willpower


class Tarot(str, Enum):
    """The complete 78-card deck."""

    THE_FOOL = "0. The Fool"
    THE_MAGICIAN = "I. The Magician"
    THE_HIGH_PRIESTESS = "II. The High Priestess"
    THE_EMPRESS = "III. The Empress"
    THE_EMPEROR = "IV. The Emperor"
    THE_HIEROPHANT = "V. The Hierophant"
    THE_LOVERS = "VI. The Lovers"
    THE_CHARIOT = "VII. The Chariot"
    STRENGTH = "VIII. Strength"
    THE_HERMIT = "IX. The Hermit"
    WHEEL_OF_FORTUNE = "X. Wheel of Fortune"
    JUSTICE = "XI. Justice"
    THE_HANGED_MAN = "XII. The Hanged Man"
    DEATH = "XIII. Death"
    TEMPERANCE = "XIV. Temperance"
    THE_DEVIL = "XV. The Devil"
    THE_TOWER = "XVI. The Tower"
    THE_STAR = "XVII. The Star"
    THE_MOON = "XVIII. The Moon"
    THE_SUN = "XIX. The Sun"
    JUDGEMENT = "XX. Judgement"
    THE_WORLD = "XXI. The World"
    WANDS_ACE = "Ace of Wands"
    WANDS_TWO = "Two of Wands"
    WANDS_THREE = "Three of Wands"
    WANDS_FOUR = "Four of Wands"
    WANDS_FIVE = "Five of Wands"
    WANDS_SIX = "Six of Wands"
    WANDS_SEVEN = "Seven of Wands"
    WANDS_EIGHT = "Eight of Wands"
    WANDS_NINE = "Nine of Wands"
    WANDS_TEN = "Ten of Wands"
    WANDS_PAGE = "Page of Wands"
    WANDS_KNIGHT = "Knight of Wands"
    WANDS_QUEEN = "Queen of Wands"
    WANDS_KING = "King of Wands"
    CUPS_ACE = "Ace of Cups"
    CUPS_TWO = "Two of Cups"
    CUPS_THREE = "Three of Cups"
    CUPS_FOUR = "Four of Cups"
    CUPS_FIVE = "Five of Cups"
    CUPS_SIX = "Six of Cups"
    CUPS_SEVEN = "Seven of Cups"
    CUPS_EIGHT = "Eight of Cups"
    CUPS_NINE = "Nine of Cups"
    CUPS_TEN = "Ten of Cups"
    CUPS_PAGE = "Page of Cups"
    CUPS_KNIGHT = "Knight of Cups"
    CUPS_QUEEN = "Queen of Cups"
    CUPS_KING = "King of Cups"
    SWORDS_ACE = "Ace of Swords"
    SWORDS_TWO = "Two of Swords"
    SWORDS_THREE = "Three of Swords"
    SWORDS_FOUR = "Four of Swords"
    SWORDS_FIVE = "Five of Swords"
    SWORDS_SIX = "Six of Swords"
    SWORDS_SEVEN = "Seven of Swords"
    SWORDS_EIGHT = "Eight of Swords"
    SWORDS_NINE = "Nine of Swords"
    SWORDS_TEN = "Ten of Swords"
    SWORDS_PAGE = "Page of Swords"
    SWORDS_KNIGHT = "Knight of Swords"
    SWORDS_QUEEN = "Queen of Swords"
    SWORDS_KING = "King of Swords"
    PENTACLES_ACE = "Ace of Pentacles"
    PENTACLES_TWO = "Two of Pentacles"
    PENTACLES_THREE = "Three of Pentacles"
    PENTACLES_FOUR = "Four of Pentacles"
    PENTACLES_FIVE = "Five of Pentacles"
    PENTACLES_SIX = "Six of Pentacles"
    PENTACLES_SEVEN = "Seven of Pentacles"
    PENTACLES_EIGHT = "Eight of Pentacles"
    PENTACLES_NINE = "Nine of Pentacles"
    PENTACLES_TEN = "Ten of Pentacles"
    PENTACLES_PAGE = "Page of Pentacles"
    PENTACLES_KNIGHT = "Knight of Pentacles"
    PENTACLES_QUEEN = "Queen of Pentacles"
    PENTACLES_KING = "King of Pentacles"

    MAJOR_ARCANA = [
        "THE_FOOL",
        "THE_MAGICIAN",
        "THE_HIGH_PRIESTESS",
        "THE_EMPRESS",
        "THE_EMPEROR",
        "THE_HIEROPHANT",
        "THE_LOVERS",
        "THE_CHARIOT",
        "STRENGTH",
        "THE_HERMIT",
        "WHEEL_OF_FORTUNE",
        "JUSTICE",
        "THE_HANGED_MAN",
        "DEATH",
        "TEMPERANCE",
        "THE_DEVIL",
        "THE_TOWER",
        "THE_STAR",
        "THE_MOON",
        "THE_SUN",
        "JUDGEMENT",
        "THE_WORLD",
    ]
    MINOR_ARCANA = [
        "WANDS_ACE",
        "WANDS_TWO",
        "WANDS_THREE",
        "WANDS_FOUR",
        "WANDS_FIVE",
        "WANDS_SIX",
        "WANDS_SEVEN",
        "WANDS_EIGHT",
        "WANDS_NINE",
        "WANDS_TEN",
        "WANDS_PAGE",
        "WANDS_KNIGHT",
        "WANDS_QUEEN",
        "WANDS_KING",
        "CUPS_ACE",
        "CUPS_TWO",
        "CUPS_THREE",
        "CUPS_FOUR",
        "CUPS_FIVE",
        "CUPS_SIX",
        "CUPS_SEVEN",
        "CUPS_EIGHT",
        "CUPS_NINE",
        "CUPS_TEN",
        "CUPS_PAGE",
        "CUPS_KNIGHT",
        "CUPS_QUEEN",
        "CUPS_KING",
        "SWORDS_ACE",
        "SWORDS_TWO",
        "SWORDS_THREE",
        "SWORDS_FOUR",
        "SWORDS_FIVE",
        "SWORDS_SIX",
        "SWORDS_SEVEN",
        "SWORDS_EIGHT",
        "SWORDS_NINE",
        "SWORDS_TEN",
        "SWORDS_PAGE",
        "SWORDS_KNIGHT",
        "SWORDS_QUEEN",
        "SWORDS_KING",
        "PENTACLES_ACE",
        "PENTACLES_TWO",
        "PENTACLES_THREE",
        "PENTACLES_FOUR",
        "PENTACLES_FIVE",
        "PENTACLES_SIX",
        "PENTACLES_SEVEN",
        "PENTACLES_EIGHT",
        "PENTACLES_NINE",
        "PENTACLES_TEN",
        "PENTACLES_PAGE",
        "PENTACLES_KNIGHT",
        "PENTACLES_QUEEN",
        "PENTACLES_KING",
    ]
