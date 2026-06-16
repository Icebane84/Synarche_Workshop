"""| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `TOOL-TOOL-ROUTER-001`                | The Sovereign ID. |
| **Official Name** | `tool_router.py`                   | The Filename.     |
| **Version**       | **v13.1**                      | The Standard.     |
| **Domain**        | `GVRN`                         | The Subject.      |
| **Evolution**     | **Autonomous Vigil**           | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[PLANET]`                    | The Tier.         |
| **Relations**     | `GOVERNED_BY: CORE-CODEX-001`  | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-02-23`                       | Creation Date.    |.
"""

import logging
import os
import re
import sys
from collections.abc import Callable
from typing import Any

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolRouter")

# Dynamic Path Setup for Local Import Resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    # Attempt to import assuming we are in the axion-core package context
    from src.logic.enums import (
        FIELD_GOVERNANCE,
        ArtifactType,
        AuditStatus,
        CelestialClass,
        Domain,
        Evolution,
        Module,
        Signal,
        Status,
        TarotShard,
        get_patron,
    )
except ImportError:
    # Fallback: Try absolute import if the package is installed in the environment
    try:
        from forge.enums import (
            FIELD_GOVERNANCE,
            ArtifactType,
            AuditStatus,
            CelestialClass,
            Domain,
            Evolution,
            Module,
            Signal,
            Status,
            TarotShard,
            get_patron,
        )
    except ImportError as e:
        logger.exception(f"Critical Import Error: Could not find src.logic.enums: {e}")
        raise

# Constants
MIN_LENGTH_GENESIS = 3
MIN_LENGTH_AUTHOR = 2


class ToolRouter:
    """Routes metadata field updates to the appropriate governance logic (Tarot Shard)."""

    def __init__(self) -> None:
        # Map Shards to specific Handler Functions (Agents)
        self.council_map: dict[TarotShard, Callable[[str, str], dict[str, Any]]] = {
            TarotShard.EMPEROR: self._agent_emperor,  # Structure/Regex
            TarotShard.STAR: self._agent_star,  # Tone/Ascension
            TarotShard.PRIESTESS: self._agent_priestess,  # Graph Connectivity
            TarotShard.MAGICIAN: self._agent_magician,  # Intent/Origin
            TarotShard.KNIGHT_SWORDS: self._agent_knight,  # Mutation/Seeds
            TarotShard.KING_PENTACLES: self._agent_king,  # Time/Persistence
            TarotShard.JUDGEMENT: self._agent_judgement,  # Audit/Integrity
        }

    def route_update(self, field: str, value: str) -> dict[str, Any]:
        """Main Entry Point: Accepts a field and value, finds the Patron, and executes logic."""
        # 1. Identify Patron
        patron = get_patron(field)
        logger.info(f"🔮 Routing '{field}' to Patron: [{patron.value}]")

        # 2. Dispatch to Agent
        agent = self.council_map.get(patron)
        if agent:
            return agent(field, value)

        raise NotImplementedError(f"Agent for {patron} not active.")

    # --- Agent Stubs (The Council) ---

    def _agent_emperor(self, field: str, value: str) -> dict[str, Any]:
        """The Emperor: Strict Regex & Schema Validation."""
        try:
            if field == "Artifact ID":
                # Regex: 3+ CAPS - 3+ CAPS - 3 DIGITS (e.g., GVRN-LEX-002)
                # Updated to support v13.0 Sovereign format if needed, but sticking to legacy validation for now
                if not re.match(r"^[A-Z]{3,}-[A-Z]{3,}-\d{3}$", value):
                    return {
                        "status": "ERROR",
                        "governor": "EMPEROR",
                        "msg": f"Invalid ID Format: {value}",
                    }

            elif field == "Version":
                # Regex: v + Digits + . + Digits (e.g., v13.0)
                if not re.match(r"^v\d+\.\d+$", value):
                    return {
                        "status": "ERROR",
                        "governor": "EMPEROR",
                        "msg": f"Invalid Version Format: {value}",
                    }

            elif field == "Type":
                if value not in ArtifactType.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "EMPEROR",
                        "msg": f"Invalid Type: {value}",
                    }

            elif field == "Status" and value not in Status.__members__:
                return {
                    "status": "ERROR",
                    "governor": "EMPEROR",
                    "msg": f"Invalid Status: {value}",
                }

            return {
                "status": "VALIDATED",
                "governor": "EMPEROR",
                "field": field,
                "value": value,
                "note": "Schema compliant.",
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "governor": "EMPEROR", "msg": str(e)}

    def _agent_star(self, field: str, value: str) -> dict[str, Any]:
        """The Star: Tone Analysis & Ascension Alignment."""
        try:
            if field == "Signal":
                # Check against values (e.g. ESF-OMEGA) and keys (OMEGA)
                valid_values = [e.value for e in Signal]
                if value not in valid_values and value not in Signal.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "STAR",
                        "msg": f"Invalid Signal: {value}",
                    }

            elif field == "Evolution":
                valid_values = [e.value for e in Evolution]
                if value not in valid_values and value not in Evolution.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "STAR",
                        "msg": f"Invalid Evolution: {value}",
                    }

            return {
                "status": "VALIDATED",
                "governor": "STAR",
                "field": field,
                "value": value,
                "note": "Resonance check passed.",
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "governor": "STAR", "msg": str(e)}

    def _agent_priestess(self, field: str, value: str) -> dict[str, Any]:
        """The High Priestess: Graph Connectivity & Domain Checks."""
        try:
            if field == "Domain":
                if value not in Domain.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "PRIESTESS",
                        "msg": f"Invalid Domain: {value}",
                    }

            elif field == "Celestial Class":
                if value not in CelestialClass.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "PRIESTESS",
                        "msg": f"Invalid Celestial Class: {value}",
                    }

            return {
                "status": "VALIDATED",
                "governor": "PRIESTESS",
                "field": field,
                "value": value,
                "note": "Synergy link verified.",
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "governor": "PRIESTESS", "msg": str(e)}

    def _agent_magician(self, field: str, value: str) -> dict[str, Any]:
        """The Magician: Intent & Catalyst Verification."""
        try:
            if field == "Module":
                if value not in Module.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "MAGICIAN",
                        "msg": f"Invalid Module: {value}",
                    }

            elif field in ["Catalyst", "Nova Spark"]:
                if (
                    not isinstance(value, str)
                    or len(value.strip()) <= MIN_LENGTH_GENESIS
                ):
                    return {
                        "status": "ERROR",
                        "governor": "MAGICIAN",
                        "msg": f"{field} too short or empty.",
                    }

            return {
                "status": "VALIDATED",
                "governor": "MAGICIAN",
                "field": field,
                "value": value,
                "note": "Spark recognized & Validated.",
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "governor": "MAGICIAN", "msg": str(e)}

    def _agent_knight(self, field: str, value: str) -> dict[str, Any]:
        """The Knight of Swords: Genesis Seeds & Mutation."""
        try:
            if field == "Genesis Seed":
                if (
                    not isinstance(value, str)
                    or len(value.strip()) <= MIN_LENGTH_GENESIS
                ):
                    return {
                        "status": "ERROR",
                        "governor": "KNIGHT_SWORDS",
                        "msg": "Genesis Seed too short.",
                    }

            return {
                "status": "VALIDATED",
                "governor": "KNIGHT_SWORDS",
                "field": field,
                "value": value,
                "note": "Actionable seed verified.",
            }
        except Exception as e:
            return {
                "status": "CRITICAL_ERROR",
                "governor": "KNIGHT_SWORDS",
                "msg": str(e),
            }

    def _agent_king(self, field: str, value: str) -> dict[str, Any]:
        """The King of Pentacles: Timestamp & Archival."""
        try:
            if field == "Created":
                # ISO-8601 strictness: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ (optional Z or offset)
                if not re.match(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}Z?)?$", value):
                    return {
                        "status": "ERROR",
                        "governor": "KING_PENTACLES",
                        "msg": f"Invalid Timestamp: {value}",
                    }

            return {
                "status": "VALIDATED",
                "governor": "KING_PENTACLES",
                "field": field,
                "value": value,
                "note": "Timestamp anchor verified.",
            }
        except Exception as e:
            return {
                "status": "CRITICAL_ERROR",
                "governor": "KING_PENTACLES",
                "msg": str(e),
            }

    def _agent_judgement(self, field: str, value: str) -> dict[str, Any]:
        """Judgement: Integrity Hash & Audit."""
        try:
            if field == "Integrity Hash":
                # Allow the placeholder OR a real sha256 hex
                if value != "[AUTO-GEN-SHA256]" and not re.match(
                    r"^sha256:[a-f0-9]{64}$", value
                ):
                    return {
                        "status": "ERROR",
                        "governor": "JUDGEMENT",
                        "msg": f"Invalid Hash Format: {value}",
                    }

            elif field == "Musashi Audit":
                if value not in AuditStatus.__members__:
                    return {
                        "status": "ERROR",
                        "governor": "JUDGEMENT",
                        "msg": f"Invalid Audit Status: {value}",
                    }

            elif field == "Author":
                if not isinstance(value, str) or len(value) < MIN_LENGTH_AUTHOR:
                    return {
                        "status": "ERROR",
                        "governor": "JUDGEMENT",
                        "msg": "Author name too short.",
                    }

            return {
                "status": "VALIDATED",
                "governor": "JUDGEMENT",
                "field": field,
                "value": value,
                "note": "Integrity seal verified.",
            }
        except Exception as e:
            return {"status": "CRITICAL_ERROR", "governor": "JUDGEMENT", "msg": str(e)}


if __name__ == "__main__":
    # Simple CLI test
    router = ToolRouter()
    if len(sys.argv) > 2:
        res = router.route_update(sys.argv[1], sys.argv[2])
        print(res)
    else:
        print("Usage: python tool_router.py [Field] [Value]")
