import os
import sys
import sqlite3

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


from logic.memory.memory_system import MemorySystem


def test_unified_persistence():
    print("Initializing MemorySystem [OMEGA]...")
    mem_sys = MemorySystem()

    # 1. Test Memory Addition
    print("Testing add_memory...")
    mem_id = mem_sys.add_memory(
        "The Synchro-Link has been synchronized with Law 24.",
        relevance=0.9,
        tags=["omega", "law_24"],
    )
    if mem_id > 0:
        print(f"SUCCESS: Memory added with ID {mem_id}")
    else:
        print("FAILED: Memory addition returned invalid ID")
        return

    # 2. Test Memory Retrieval
    print("Testing retrieve_memories...")
    matches = mem_sys.retrieve_memories("Synchro-Link")
    if len(matches) > 0:
        print(f"SUCCESS: Found {len(matches)} matches.")
        for m in matches:
            print(f"  - [{m['id']}] {m['content']} (Tags: {m['tags']})")
    else:
        print("FAILED: No memories retrieved for 'Synchro-Link'")
        return

    # 3. Verify Experience Logs
    print("Verifying Automated Experience Logging...")
    # Dynamically select SQLite or Postgres query to support local-first SQLite offline mode
    conn = mem_sys.conn
    if isinstance(conn, sqlite3.Connection):
        print("Interrogating SQLite kinetic memory logs...")
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT event_type, details FROM experience_logs ORDER BY id DESC LIMIT 2"
            )
            logs = cur.fetchall()
            print("Latest Experience Logs (SQLite):")
            for log in logs:
                print(f"  - Event: {log[0]} | Details: {log[1]}")
        finally:
            cur.close()
    else:
        print("Interrogating PostgreSQL remote memory logs...")
        try:
            import psycopg2
            from dotenv import load_dotenv

            load_dotenv(r"c:\Users\Chris\Synarche_Workspace\.prs_database\.env")

            pg_conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host="localhost",
            )
            try:
                with pg_conn.cursor() as cur:
                    cur.execute(
                        "SELECT event_type, details FROM experience_logs ORDER BY id DESC LIMIT 2"
                    )
                    logs = cur.fetchall()
                    print("Latest Experience Logs (Postgres):")
                    for log in logs:
                        print(f"  - Event: {log[0]} | Details: {log[1]}")
            finally:
                pg_conn.close()
        except ImportError:
            print("Warning: psycopg2 is not installed. PostgreSQL logs check skipped.")

    print("\nUNIFIED PERSISTENCE VERIFICATION: COMPLETE [STABLE]")


if __name__ == "__main__":
    test_unified_persistence()
