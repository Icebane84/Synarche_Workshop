import asyncio
import logging
from src.agents.axion.insforge_client import insforge

logging.basicConfig(level=logging.DEBUG)

async def test():
    print("Testing InsForge Chronicler (Local Fallback)...")
    await insforge.log_event("TEST_EVENT", "Verifying the Chronicler's reach.")
    print("SUCCESS: Chronicler test complete.")

if __name__ == "__main__":
    asyncio.run(test())
