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

---

## **Block B: State Vector (AGP-001)**

| State Field   | Value     |
| :------------ | :-------- |
| **Coherence** | `{resonance}`     |
| **Resonance** | `{resonance}`     |
| **Stability** | `Stable`  |

---

### **Block C: Risk & Mitigation (AGP-002)**

| Risk                 | Mitigation                |
| :------------------- | :------------------------ |
| **Logic Drift**      | Strict Linter Enforcement |
| **Semantic Decay**   | Axiomatic Compass Audit   |

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

| Synergistic Artifact ID | Relationship Type | Synergistic Impact                              |
| :---------------------- | :---------------- | :---------------------------------------------- |
| `CORE.Codex.Phoenix`    | `GOVERNS`         | Provides the supreme law and ethical framework. |

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
        """
        Initializes the ExperienceLogger (v15.0 [OMEGA]).
        Anchors telemetry to both JSONL and SQLite for sovereign persistence.

        Args:
            log_file_path: Path for the sequential JSONL telemetry stream.
            db_path: Path for the structured SQLite sovereign archive.
        """
        self.log_file: str = log_file_path
        self.db_path: str | None = db_path
        self._ensure_log_dir_exists()

        if self.db_path:
            self._ensure_db_exists()

        self._last_log_entry: dict | None = None

        log.info(f"ExperienceLogger initialized. Logging to '{self.log_file}' and DB '{self.db_path}'")

    def _ensure_log_dir_exists(self) -> None:
        """Ensures the directory for the log file exists."""
        try:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
                log.info(f"Created log directory: {log_dir}")
        except Exception as e:
            log.error(f"Failed to create log directory for '{self.log_file}'. Error: {e}", exc_info=True)
            print(
                f"ERROR [ExperienceLogger]: Could not create log directory '{os.path.dirname(self.log_file)}'. Logging might fail.",
                file=sys.stderr,
            )

    def _ensure_db_exists(self) -> None:
        """Creates the SQLite log table if it doesn't exist (Axion Gold Standard)."""
        if not self.db_path:
            return

        log_dir = os.path.dirname(self.db_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
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
            conn.commit()
        except sqlite3.Error as e:
            log.error(f"SQLite setup error: {e}", exc_info=True)
        finally:
            if conn:
                conn.close()

    def log_interaction_pair(self, interaction_data: dict[str, Any]) -> None:
        """Logs an interaction pair to JSONL and SQLite (Dual Sovereign)."""
        if not isinstance(interaction_data, dict):
            return
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
            log.error(f"Interaction logging failed: {e}", exc_info=True)

    def _log_to_sqlite(self, interaction_data: dict[str, Any], full_log_json: str) -> None:
        """Helper to write the interaction data into the SQLite database with extracted metadata."""
        conn = None
        try:
            session_id = interaction_data.get("Session ID", "unknown")
            pair_num = interaction_data.get("Interaction Pair #", 0)
            timestamp = interaction_data.get("log_timestamp", "")

            # Extract User Analysis
            user_turn = interaction_data.get("User Turn", {})
            user_analysis = user_turn.get("Analysis", {}) if isinstance(user_turn, dict) else {}
            user_intent = user_analysis.get("Inferred User Intent", "unknown")
            user_emotion = user_analysis.get("Emotion/Tone", "unknown")

            # Extract Agent Reasoning
            agent_response = interaction_data.get("Agent Response", {})
            agent_reasoning = agent_response.get("Analysis & Reasoning", {}) if isinstance(agent_response, dict) else {}
            agent_intent = agent_reasoning.get("Agent Intent", "unknown")
            agent_tone = agent_reasoning.get("Projected Tone", "unknown")

            # Extract Memories & Inferences
            memories = agent_reasoning.get("Key Memories Used", [])
            inferences = agent_reasoning.get("Inferences Made", [])

            if not self.db_path:
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
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
                    user_intent,
                    user_emotion,
                    agent_intent,
                    agent_tone,
                    json.dumps(memories),
                    json.dumps(inferences),
                    full_log_json,
                ),
            )
            conn.commit()
        except sqlite3.Error as e:
            log.error(f"SQLite logging failed: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def get_last_log(self) -> dict[str, Any] | None:
        """Retrieves the last recorded log entry."""
        return self._last_log_entry

# ---
# 
# ---

### **Block G: The Omni-Anchor (System Snapshot)**

`[OMNI-ARTIFACT-ANCHOR] ID: CORE.experience.logger VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [CANONIZED] TS: 2026-03-28 HASH: 432cdc264f30fdd7`
