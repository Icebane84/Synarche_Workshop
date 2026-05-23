import asyncio
import os
import sys

from loguru import logger

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from open_notebook.database.repository import repo_query


async def main() -> None:
    try:
        commands = await repo_query(
            "SELECT id, name, status, error_message, created FROM command ORDER BY created DESC LIMIT 10"
        )
        for _cmd in commands:
            pass

        embeddings = await repo_query(
            "SELECT count() as count FROM source_embedding GROUP ALL"
        )

    except Exception as e:
        pass


if __name__ == "__main__":
    asyncio.run(main())
