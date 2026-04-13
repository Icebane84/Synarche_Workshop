#!/usr/bin/env python3
"""
# TOOL-GEN-001: Genesis Ingestion Script
# Domain: ARCH | State: ACTIVE | Version: v1.0
# Objective: Ingest the 'tapestry.json' graph into the Supabase Knowledge Graph.
"""

import json
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Configuration
TAPESTRY_PATH = Path(r"c:\Users\Chris\Synarche_Workspace\tapestry.json")
NAMESPACE = uuid.NAMESPACE_DNS

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Ensure import path for nova_forge
# nova-forge is a sibling directory to axion-core
WORKSPACE_ROOT = Path(r"c:\Users\Chris\Synarche_Workspace")
NOVA_FORGE_PATH = WORKSPACE_ROOT / "nova-forge" / "src"
AXION_CORE_SRC = WORKSPACE_ROOT / "axion-core" / "src"

# Load Environment Variables from Workspace Root
ENV_PATH = WORKSPACE_ROOT / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    logger.info(f"Loaded environment from {ENV_PATH}")
else:
    logger.warning(f"No .env file found at {ENV_PATH}")

sys.path.append(str(NOVA_FORGE_PATH))
sys.path.append(str(AXION_CORE_SRC))

try:
    from nova_forge.backend.supabase_client import get_supabase
except ImportError as e:
    logger.exception(f"Import Error: {e}")
    logger.error(f"Sys Path: {sys.path}")
    raise


def get_uuid(artifact_id: str) -> str:
    """Generates a consistent UUID5 from an artifact ID string."""
    return str(uuid.uuid5(NAMESPACE, artifact_id))


def upsert_batch(client: Any, table: str, data: list[dict[str, Any]], batch_size: int = 100) -> None:
    """Helper to batch upsert data to Supabase."""
    if not data:
        return
    logger.info(f"[INFO] Upserting {len(data)} items into '{table}'...")
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        try:
            client.table(table).upsert(batch, on_conflict="id").execute()
            logger.info(f"   Processed {i} to {i + len(batch)}")
        except Exception as e:
            logger.error(f"[!] Batch upsert failed for table '{table}' at index {i}: {e}")


def ingest_tapestry() -> None:
    """Main ingestion logic."""
    if not TAPESTRY_PATH.exists():
        logger.error(f"[ERROR] Tapestry file not found: {TAPESTRY_PATH}")
        return

    logger.info(f"🔥 Loading Tapestry: {TAPESTRY_PATH}")
    try:
        with open(TAPESTRY_PATH, "r", encoding="utf-8") as f:
            tapestry = json.load(f)
    except Exception as e:
        logger.error(f"[ERROR] Failed to load JSON: {e}")
        return

    nodes = tapestry.get("nodes", {})
    logger.info(f"📚 Found {len(nodes)} nodes in Tapestry.")

    # Prepare Entities
    entities = []

    for key, node in nodes.items():
        # Ensure we have a valid ID
        raw_id = node.get("id", key)
        entity_uuid = get_uuid(raw_id)

        # Prepare Metadata
        metadata = node.get("metadata", {})
        content_preview = node.get("content_preview", "")
        if content_preview:
            metadata["content_preview"] = content_preview

        # Determine Title
        title = raw_id
        if "path" in node:
            title = Path(node["path"]).name

        entity = {
            "id": entity_uuid,
            "title": title,
            "type": node.get("type", "Artifact"),
            "metadata": metadata,
            # "content": ... # content is typically separate or large, tapestry keeps it light.
            # If we had full content we would map it, but entities usually takes metadata.
        }
        entities.append(entity)

    # Initialize Supabase
    try:
        client = get_supabase()
    except Exception as e:
        logger.error(f"[ERROR] Failed to connect to Supabase: {e}")
        return

    # Upsert Entities
    upsert_batch(client, "entities", entities)

    # (Optional) Process Links if properly structured in tapestry.json
    # Preview showed "links": [] lists. If they exist, we would map them here.
    # Current tapestry format for links seems to be a simple list of strings (Target IDs)
    relationships = []

    for key, node in nodes.items():
        source_uuid = get_uuid(node.get("id", key))
        links = node.get("links", [])

        for link_target in links:
            # We assume link_target is the ID string of another node
            target_uuid = get_uuid(link_target)
            edge_id = get_uuid(f"{node.get('id', key)}->{link_target}->references")

            rel = {
                "id": edge_id,
                "source_id": source_uuid,
                "target_id": target_uuid,
                "type": "references",
                "metadata": {"origin": "tapestry_genesis"},
            }
            relationships.append(rel)

    if relationships:
        upsert_batch(client, "relationships", relationships)

    logger.info("\n✅ Genesis Ingestion Complete.")


if __name__ == "__main__":
    ingest_tapestry()
