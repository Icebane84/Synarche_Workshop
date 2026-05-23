import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from logic.memory.memory_system import MemorySystem


def verify() -> None:
    print("[*] Initializing MemorySystem...")
    ms = MemorySystem()

    print("[*] Adding test memory (L2)...")
    mid = ms.add_memory("Phase 28 Verification Entry", domain="Test", layer=2)
    print(f"[+] Memory added with ID: {mid}")

    print("[*] Retrieving by layer...")
    layer_entries = ms.retrieve_by_layer(2)
    found = any(e["id"] == mid for e in layer_entries)
    print(f"[+] Found in L2: {found}")

    print("[*] Testing Gemify (L1 elevation)...")
    success = ms.gemify(mid, "Verification Insight", importance=1.0)
    print(f"[+] Gemify success: {success}")

    print("[*] Retrieving entry details after gemify...")
    conn = ms.conn
    row = conn.execute("SELECT * FROM memory_entries WHERE id = ?", (mid,)).fetchone()
    if row:
        row_dict = dict(row)
        print(
            f"[DEBUG] Memory Entry {mid}: layer={row_dict.get('memory_layer')}, state={row_dict.get('state')}"
        )
    else:
        print(f"[DEBUG] Memory Entry {mid} NOT FOUND in database!")

    print("[*] Verifying L1 status via retrieve_by_layer...")
    l1_entries = ms.retrieve_by_layer(1)
    print(f"[DEBUG] Total L1 entries: {len(l1_entries)}")
    for e in l1_entries:
        print(f"  - L1 Entry: id={e['id']}, content={e['content'][:20]}")

    l1_found = any(e["id"] == mid for e in l1_entries)
    print(f"[+] Found in L1: {l1_found}")

    if found and l1_found:
        print("[SUCCESS] Phase 28 Memory Substrate Verified.")
    else:
        print("[FAILURE] Verification failed.")


if __name__ == "__main__":
    verify()
