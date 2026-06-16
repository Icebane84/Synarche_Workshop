import asyncio
import logging
import os
import sys

# Add src to path
# The directory structure is axion-core/src/logic/memory/memory_system.py
# If we run from axion-core/, then src is in the current dir.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from logic.memory.memory_system import MemorySystem


async def verify_memory():
    logging.basicConfig(level=logging.INFO)
    print("--- 🧠 Memory System Functional Audit ---")

    # 1. Initialization
    try:
        mem_sys = MemorySystem()
        print(
            f"SUCCESS: MemorySystem initialized using {type(mem_sys.storage).__name__}"
        )
    except Exception as e:
        print(f"FAILURE: MemorySystem initialization failed: {e}")
        return

    # 2. End-to-End Test (Add + Tag + Store)
    content = "The shadow self found a lost inner flame amidst the battle of Valerius."
    print(f"\nAdding memory: '{content}'")
    try:
        # This will trigger Tagger (NLP) and EmotionAnalyzer
        mem_id = mem_sys.add_memory(
            content=content, domain="Mythology", relevance=0.8, tags=["test", "audit"]
        )
        if mem_id > 0:
            print(f"SUCCESS: Memory added with ID {mem_id}")
        else:
            print("FAILURE: Memory addition returned invalid ID")
    except Exception as e:
        print(f"FAILURE: Error during add_memory: {e}")

    # 3. Retrieval & NLP Verification
    print("\nRetrieving memory and checking tags...")
    try:
        results = mem_sys.retrieve_memories("shadow self")
        if results:
            m = results[0]
            print(f"SUCCESS: Found memory [{m['id']}]")
            print(f"  - Tags: {m['tags']}")
            print(f"  - Layer: {m['memory_layer']}")
            print(f"  - Activation: {m['activation_score']}")
        else:
            print("FAILURE: No memories retrieved for 'shadow self'")
    except Exception as e:
        print(f"FAILURE: Error during retrieval: {e}")

    print("\n--- Audit Complete ---")


if __name__ == "__main__":
    asyncio.run(verify_memory())
