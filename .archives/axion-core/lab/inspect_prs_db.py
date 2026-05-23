"""ID: TOOL-DB-INSPECT-001
Version: v1.0
Domain: ACT
Ethos: "Vision into the Depth."
Description: PostgreSQL DB Inspector for OMEGA.
Inspects memory_entries and experience_logs.
"""

import os
import sys

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DOTENV_PATH = r"c:\Users\Chris\Synarche_Workspace\.prs_database\.env"
load_dotenv(DOTENV_PATH)


def inspect_db():
    db_name = os.getenv("POSTGRES_DB", "prs_db")
    user = os.getenv("POSTGRES_USER", "prs_user")
    password = os.getenv("POSTGRES_PASSWORD", "prs_password")
    host = "localhost"
    port = "5432"

    try:
        conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        print(f"--- CONNECTED TO {db_name} ---")

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 1. Total Counts
            cur.execute("SELECT COUNT(*) FROM memory_entries")
            res_mem = cur.fetchone()
            mem_count = res_mem["count"] if res_mem else 0

            cur.execute("SELECT COUNT(*) FROM experience_logs")
            res_exp = cur.fetchone()
            log_count = res_exp["count"] if res_exp else 0

            print(f"Memory Entries: {mem_count}")
            print(f"Experience Logs: {log_count}")

            # 2. Latest Memories
            print("\n--- LATEST 3 MEMORIES ---")
            cur.execute(
                "SELECT id, content, tags, last_retrieved FROM memory_entries ORDER BY id DESC LIMIT 3"
            )
            for row in cur.fetchall():
                print(f"[{row['id']}] {row['content'][:50]}... (Tags: {row['tags']})")

            # 3. Latest Experience Logs
            print("\n--- LATEST 3 EXPERIENCE LOGS ---")
            cur.execute(
                "SELECT id, event_type, module, coherence_impact FROM experience_logs ORDER BY id DESC LIMIT 3"
            )
            for row in cur.fetchall():
                print(
                    f"[{row['id']}] {row['event_type']} in {row['module']} (Impact: {row['coherence_impact']})"
                )

        conn.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect_db()
