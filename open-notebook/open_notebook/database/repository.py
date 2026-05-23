import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypeVar, Union

from loguru import logger
from surrealdb import AsyncSurreal, RecordID  # type: ignore

T = TypeVar("T", dict[str, Any], list[dict[str, Any]])


def get_database_url():
    """Get database URL with backward compatibility"""

    # --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
    # System Slot: Passive Knowledge
    # Synergy Set: N/A
    # Primary Stat Buff: Adaptability
    # Passive Ability: The Forge's Heart (Auto-Refactor)
    # Cognitive Load Cost: Low
    # XP Award Value: 50 XP

    surreal_url = os.getenv("SURREAL_URL")
    if surreal_url:
        return surreal_url

    # Fallback to old format - WebSocket URL format
    address = os.getenv("SURREAL_ADDRESS", "localhost")
    port = os.getenv("SURREAL_PORT", "8000")
    return f"ws://{address}/rpc:{port}"


def get_database_password():
    """Get password with backward compatibility"""
    return os.getenv("SURREAL_PASSWORD") or os.getenv("SURREAL_PASS")


def parse_record_ids(obj: Any) -> Any:
    """Recursively parse and convert RecordIDs into strings."""
    if isinstance(obj, dict):
        return {k: parse_record_ids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [parse_record_ids(item) for item in obj]
    elif isinstance(obj, RecordID):
        return str(obj)
    return obj


def ensure_record_id(value: str | RecordID) -> RecordID:
    """Ensure a value is a RecordID."""
    if isinstance(value, RecordID):
        return value
    return RecordID.parse(value)


class DatabaseManager:
    _instance = None
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def get_db(self) -> AsyncSurreal:
        if self._client is None:
            self._client = AsyncSurreal(get_database_url())
            await self._client.connect()
            await self._client.signin(
                {
                    "username": os.environ.get("SURREAL_USER", "root"),
                    "password": get_database_password(),
                }
            )
            await self._client.use(
                os.environ.get("SURREAL_NAMESPACE", "test"),
                os.environ.get("SURREAL_DATABASE", "test"),
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None


@asynccontextmanager
async def db_connection():
    db = await DatabaseManager.get_instance().get_db()
    yield db
    # We do NOT close the connection here anymore, allowing reuse.


async def repo_query(
    query_str: str, vars: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Execute a SurrealQL query and return the results"""

    async with db_connection() as connection:
        try:
            result = parse_record_ids(await connection.query(query_str, vars))
            if isinstance(result, str):
                raise RuntimeError(result)
            return result
        except RuntimeError as e:
            # RuntimeError is raised for retriable transaction conflicts - log at debug to avoid noise
            logger.debug(str(e))
            raise
        except Exception as e:
            logger.exception(e)
            raise


async def repo_create(table: str, data: dict[str, Any]) -> dict[str, Any]:
    """Create a new record in the specified table"""
    # Remove 'id' attribute if it exists in data
    data.pop("id", None)
    data["created"] = datetime.now(timezone.utc)
    data["updated"] = datetime.now(timezone.utc)
    try:
        async with db_connection() as connection:
            result = parse_record_ids(await connection.insert(table, data))
            # SurrealDB may return a string error message instead of the expected record
            if isinstance(result, str):
                raise RuntimeError(result)
            return result
    except RuntimeError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.exception(e)
        raise RuntimeError("Failed to create record")


async def repo_relate(
    source: str, relationship: str, target: str, data: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Create a relationship between two records with optional data"""
    if data is None:
        data = {}
    query = f"RELATE {source}->{relationship}->{target} CONTENT $data;"
    # logger.debug(f"Relate query: {query}")

    return await repo_query(
        query,
        {
            "data": data,
        },
    )


async def repo_upsert(
    table: str, id: str | None, data: dict[str, Any], add_timestamp: bool = False
) -> list[dict[str, Any]]:
    """Create or update a record in the specified table"""
    data.pop("id", None)
    if add_timestamp:
        data["updated"] = datetime.now(timezone.utc)
    query = f"UPSERT {id if id else table} MERGE $data;"
    return await repo_query(query, {"data": data})


async def repo_update(
    table: str, id: str, data: dict[str, Any]
) -> list[dict[str, Any]]:
    """Update an existing record by table and id"""
    # If id already contains the table name, use it as is
    try:
        record_id = (
            id
            if isinstance(id, RecordID) or (":" in id and id.startswith(f"{table}:"))
            else f"{table}:{id}"
        )
        data.pop("id", None)
        if "created" in data and isinstance(data["created"], str):
            data["created"] = datetime.fromisoformat(data["created"])
        data["updated"] = datetime.now(timezone.utc)
        query = f"UPDATE {record_id} MERGE $data;"
        # logger.debug(f"Update query: {query}")
        result = await repo_query(query, {"data": data})
        return parse_record_ids(result)
    except Exception as e:
        raise RuntimeError(f"Failed to update record: {e!s}")


async def repo_delete(record_id: str | RecordID):
    """Delete a record by record id"""

    try:
        async with db_connection() as connection:
            return await connection.delete(ensure_record_id(record_id))
    except Exception as e:
        logger.exception(e)
        raise RuntimeError(f"Failed to delete record: {e!s}")


async def repo_insert(
    table: str, data: list[dict[str, Any]], ignore_duplicates: bool = False
) -> list[dict[str, Any]]:
    """Create a new record in the specified table"""
    try:
        async with db_connection() as connection:
            result = parse_record_ids(await connection.insert(table, data))
            # SurrealDB may return a string error message instead of the expected records
            if isinstance(result, str):
                raise RuntimeError(result)
            return result
    except RuntimeError as e:
        if ignore_duplicates and "already contains" in str(e):
            return []
        logger.error(str(e))
        raise
    except Exception as e:
        if ignore_duplicates and "already contains" in str(e):
            return []
        logger.exception(e)
        raise RuntimeError("Failed to create record")
