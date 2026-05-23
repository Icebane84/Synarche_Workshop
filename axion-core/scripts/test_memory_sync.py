import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from logic.memory.memory_system import MemorySystem


async def test_sync():
    print("--- 🧠 Sovereign Sync Test ---")

    # Initialize system
    ms = MemorySystem()
    print(f"Memory System using storage: {type(ms.storage).__name__}")

    # Log a high-impact event
    event_type = "SYNERGY_FOUND"
    module = "TestForge"
    details = {
        "insight": "The Unified Memory Layer has achieved 100% resonance.",
        "impact": 0.9,
    }

    print(f"Syncing event: {event_type}...")
    ms._sync_to_sovereign(event_type, module, details)

    # Check the file
    target = ms.sovereign_memory_path
    if target.exists():
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
        if "### [" in content and "SYNERGY_FOUND" in content:
            print(f"SUCCESS: Event found in {target.name}")
        else:
            print(f"FAILURE: Event not found in {target.name}")
    else:
        print(f"FAILURE: Target file {target} does not exist.")


if __name__ == "__main__":
    asyncio.run(test_sync())
