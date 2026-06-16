import asyncio
import os
import sys

from loguru import logger

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from open_notebook.domain.notebook import Source


async def main() -> None:
    source_id = "source:r1dq2azokwta7tdnl85r"
    try:
        source = await Source.get(source_id)
        if not source:
            return


        if source.full_text:
        else:
            pass

    except Exception as e:
        pass


if __name__ == "__main__":
    asyncio.run(main())
