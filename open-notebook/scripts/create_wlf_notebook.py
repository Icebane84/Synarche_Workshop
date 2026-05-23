import asyncio
import os
import sys

from loguru import logger

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from open_notebook.database.repository import repo_query
from open_notebook.domain.notebook import Notebook


async def main() -> None:
    logger.info("Connecting to SurrealDB...")

    # Check if notebook already exists
    existing = await repo_query(
        "SELECT * FROM notebook WHERE name = 'Where Light Fades'"
    )
    if existing:
        logger.info(
            f"Notebook 'Where Light Fades' already exists with ID: {existing[0]['id']}"
        )
        return

    logger.info("Creating 'Where Light Fades' notebook...")
    nb = Notebook(
        name="Where Light Fades",
        description="Core notebook for the 'Where Light Fades' story project and Obsidian vault.",
    )
    await nb.save()
    logger.info(f"Created notebook: {nb.name} (ID: {nb.id})")


if __name__ == "__main__":
    asyncio.run(main())
