"""## **[ARTIFACT START]**.

## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.experience.logger`                | The Sovereign ID. |
| **Official Name** | `experience_logger.py`                   | The Filename.     |
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
# | **Data Corruption**  | Atomic SQLite Transactions |
# | **Storage Drift**    | Standardized JSONL Format |

# ---

### **Block D: Standardized Synergy Block (The Loom Signature)**

# | Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
# | :---------------------- | :---------------- | :---------------------------------------------- |
| CORE.Codex.Phoenix    | GOVERNS         | Provides the supreme law and ethical framework. |

## **[ARTIFACT END]**

Logs agent experiences for L1-L5 memory processing and analysis.
Conforms to OGLN/AISTF v15.0 documentation and compliance standards.
"""

import datetime
import json
import logging
import os
import sqlite3
import sys
from typing import Any, Dict, Optional

# Configure logging for the experience logger
log = logging.getLogger(__name__)

if not log.handlers:
    log.addHandler(logging.StreamHandler(sys.stderr))
    log.setLevel(logging.INFO)


class ExperienceLogger:
    """Logs agent experiences for L1-L5 memory processing and analysis.
    Supports both JSONL flat-file logging and SQLite relational logging.
    """

    def __init__(
        self,
        log_file_path: str = "gemini_gem_experience_log.jsonl",
        db_path: Optional[str] = None,
    ) -> None:
        """Initializes the ExperienceLogger.

        Args:
            log_file_path: Path to the JSONL log file.
            db_path: Path to the SQLite database file (optional).

        """
        self.log_file: str = log_file_path
        self.db_path: Optional[str] = db_path
        self._last_log_entry: Optional[Dict[str, Any]] = None
        self._ensure_log_dir_exists()
        if self.db_path:
            self._ensure_db_exists()
        log.info(f"ExperienceLogger initialized. Logging to '{self.log_file}'")

    def _ensure_log_dir_exists(self) -> None:
        """Ensures that the directory for the JSONL log file exists."""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _ensure_db_exists(self) -> None:
        """Ensures that the directory for the SQLite database exists
        and initializes the schema if it does not exist.
        """
        if not self.db_path:
            return
        log_dir = os.path.dirname(self.db_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS experience_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    pair_num INTEGER,
                    timestamp TEXT,
                    user_intent TEXT,
                    user_emotion TEXT,
                    agent_intent TEXT,
                    agent_tone TEXT,
                    memories_used TEXT,
                    inferences TEXT,
                    full_log TEXT
                );
                """)
        except sqlite3.Error as e:
            log.error(f"SQLite setup error: {e}")

    def log_interaction_pair(self, interaction_data: Dict[str, Any]) -> None:
        """Logs a single interaction pair (User Turn + Agent Response) to JSONL and optional SQLite.

        Args:
            interaction_data: Dictionary containing the interaction details.

        """
        if not isinstance(interaction_data, dict):
            return
        try:
            if "log_timestamp" not in interaction_data:
                interaction_data["log_timestamp"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()
            self._last_log_entry = interaction_data.copy()
            log_line = json.dumps(interaction_data, default=str)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
            if self.db_path:
                self._log_to_sqlite(interaction_data, log_line)
        except Exception as e:
            log.error(f"Interaction logging failed: {e}")

    def _log_to_sqlite(
        self, interaction_data: Dict[str, Any], full_log_json: str
    ) -> None:
        """Parses interaction data and inserts it into the SQLite experience_logs table.

        Args:
            interaction_data: The dictionary of interaction metadata.
            full_log_json: The complete interaction serialized as a JSON string.

        """
        if not self.db_path:
            return
        try:
            session_id = interaction_data.get("Session ID", "unknown")
            pair_num = interaction_data.get("Interaction Pair #", 0)
            timestamp = interaction_data.get("log_timestamp", "")
            user_turn = interaction_data.get("User Turn", {})
            user_analysis = (
                user_turn.get("Analysis", {}) if isinstance(user_turn, dict) else {}
            )
            agent_response = interaction_data.get("Agent Response", {})
            agent_reasoning = (
                agent_response.get("Analysis & Reasoning", {})
                if isinstance(agent_response, dict)
                else {}
            )

            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO experience_logs (
                        session_id, pair_num, timestamp, user_intent, user_emotion,
                        agent_intent, agent_tone, memories_used, inferences, full_log
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        session_id,
                        pair_num,
                        timestamp,
                        user_analysis.get("Inferred User Intent", "unknown"),
                        user_analysis.get("Emotion/Tone", "unknown"),
                        agent_reasoning.get("Agent Intent", "unknown"),
                        agent_reasoning.get("Projected Tone", "unknown"),
                        json.dumps(agent_reasoning.get("Key Memories Used", [])),
                        json.dumps(agent_reasoning.get("Inferences Made", [])),
                        full_log_json,
                    ),
                )
        except sqlite3.Error as e:
            log.error(f"SQLite logging failed: {e}")

    def get_last_log(self) -> Optional[Dict[str, Any]]:
        """Retrieves the last log entry processed by this instance.

        Returns:
            The last log entry as a dictionary, or None if no entries have been logged.

        """
        return self._last_log_entry


# ---
# [OMNI-ARTIFACT-ANCHOR] ID: CORE.experience.logger VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28
# ---
