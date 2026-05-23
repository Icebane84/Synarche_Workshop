"""
# Universal Identification & Provenance (UIP)
| Field                  | Value                                          |
| :--------------------- | :--------------------------------------------- |
| **1. Artifact ID**     | `TOOL-MAGI-001`                                |
| **2. Official Name**   | `ingest_vault.py`                              |
| **3. Version**         | **v13.0**                                      |
| **4. Provenance**      | **Reforged: 2026-02-01**                       |
| **5. Domain**          | `ARCH` (Archival)                              |
| **6. Evolution**       | **Cognitive Ascension**                        |
| **7. Celestial Class** | `[PLANET]`                                     |
| **8. Tier**            | **Operational**                                |
| **9. Status (State)**  | `[ACTIVE]`                                     |
| **10. Ethos**          | **Total Recall**                               |
| **11. Catalyst**       | **System Ascension v13.0**                     |
| **12. Relations**      | `LINK: [CHAR-AXION-001]`, `GOVERNED_BY: [CORE-CODEX-001]` |
| **13. Integrity Hash** | `[AUTO-GENERATED]`                             |

---

### **I.B. Standardized Synergy Block (The Loom Signature)**

> [!NOTE]
> The following block is parsed by `TOOL-MAP-001` for architectural visualization.

| Synergistic Artifact ID | Relationship Type | Synergistic Impact |
| :--- | :--- | :--- |
| CHAR-AXION-001 | WIELDS | The Magician persona uses this tool for ingestion. |
| CORE-CODEX-001 | GOVERNS | This tool is governed by the Supreme Law. |

---

# --- RPG FRAMEWORK INTEGRATION ---
# System Slot: Ingestion Gate (The Magician)
# Synergy Set: The Hephaestus Hexad
# Primary Stat Buff: Intelligence (+15)
# Passive Ability: The Seer's Eye (Entity Discovery)
# Cognitive Load Cost: Medium
# XP Award Value: 100 XP
"""

import logging
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any

# Configuration
VAULT_PATH = Path(r"c:\Users\Chris\_Desktop_Vault\Phoenix\Obsidian\Where Light Fades")
NAMESPACE = uuid.NAMESPACE_DNS

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Ensure import path
sys.path.append(os.path.join(os.getcwd(), "src"))
from nova_forge.backend.supabase_client import get_supabase


def get_uuid(artifact_id: str) -> str:
    """Generates a consistent UUID5 from an artifact ID string."""
    return str(uuid.uuid5(NAMESPACE, artifact_id))


def extract_links(content: str) -> set[str]:
    """Extracts Obsidian [[Wikilinks]] from content."""
    links = re.findall(r"\[\[(.*?)(?:\|.*?)?\]\]", content)
    return set(links)


def determine_entity_type(rel_path: Path) -> str:
    """Determines entity type based on directory structure."""
    parent_dir = rel_path.parts[0] if len(rel_path.parts) > 1 else "misc"
    type_map = {
        "1. Core Concepts & Themes": "concept",
        "2. World & Setting": "location",
        "3. History, Lore, & Mythology": "history",
        "4. Society, Cultures, & Factions": "faction",
        "5. Magic and Power Systems": "magic",
        "6. Characters": "character",
        "7. Bestiary & Races": "race",
        "8. Artifacts Key Items": "artifact",
        "9. Plot and Narrative Structure": "narrative",
    }
    return type_map.get(parent_dir, "concept")


def upsert_batch(client: Any, table: str, data: list[dict[str, Any]], batch_size: int = 100) -> None:
    """Helper to batch upsert data to Supabase."""
    logger.info(f"[INFO] Upserting {len(data)} items into '{table}'...")
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        try:
            client.table(table).upsert(batch, on_conflict="id").execute()
            logger.info(f"   Processed {i} to {i + len(batch)}")
        except Exception:
            logger.exception(f"[!] Batch upsert failed for table '{table}' at index {i}")


def process_entities(files: list[Path]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Scans files and prepares entity records."""
    entities: list[dict[str, Any]] = []
    file_map: dict[str, str] = {}

    for file_path in files:
        if file_path.name.startswith("."):
            continue

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"[WARN] Failed to read {file_path}: {e}")
            continue

        title = file_path.stem
        file_map[title] = content

        # Calculate relative path safely
        try:
            rel_path = file_path.relative_to(VAULT_PATH)
        except ValueError:
            rel_path = Path("unknown") / file_path.name

        entity = {
            "id": get_uuid(title),
            "title": title,
            "type": determine_entity_type(rel_path),
            "metadata": {
                "source_path": str(rel_path),
                "summary": content[:500],
            },
        }
        entities.append(entity)

    return entities, file_map


def process_relationships(file_map: dict[str, str]) -> list[dict[str, Any]]:
    """Extracts links and creates relationship records."""
    relationships: list[dict[str, Any]] = []
    entity_titles = set(file_map.keys())

    for title, content in file_map.items():
        links = extract_links(content)
        source_uuid = get_uuid(title)

        for link in links:
            if link not in entity_titles:
                continue

            edge_id = get_uuid(f"{title}->{link}->references")
            rel = {
                "id": edge_id,
                "source_id": source_uuid,
                "target_id": get_uuid(link),
                "type": "references",
                "metadata": {"origin": "vault_ingestion"},
            }
            relationships.append(rel)

    return relationships


def ingest() -> None:
    """Main ingestion entry point."""
    if not VAULT_PATH.exists():
        logger.error(f"[ERROR] Vault path {VAULT_PATH} not found.")
        return

    logger.info(f"[INFO] Scanning Vault at {VAULT_PATH}...")
    files = list(VAULT_PATH.rglob("*.md"))
    logger.info(f"   Found {len(files)} markdown files.")

    try:
        client = get_supabase()
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return

    # 1. Process & Upsert Entities
    entities_to_upsert, file_map = process_entities(files)
    if entities_to_upsert:
        upsert_batch(client, "entities", entities_to_upsert)

    # 2. Process & Upsert Relationships
    relationships_to_upsert = process_relationships(file_map)
    if relationships_to_upsert:
        upsert_batch(client, "relationships", relationships_to_upsert)

    logger.info("\n[SUCCESS] Vault Ingestion Complete!")


if __name__ == "__main__":
    ingest()
