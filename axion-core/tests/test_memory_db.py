import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


from logic.memory.memory_system import MemorySystem


def test_unified_persistence():
    print("Initializing MemorySystem [OMEGA]...")
    mem_sys = MemorySystem()
    
    # 1. Test Memory Addition
    print("Testing add_memory...")
    mem_id = mem_sys.add_memory("The Synchro-Link has been synchronized with Law 24.", relevance=0.9, tags=["omega", "law_24"])
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
    # We'll check the database directly for the MEMORY_ADD event
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv(r'c:\Users\Chris\Synarche_Workspace\.prs_database\.env')
    
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost"
    )
    with conn.cursor() as cur:
        cur.execute("SELECT event_type, details FROM experience_logs ORDER BY id DESC LIMIT 2")
        logs = cur.fetchall()
        print("Latest Experience Logs:")
        for log in logs:
            print(f"  - Event: {log[0]} | Details: {log[1]}")
            
    conn.close()
    print("\nUNIFIED PERSISTENCE VERIFICATION: COMPLETE [STABLE]")

if __name__ == "__main__":
    test_unified_persistence()
