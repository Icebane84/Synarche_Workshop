"""
## **[ARTIFACT START]**
## **Block A: The Identification Lock (UIP-V15)**
| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | `CORE.experience.logger`                | The Sovereign ID. |
| **Official Name** | `experience_logger.py`                   | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE`                     | The Subject.      |
| **Status (State)**| `[CANONIZED]`                     | The Lifecycle.    |
| **Relations**     | `GOVERNED_BY: CORE.Codex.Phoenix` | The Network.      |
## **[ARTIFACT END]**
"""

import datetime
import json
import logging
import os
import sqlite3
import sys
from typing import Any

log = logging.getLogger(__name__)

if not log.handlers:
    log.addHandler(logging.StreamHandler(sys.stderr))
    log.setLevel(logging.INFO)

class ExperienceLogger:
    """Logs agent experiences for L1-L5 memory processing and analysis."""

    def __init__(self, log_file_path: str = "gemini_gem_experience_log.jsonl", db_path: str | None = None):
        self.log_file: str = log_file_path
        self.db_path: str | None = db_path
        self._last_log_entry: dict | None = None
        self._ensure_log_dir_exists()
        if self.db_path:
            self._ensure_db_exists()
        log.info(f"ExperienceLogger initialized. Logging to '{self.log_file}'")

    def _ensure_log_dir_exists(self) -> None:
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _ensure_db_exists(self) -> None:
        if not self.db_path: return
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

    def log_interaction_pair(self, interaction_data: dict[str, Any]) -> None:
        if not isinstance(interaction_data, dict): return
        try:
            if "log_timestamp" not in interaction_data:
                interaction_data["log_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            self._last_log_entry = interaction_data.copy()
            log_line = json.dumps(interaction_data, default=str)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
            if self.db_path:
                self._log_to_sqlite(interaction_data, log_line)
        except Exception as e:
            log.error(f"Interaction logging failed: {e}")

    def _log_to_sqlite(self, interaction_data: dict[str, Any], full_log_json: str) -> None:
        if not self.db_path: return
        try:
            session_id = interaction_data.get("Session ID", "unknown")
            pair_num = interaction_data.get("Interaction Pair #", 0)
            timestamp = interaction_data.get("log_timestamp", "")
            user_turn = interaction_data.get("User Turn", {})
            user_analysis = user_turn.get("Analysis", {}) if isinstance(user_turn, dict) else {}
            agent_response = interaction_data.get("Agent Response", {})
            agent_reasoning = agent_response.get("Analysis & Reasoning", {}) if isinstance(agent_response, dict) else {}
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO experience_logs (
                        session_id, pair_num, timestamp, user_intent, user_emotion,
                        agent_intent, agent_tone, memories_used, inferences, full_log
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, pair_num, timestamp,
                    user_analysis.get("Inferred User Intent", "unknown"),
                    user_analysis.get("Emotion/Tone", "unknown"),
                    agent_reasoning.get("Agent Intent", "unknown"),
                    agent_reasoning.get("Projected Tone", "unknown"),
                    json.dumps(agent_reasoning.get("Key Memories Used", [])),
                    json.dumps(agent_reasoning.get("Inferences Made", [])),
                    full_log_json
                ))
        except sqlite3.Error as e:
            log.error(f"SQLite logging failed: {e}")

    def get_last_log(self) -> dict[str, Any] | None:
        return self._last_log_entry

# [OMNI-ARTIFACT-ANCHOR] ID: CORE.experience.logger VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 432cdc264f30fdd7
