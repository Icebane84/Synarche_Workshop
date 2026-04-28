import asyncio
import os
import sys
from loguru import logger

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api.client import api_client


async def main():
    notebook_id = "notebook:hhgjek28qxr88o34ohut"
    bible_path = r"C:\Users\Chris\Synarche_Workspace\where-light-fades\Where Light Fades_ The Definitive Content Bible.md"

    if not os.path.exists(bible_path):
        logger.error(f"File not found: {bible_path}")
        return

    logger.info(f"Ingesting: {bible_path}")

    try:
        response = api_client.create_source(
            notebook_id=notebook_id,
            source_type="upload",
            file_path=bible_path,
            title="Where Light Fades: The Definitive Content Bible",
            embed=True,
            async_processing=True,
        )
        logger.info(f"Ingestion triggered. Response: {response}")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
