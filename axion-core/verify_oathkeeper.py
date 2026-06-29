from src.agents.axion.oathkeeper import AxionOathkeeper
import asyncio

async def test():
    try:
        agent = AxionOathkeeper()
        print("SUCCESS: Oathkeeper graph compiled.")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(test())
