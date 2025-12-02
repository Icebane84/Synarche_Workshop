import logging
import os
import sqlite3
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json

# Configuration
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Resolve Workspace Root
WORKSPACE_ROOT = os.getenv("AXION_WORKSPACE_ROOT")
if not WORKSPACE_ROOT:
    # Marker file traversal: Start from this script's parent (scripts/)
    current = Path(__file__).resolve().parent
    # root is two levels up from scripts/
    WORKSPACE_ROOT = current.parent.parent
else:
    WORKSPACE_ROOT = Path(WORKSPACE_ROOT)

SQLITE_DB = WORKSPACE_ROOT / "axion-core" / "data" / "GVRN.Log.Experience.db"
DOTENV_PATH = WORKSPACE_ROOT / ".prs_database" / ".env"

logger.info(f"Resolved WORKSPACE_ROOT: {WORKSPACE_ROOT}")
logger.info(f"Targeting SQLite DB: {SQLITE_DB}")
logger.info(f"Using .env from: {DOTENV_PATH}")

load_dotenv(str(DOTENV_PATH))


def migrate() -> None:
    logger.info(f"Starting migration from {SQLITE_DB} to PostgreSQL...")

    if not SQLITE_DB.exists():
        logger.error(f"SQLite database file not found at: {SQLITE_DB}")
        return

    user = os.getenv("POSTGRES_USER")
    db = os.getenv("POSTGRES_DB")
    password = os.getenv("POSTGRES_PASSWORD")

    if not all([user, db, password]):
        logger.error("Database credentials missing from .env")
        return

    try:
        sl_conn = sqlite3.connect(str(SQLITE_DB))
        sl_cursor = sl_conn.cursor()
        logger.info("Connected to SQLite successful.")
    except Exception as e:
        logger.error(f"Error connecting to SQLite: {e}")
        return

    try:
        pg_conn = psycopg2.connect(dbname=db, user=user, password=password, host="localhost", port="5432")
        pg_cursor = pg_conn.cursor()
        logger.info("Connected to PostgreSQL successful.")
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        sl_conn.close()
        return

    try:
        sl_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experience_logs'")
        if not sl_cursor.fetchone():
            logger.error("Table 'experience_logs' not found in SQLite.")
            return

        sl_cursor.execute(
            "SELECT log_timestamp, session_id, user_intent, agent_intent, full_log_data FROM experience_logs"
        )
        rows = sl_cursor.fetchall()
        logger.info(f"Found {len(rows)} records in SQLite.")

        if not rows:
            logger.info("No records to migrate.")
            return

        insert_query = """
            INSERT INTO experience_logs (timestamp, event_type, module, details, coherence_impact)
            VALUES (%s, %s, %s, %s, %s)
        """

        migrated_count = 0
        for row in rows:
            log_timestamp, session_id, user_intent, agent_intent, full_log_data = row
            details_json = {
                "session_id": session_id,
                "user_intent": user_intent,
                "agent_intent": agent_intent,
                "full_log_data": full_log_data,
            }
            pg_cursor.execute(insert_query, (log_timestamp, "INTERACTION", "AXION_PRIME", Json(details_json), 0.1))
            migrated_count += 1

        pg_conn.commit()
        logger.info(f"Successfully migrated {migrated_count} records.")

    except Exception as e:
        logger.error(f"An error occurred during migration: {e}")
        pg_conn.rollback()
    finally:
        sl_conn.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
