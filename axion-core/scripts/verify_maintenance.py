import asyncio
import logging
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from logic.memory.memory_system import MemorySystem


async def verify_maintenance() -> None:
    logging.basicConfig(level=logging.INFO)
    print("--- Memory Maintenance & Transition Audit ---")

    mem_sys = MemorySystem()
    if mem_sys.storage is None:
        print("\nFAILURE: Memory storage not initialized.")
        return

    # 1. Create a "Consolidatable" Memory
    # Requirements for L2 -> L3 transition:
    # - Activation > 0.8
    # - Usage > 10
    print("\n1. Creating high-usage L2 memory...")
    content = "The OMEGA-15 synchronization protocol is stable."
    mem_id = mem_sys.add_memory(
        content=content, domain="Systems", relevance=1.0, layer=2
    )

    # Manually boost to meet thresholds for testing
    print(f"   Boosting memory {mem_id} to meet consolidation thresholds...")
    mem_sys.storage.update_memory(mem_id, {"activation_score": 0.95, "usage_count": 15})

    # 2. Run Maintenance Cycle
    print("\n2. Running Maintenance Cycle...")
    transitions = mem_sys.maintenance_cycle()
    print(f"   Cycle Complete. Transitions reported: {transitions}")

    # 3. Verify L3 Transition
    print("\n3. Verifying Layer Ascension...")
    results = mem_sys.storage.retrieve_memories("OMEGA-15", limit=1)
    if results:
        m = results[0]
        print(f"Memory [{m['id']}] status:")
        print(f"   - Current Layer: L{m['memory_layer']}")
        print(f"   - State: {m['state']}")

        if m["memory_layer"] == 3:
            print("\nSUCCESS: Memory successfully ascended to L3 Semantic Layer.")
        else:
            print("\nFAILURE: Memory failed to transition to L3.")
    else:
        print("\nFAILURE: Memory not found.")

    print("\n--- Audit Complete ---")


if __name__ == "__main__":
    asyncio.run(verify_maintenance())
