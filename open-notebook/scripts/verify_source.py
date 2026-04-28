import asyncio
import os
import sys
from loguru import logger

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from open_notebook.domain.notebook import Source


async def main():
    source_id = "source:r1dq2azokwta7tdnl85r"
    try:
        source = await Source.get(source_id)
        if not source:
            print(f"Source {source_id} not found")
            return

        print(f"ID: {source.id}")
        print(f"Title: {source.title}")
        print(f"Text length: {len(source.full_text) if source.full_text else 0}")
        print(f"Asset: {source.asset}")

        if source.full_text:
            print("\nFirst 100 chars of text:")
            print(source.full_text[:100])
        else:
            print("\nFULL TEXT IS EMPTY")

    except Exception as e:
        print(f"Failed to fetch source: {e}")


if __name__ == "__main__":
    asyncio.run(main())
