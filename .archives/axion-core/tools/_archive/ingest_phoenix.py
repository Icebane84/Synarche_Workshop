"""
UWB-TOOL-INGEST-001: Phoenix Protocol Ingestor
Domain: ACT | State: ACTIVE | Version: v1.0
Objective: Batch ingest the Phoenix Protocol Library (_governance) into a dedicated Notebook.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to sys.path to access open_notebook modules
PROJECT_ROOT = Path(r"C:\Users\Chris\Synarche_Workspace\open-notebook")
INNER_PKG = PROJECT_ROOT / "open_notebook"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
if str(INNER_PKG) not in sys.path:
    sys.path.append(str(INNER_PKG))

from open_notebook.api.notebook_service import notebook_service
from open_notebook.api.sources_service import sources_service

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("PhoenixIngest")

GOVERNANCE_PATH = Path(r"C:\Users\Chris\Synarche_Workspace\_governance")
NOTEBOOK_NAME = "Phoenix Protocol Library"
NOTEBOOK_DESC = (
    "The complete repository of all Phoenix Protocol Governance artifacts, ingested for AI Contextualization."
)


def ingest_artifacts():
    logger.info("🔥 Initiating Phoenix Protocol Ingestion...")

    # 1. Check/Create Notebook
    logger.info(f"🔍 Checking for Notebook: '{NOTEBOOK_NAME}'")
    existing_notebooks = notebook_service.get_all_notebooks()
    target_notebook = next((nb for nb in existing_notebooks if nb.name == NOTEBOOK_NAME), None)

    if target_notebook:
        logger.info(f"✅ Found existing notebook: {target_notebook.id}")
    else:
        logger.info(f"✨ Creating new notebook: '{NOTEBOOK_NAME}'")
        target_notebook = notebook_service.create_notebook(name=NOTEBOOK_NAME, description=NOTEBOOK_DESC)
        logger.info(f"✅ Created notebook: {target_notebook.id}")

    # 2. Scan _governance artifacts
    if not GOVERNANCE_PATH.exists():
        logger.error(f"❌ Governance path not found: {GOVERNANCE_PATH}")
        return

    artifacts = list(GOVERNANCE_PATH.rglob("*.md"))
    logger.info(f"📚 Found {len(artifacts)} markdown artifacts to ingest.")

    # 3. Ingest Artifacts
    success_count = 0
    failure_count = 0

    for artifact in artifacts:
        try:
            # Use relative path as title or filename
            title = artifact.stem

            # Use create_source logic (upload type)
            # Note: For local files, we might be able to use 'file_path' if the API supports local path references
            # However, typically 'upload' expects the file content or an actual upload.
            # Given the API client logic, let's try reading content and sending as 'text' type to ensure compatibility
            # unless we confirm 'file_path' works for local backend access.
            # Let's read content to be safe and "AI-Ready".

            content = artifact.read_text(encoding="utf-8", errors="ignore")

            logger.info(f"   -> Ingesting: {title}")

            sources_service.create_source(
                notebooks=[target_notebook.id],
                source_type="text",
                title=title,
                content=content,
                embed=True,  # Critical for "Hidden Layers" connection
                async_processing=True,  # Let the worker handle embedding
            )
            success_count += 1

        except Exception as e:
            logger.error(f"   ❌ Failed to ingest {artifact.name}: {e}")
            failure_count += 1

    logger.info("-" * 40)
    logger.info(f"🏁 Ingestion Complete.")
    logger.info(f"   Notebook: {NOTEBOOK_NAME}")
    logger.info(f"   Success:  {success_count}")
    logger.info(f"   Failed:   {failure_count}")
    logger.info("-" * 40)


if __name__ == "__main__":
    ingest_artifacts()
