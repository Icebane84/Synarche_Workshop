import asyncio

from src.agents.axion.oathkeeper import AxionOathkeeper


async def test():
    try:
        AxionOathkeeper()
        print("SUCCESS: Oathkeeper graph compiled.")
    except Exception as e:
        print(f"FAILURE: {e}")


if __name__ == "__main__":
    asyncio.run(test())
