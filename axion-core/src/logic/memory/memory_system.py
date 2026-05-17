"""
### **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                          | Description       |
| :---------------- | :----------------------------- | :---------------- |
| **Artifact ID**   | `CORE-LOGIC-MEMORY-001`         | The Sovereign ID. |
| **Official Name** | `memory_system.py`             | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**              | The Standard.     |
| **Domain**        | `CORE-LOGIC`                   | The Subject.      |
| **Evolution**     | `Cognitive Repository`         | The Alignment.    |
| **Status (State)**| `[CANONIZED]`                  | The Lifecycle.    |
| **Celestial Class**| `[STAR]`                      | The Tier.         |
| **Relations**     | `IDENTITY: High Priestess`    | The Network.      |
| **Integrity Hash**| `[AUTO-GENERATED]`             | Verification.     |
| **Genesis Stamp** | `2026-03-07`                   | Creation Date.    |

**The Spirit Bomb Axiom: Cognitive Persistence (Law 28)**
> Implemented from Blueprint `GVRN.REG.CognitivePersistence.md`.
> Ethos: Memories are the Ledger of Existence.
"""

import array
import asyncio
import datetime
import json
import logging
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import sqlite_vec  # type: ignore

    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from dotenv import load_dotenv

try:
    import psycopg2
    import psycopg2.extras
    from psycopg2.extras import Json, RealDictCursor

    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
    Json: Any = None  # type: ignore
    RealDictCursor: Any = None  # type: ignore

# Synarche Imports
try:
    from ...agents.axion.insforge_client import insforge
    from ..nlp.emotion_analyzer import EmotionAnalyzer
    from ..nlp.nlp_engine import AxionCognition
    from ..sync.insforge_bridge import bridge as insforge_bridge
    from .association_manager import AssociationManager
    from .retrieval_engine import RetrievalEngine

    HAS_NLP_ENGINE = True
except ImportError:
    # Manual fallback for insforge if not in context
    try:
        from agents.axion.insforge_client import insforge
    except ImportError:
        insforge = Any  # type: ignore
    HAS_NLP_ENGINE = False

logger = logging.getLogger(__name__)

# Load environment variables
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.parent
DOTENV_PATH = r"c:\Users\Chris\Synarche_Workspace\.prs_database\.env"
load_dotenv(DOTENV_PATH)


class MemoryProtocols:
    """OMEGA Standard Global Thresholds for Cognitive Lifecycle."""

    # Transition Thresholds
    THRESHOLD_FADING = 0.2
    THRESHOLD_CONSOLIDATED = 0.8
    MIN_USAGE_CONSOLIDATED = 10
    THRESHOLD_ARCHIVED = 0.05
    THRESHOLD_REACTIVATE = 0.3

    # Layer Definitions
    LAYER_GEMS = 1
    LAYER_KINETIC = 2
    LAYER_SEMANTIC = 3
    LAYER_SOVEREIGN = 4
    LAYER_META = 5

    # Decay & Scoring
    RECENCY_HALFLIFE = 30.0
    COHERENCE_SYNC_THRESHOLD = 0.8


class GemMemoryAgent:
    """The Muse: Specialized agent for L1 Gem extraction and validation."""

    def __init__(self, system_reference: "MemorySystem") -> None:
        self.system = system_reference

    def gemify(self, entry_id: int, insight_label: str, importance: float = 1.0) -> bool:
        """Canonize a memory entry into an L1 Gem."""
        if not self.system.storage:
            return False

        try:
            # Update memory_layer in main entry
            self.system.storage.update_memory(
                entry_id,
                {"memory_layer": MemorySystem.LAYER_GEMS, "activation_score": 1.0},
            )

            # Add to memory_gems table
            conn = getattr(self.system.storage, "conn", None)
            if conn:
                with conn as c:
                    cur = c.cursor()
                    if isinstance(self.system.storage, PostgresMemoryStorage):
                        cur.execute(
                            "INSERT INTO memory_gems (entry_id, insight_label, importance) VALUES (%s, %s, %s) ON CONFLICT (entry_id) DO UPDATE SET importance = EXCLUDED.importance",
                            (entry_id, insight_label, importance),
                        )
                    else:  # SQLite
                        cur.execute(
                            "INSERT OR REPLACE INTO memory_gems (entry_id, insight_label, importance) VALUES (?, ?, ?)",
                            (entry_id, insight_label, importance),
                        )
                return True
            return False
        except Exception:
            logger.exception("Gemification failed")
            return False


@dataclass
class MemoryEntry:
    """Represents a single memory with lifecycle logic."""

    id: int
    content: str
    domain: str = "GeneralKnowledge"
    relevance: float = 0.5
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)
    activation_score: float = 0.5
    state: str = "Active"
    source: str = "Unknown"
    usage_count: int = 0
    layer: int = 2  # default to L2 Kinetic
    vector: list[float] | None = None
    created_at: datetime.datetime | None = None
    last_retrieved: datetime.datetime | None = None

    def decay(self, base_rate: float = 0.01) -> None:
        """Applies time-based decay to the activation score."""
        if self.state in ["Active", "Fading", "Consolidated"]:
            # Decay based on time since last retrieval
            last_time = self.last_retrieved or self.created_at or datetime.datetime.now(datetime.timezone.utc)
            if last_time.tzinfo is None:
                last_time = last_time.replace(tzinfo=datetime.timezone.utc)
            delta = datetime.datetime.now(datetime.timezone.utc) - last_time
            days = delta.days + (delta.seconds / 86400)

            # Relevance slows decay
            effective_rate = base_rate / (1.0 + self.relevance)
            decay_factor = (1 - effective_rate) ** days
            self.activation_score = max(0.0, min(1.0, self.activation_score * decay_factor))

    def transition(self) -> None:
        """Transitions memory state and layer based on activation and usage (OMEGA v15.0)."""
        old_state = self.state

        # 1. Active State Management
        if self.state == "Active":
            self._handle_active_transition()
        # 2. Fading/Archived/Consolidated State Management
        elif self.state == "Fading":
            self._handle_fading_transition()
        elif self.state == "Consolidated":
            self._handle_consolidated_transition()
        elif self.state == "Archived":
            self._handle_archived_transition()

        if self.state != old_state:
            logger.info(
                f"Memory {self.id} transitioned: {old_state} -> {self.state} (Score: {self.activation_score:.2f})"
            )

    def _handle_active_transition(self) -> None:
        """Process transitions for memories in the 'Active' state."""
        if self.activation_score < MemoryProtocols.THRESHOLD_FADING:
            self.state = "Fading"
        elif (
            self.activation_score > MemoryProtocols.THRESHOLD_CONSOLIDATED
            and self.usage_count > MemoryProtocols.MIN_USAGE_CONSOLIDATED
        ):
            self.state = "Consolidated"
            if self.layer == MemoryProtocols.LAYER_KINETIC:
                self.layer = MemoryProtocols.LAYER_SEMANTIC

    def _handle_fading_transition(self) -> None:
        """Process transitions for memories in the 'Fading' state."""
        if self.activation_score < MemoryProtocols.THRESHOLD_ARCHIVED:
            self.state = "Archived"
        elif self.activation_score > MemoryProtocols.THRESHOLD_REACTIVATE:
            self.state = "Active"

    def _handle_consolidated_transition(self) -> None:
        """Process transitions for memories in the 'Consolidated' state."""
        if self.activation_score < (MemoryProtocols.THRESHOLD_FADING * 1.5):
            self.state = "Fading"

    def _handle_archived_transition(self) -> None:
        """Process transitions for memories in the 'Archived' state."""
        if self.activation_score > MemoryProtocols.THRESHOLD_REACTIVATE:
            self.state = "Active"


class MemoryStorage(ABC):
    """Abstract base class for memory storage (The True Loom standard)."""

    VECTOR_DIM_OG = 384  # Local sentence-transformers (all-MiniLM-L6-v2)

    @abstractmethod
    def add_memory(self, entry: dict[str, Any]) -> int:
        """Persist a new memory entry. Returns the unique ID (int)."""
        pass

    @abstractmethod
    def retrieve_memories(self, query: str, limit: int) -> list[dict[str, Any]]:
        """Perform a keyword-based retrieval of memories."""
        pass

    @abstractmethod
    def vector_search(self, vector: list[float], limit: int) -> list[dict[str, Any]]:
        """Perform a semantic search using cosine similarity on embeddings."""
        pass

    @abstractmethod
    def add_soft_link(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        initial_strength: str = "Weak",
    ) -> bool:
        """Add a bidirectional soft link between two memory entries."""

    @abstractmethod
    def update_memory(self, memory_id: int, updates: dict[str, Any]) -> bool:
        """Update fields of an existing memory. Returns success status."""
        pass

    @abstractmethod
    def boost_access(self, ids: list[int]) -> None:
        """Increase usage count and activation score for specified memories."""
        pass

    @abstractmethod
    def get_all_active(self) -> list[dict[str, Any]]:
        """Retrieve all memories currently in a non-archived state."""
        pass


# Repository Layer


class PostgresMemoryStorage(MemoryStorage):
    """PostgreSQL backend for MemorySystem."""

    def __init__(self, db_config: dict[str, Any] | None = None) -> None:
        self.params = db_config or {}
        self.conn = self._connect()
        self._ensure_tables()

    def _connect(self) -> Any | None:
        """Establish connection to PostgreSQL."""
        if not HAS_PSYCOPG2:
            return None
        try:
            return psycopg2.connect(**self.params)
        except Exception:
            logger.info("Failed to connect to PostgreSQL")
            return None

    def _ensure_tables(self) -> None:
        """Initialize the PostgreSQL schema with vector support and relational tables."""
        if not self.conn:
            return
        try:
            with self.conn.cursor() as cur:
                # 1. Try to enable vector extension (True Loom)
                try:
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                except Exception:
                    logger.warning("pgvector extension not available. Falling back to FLOAT[].")
                    self.conn.rollback()

                # 2. Ensure tables exist
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS memory_entries (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        domain TEXT DEFAULT 'GeneralKnowledge',
                        relevance REAL DEFAULT 0.5,
                        confidence REAL DEFAULT 1.0,
                        tags TEXT[],
                        vector vector(384), -- Native pgvector
                        activation_score REAL DEFAULT 0.5,
                        state TEXT DEFAULT 'Active',
                        source TEXT DEFAULT 'Unknown',
                        usage_count INTEGER DEFAULT 0,
                        memory_layer INTEGER DEFAULT 2, -- L1-L5 Model
                        last_retrieved TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS memory_gems (
                        entry_id INTEGER PRIMARY KEY REFERENCES memory_entries(id) ON DELETE CASCADE,
                        insight_label TEXT,
                        importance REAL DEFAULT 1.0,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS memory_associations (
                        id SERIAL PRIMARY KEY,
                        source_id INTEGER REFERENCES memory_entries(id) ON DELETE CASCADE,
                        target_id INTEGER REFERENCES memory_entries(id) ON DELETE CASCADE,
                        relationship_type TEXT DEFAULT 'Thematic',
                        strength TEXT DEFAULT 'Weak',
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source_id, target_id)
                    );
                    CREATE TABLE IF NOT EXISTS experience_logs (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        event_type TEXT NOT NULL,
                        module TEXT NOT NULL,
                        details JSONB,
                        coherence_impact REAL DEFAULT 0.0
                    );
                """)
                # Ensure memory_layer exists (OMNI-V14 Migration)
                try:
                    cur.execute("ALTER TABLE memory_entries ADD COLUMN IF NOT EXISTS memory_layer INTEGER DEFAULT 2;")
                except Exception:
                    self.conn.rollback()
                    # Fallback for older PG versions
                    try:
                        cur.execute("""
                            DO $$ 
                            BEGIN 
                                IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='memory_entries' AND column_name='memory_layer') THEN
                                    ALTER TABLE memory_entries ADD COLUMN memory_layer INTEGER DEFAULT 2;
                                END IF;
                            END $$;
                        """)
                    except Exception:
                        self.conn.rollback()

                # 3. Attempt to upgrade to 'vector' type if possible
                try:
                    cur.execute(
                        "ALTER TABLE memory_entries ALTER COLUMN vector TYPE vector(384) USING vector::vector(384);"
                    )
                except Exception:
                    self.conn.rollback()
                    logger.debug("Native vector type upgrade skipped (pgvector missing).")

            self.conn.commit()
        except Exception:
            logger.exception("Error ensuring Postgres tables. Forcing SQLite fallback.")
            if self.conn:
                self.conn.close()
            self.conn = None

    def add_memory(self, entry: dict[str, Any]) -> int:
        """Persist a memory entry to PostgreSQL and return its serial ID."""
        if not self.conn:
            return -1
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO memory_entries (content, domain, relevance, confidence, tags, vector, source, memory_layer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        entry["content"],
                        entry["domain"],
                        entry["relevance"],
                        entry["confidence"],
                        entry["tags"],
                        entry.get("vector"),
                        entry["source"],
                        entry.get("memory_layer", 2),
                    ),
                )
                res = cur.fetchone()
                return res[0] if res else -1
        except Exception:
            logger.exception("Postgres add_memory failed")
            self.conn.rollback()
            return -1

    def retrieve_memories(self, query: str, limit: int) -> list[dict[str, Any]]:
        """Retrieve memories matching a keyword pattern from PostgreSQL."""
        if not self.conn:
            return []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM memory_entries WHERE content ILIKE %s AND state != 'Archived' LIMIT %s",
                    (f"%{query}%", limit),
                )
                return [dict(row) for row in cur.fetchall()]
        except Exception:
            logger.exception("Postgres retrieve failed")
            return []

    def vector_search(self, vector: list[float], limit: int) -> list[dict[str, Any]]:
        """Perform a semantic vector search in PostgreSQL using the <=> operator."""
        if not self.conn:
            return []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                # pgvector cosine similarity (<=>) or Euclidean distance (<->)
                # OMEGA v14.0 prefers cosine for semantic coherence
                # Explicitly cast to vector type for pgvector compatibility
                cur.execute(
                    "SELECT *, (vector <=> %s::vector) as distance FROM memory_entries WHERE state != 'Archived' ORDER BY vector <=> %s::vector LIMIT %s",
                    (str(vector), str(vector), limit),
                )
                return [dict(row) for row in cur.fetchall()]
        except Exception:
            logger.exception("Postgres vector search failed")
            return []

    def update_memory(self, memory_id: int, updates: dict[str, Any]) -> bool:
        """Update a memory entry with the provided fields."""
        if not self.conn:
            return False
        try:
            keys = updates.keys()
            set_clause = ", ".join([f"{k} = %s" for k in keys])
            with self.conn.cursor() as cur:
                cur.execute(
                    f"UPDATE memory_entries SET {set_clause} WHERE id = %s",
                    (*updates.values(), memory_id),
                )
            self.conn.commit()
            return True
        except Exception:
            logger.exception("Postgres update failed")
            self.conn.rollback()
            return False

    def boost_access(self, ids: list[int]) -> None:
        """Atomically increment usage counts and activation scores in PostgreSQL."""
        if not self.conn or not ids:
            return
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "UPDATE memory_entries SET usage_count = usage_count + 1, activation_score = LEAST(1.0, activation_score + 0.1), last_retrieved = CURRENT_TIMESTAMP WHERE id IN %s",
                    (tuple(ids),),
                )
            self.conn.commit()
        except Exception:
            logger.exception("Postgres boost failed")
            if self.conn:
                self.conn.rollback()

    def add_soft_link(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        initial_strength: str = "Weak",
    ) -> bool:
        """Add a soft link (association) between two memories in Postgres."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO memory_associations (source_id, target_id, relationship_type, strength) VALUES (%s, %s, %s, %s) ON CONFLICT (source_id, target_id) DO UPDATE SET strength = EXCLUDED.strength",
                    (int(source_id), int(target_id), rel_type, initial_strength),
                )
            self.conn.commit()
            return True
        except Exception:
            logger.exception("Postgres add_soft_link failed")
            if self.conn:
                self.conn.rollback()
            return False

    def get_all_active(self) -> list[dict[str, Any]]:
        """Retrieve all non-archived memory entries from the PostgreSQL repository."""
        if not self.conn:
            return []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM memory_entries WHERE state != 'Archived'")
                return [dict(row) for row in cur.fetchall()]
        except Exception:
            logger.exception("Postgres get_all_active failed")
            return []


class SQLiteMemoryStorage(MemoryStorage):
    """SQLite backend for local portability."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Load sqlite-vec extension
        if HAS_SQLITE_VEC:
            self.conn.enable_load_extension(True)
            sqlite_vec.load(self.conn)

        self._ensure_tables()

    def _ensure_tables(self) -> None:
        """Initialize the local SQLite schema with virtual vector tables support."""
        try:
            with self.conn:
                self.conn.execute("PRAGMA journal_mode=WAL;")
                self.conn.execute("PRAGMA synchronous=NORMAL;")
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS memory_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        domain TEXT DEFAULT 'GeneralKnowledge',
                        relevance REAL DEFAULT 0.5,
                        confidence REAL DEFAULT 1.0,
                        tags TEXT,
                        vector TEXT, -- Legacy JSON storage
                        activation_score REAL DEFAULT 0.5,
                        state TEXT DEFAULT 'Active',
                        source TEXT DEFAULT 'Unknown',
                        usage_count INTEGER DEFAULT 0,
                        memory_layer INTEGER DEFAULT 2, -- L1-L5 Model
                        last_retrieved TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                # Create native vector virtual table (The True Loom)
                # sqlite-vec uses vec0 virtual tables
                # Dimension 1536 matches standard embeddings (e.g. OpenAI)
                self.conn.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS vec_memory_entries USING vec0(
                        id INTEGER PRIMARY KEY,
                        embedding FLOAT[384]
                    );
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS memory_gems (
                        entry_id INTEGER PRIMARY KEY,
                        insight_label TEXT,
                        importance REAL DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(entry_id) REFERENCES memory_entries(id) ON DELETE CASCADE
                    );
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS memory_associations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_id INTEGER,
                        target_id INTEGER,
                        relationship_type TEXT DEFAULT 'Thematic',
                        strength TEXT DEFAULT 'Weak',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source_id, target_id),
                        FOREIGN KEY(source_id) REFERENCES memory_entries(id) ON DELETE CASCADE,
                        FOREIGN KEY(target_id) REFERENCES memory_entries(id) ON DELETE CASCADE
                    );
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS experience_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        event_type TEXT NOT NULL,
                        module TEXT NOT NULL,
                        details TEXT,
                        coherence_impact REAL DEFAULT 0.0
                    );
                """)
                # Ensure memory_layer exists (SQLite Migration)
                try:
                    self.conn.execute("ALTER TABLE memory_entries ADD COLUMN memory_layer INTEGER DEFAULT 2;")
                except sqlite3.OperationalError:
                    pass  # Column already exists
        except Exception:
            logger.exception("Error ensuring SQLite tables")

    def add_memory(self, entry: dict[str, Any]) -> int:
        """Add a memory entry to SQLite."""
        try:
            with self.conn:
                # 1. Main entry
                cur = self.conn.execute(
                    "INSERT INTO memory_entries (content, domain, relevance, confidence, tags, vector, source, state, activation_score, usage_count, memory_layer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        entry["content"],
                        entry.get("domain", "GeneralKnowledge"),
                        entry.get("relevance", 0.5),
                        entry.get("confidence", 1.0),
                        ",".join(entry.get("tags", [])),
                        json.dumps(entry.get("vector")),
                        entry.get("source", "Unknown"),
                        entry.get("state", "Active"),
                        entry.get("activation_score", 0.5),
                        entry.get("usage_count", 0),
                        entry.get("memory_layer", 2),
                    ),
                )
                memory_id = cur.lastrowid

                # 2. Native Vector Entry (The True Loom integration)
                vector_data = entry.get("vector")
                if vector_data and len(vector_data) == self.VECTOR_DIM_OG:  # Legacy hardcoded for now
                    vec_blob = array.array("f", vector_data).tobytes()
                    self.conn.execute(
                        "INSERT INTO vec_memory_entries(id, embedding) VALUES (?, ?)",
                        (memory_id, vec_blob),
                    )

                return int(memory_id) if memory_id is not None else -1
        except Exception:
            logger.exception("SQLite add_memory failed")
            return -1

    def retrieve_memories(self, query: str, limit: int) -> list[dict[str, Any]]:
        """Perform a standard SQL LIKE search across the SQLite memory repository."""
        try:
            # Native SQLite keyword search (fallback/base)
            cur = self.conn.execute(
                "SELECT * FROM memory_entries WHERE content LIKE ? AND state != 'Archived' LIMIT ?",
                (f"%{query}%", limit),
            )
            rows = cur.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d["tags"] = d["tags"].split(",") if d["tags"] else []
                d["vector"] = json.loads(d["vector"]) if d["vector"] else None
                results.append(d)
        except Exception:
            logger.exception("SQLite retrieve failed")
            return []
        else:
            return results

    def vector_search(self, vector: list[float], limit: int) -> list[dict[str, Any]]:
        """Perform semantic search using SQLite-vec or fallback to numpy cosine similarity."""
        try:
            if len(vector) != self.VECTOR_DIM_OG:
                logger.warning(f"Vector search failed: dimension mismatch ({len(vector)} != {self.VECTOR_DIM_OG})")
                return []

            if HAS_SQLITE_VEC:
                vec_blob = array.array("f", vector).tobytes()
                # 1. Search in the virtual table for IDs
                cur = self.conn.execute(
                    "SELECT id, distance FROM vec_memory_entries WHERE embedding MATCH ? ORDER BY distance LIMIT ?",
                    (vec_blob, limit),
                )
                vec_results = cur.fetchall()
                if not vec_results:
                    return []

                # 2. Fetch full memory details
                ids = [r["id"] for r in vec_results]
                placeholders = ",".join(["?"] * len(ids))
                cur = self.conn.execute(
                    f"SELECT * FROM memory_entries WHERE id IN ({placeholders})",
                    tuple(ids),
                )
                rows = cur.fetchall()

                # Reconstruct and map distances
                dist_map = {r["id"]: r["distance"] for r in vec_results}
                results = []
                for row in rows:
                    d = dict(row)
                    d["tags"] = d["tags"].split(",") if d["tags"] else []
                    d["vector"] = json.loads(d["vector"]) if d["vector"] else None
                    d["semantic_distance"] = dist_map.get(d["id"])
                    if d.get("state") != "Archived":
                        results.append(d)

                return sorted(results, key=lambda x: x.get("semantic_distance", 1.0))

            # --- NUMPY FALLBACK (The True Loom / Intuition Engine script) ---
            if HAS_NUMPY:
                cur = self.conn.execute("SELECT * FROM memory_entries WHERE state != 'Archived' AND vector IS NOT NULL")
                rows = cur.fetchall()

                query_vec = np.array(vector, dtype=np.float32)
                query_norm = np.linalg.norm(query_vec)
                if query_norm == 0:
                    return []

                results = []
                for row in rows:
                    d = dict(row)
                    try:
                        mem_vec_data = json.loads(d["vector"]) if d["vector"] else None
                        if not mem_vec_data or len(mem_vec_data) != self.VECTOR_DIM_OG:
                            continue

                        mem_vec = np.array(mem_vec_data, dtype=np.float32)
                        mem_norm = np.linalg.norm(mem_vec)
                        if mem_norm == 0:
                            continue

                        # Cosine similarity (1.0 = identical, -1.0 = opposite)
                        similarity = np.dot(query_vec, mem_vec) / (query_norm * mem_norm)
                        # Convert to distance for consistency (0.0 = identical, 2.0 = opposite)
                        distance = 1.0 - similarity
                        d["semantic_distance"] = float(distance)
                        d["tags"] = d["tags"].split(",") if d["tags"] else []
                        d["vector"] = mem_vec_data
                        results.append(d)
                    except Exception as e:
                        logger.warning(f"Error computing numpy similarity for memory {d['id']}: {e}")

                # Sort by smallest distance (highest similarity)
                results.sort(key=lambda x: x.get("semantic_distance", 1.0))
                return results[:limit]

            logger.warning("Neither sqlite-vec nor numpy is available for vector search.")
            return []

        except Exception:
            logger.exception("SQLite vector search (fallback) failed")
            return []

    def update_memory(self, memory_id: int, updates: dict[str, Any]) -> bool:
        """Update a memory entry in SQLite."""
        try:
            if "tags" in updates:
                updates["tags"] = ",".join(updates["tags"])
            if "vector" in updates:
                updates["vector"] = json.dumps(updates["vector"])

            keys = updates.keys()
            set_clause = ", ".join([f"{k} = ?" for k in keys])
            with self.conn:
                self.conn.execute(
                    f"UPDATE memory_entries SET {set_clause} WHERE id = ?",
                    (*updates.values(), memory_id),
                )
            return True
        except Exception:
            logger.exception("SQLite update failed")
            return False

    def boost_access(self, ids: list[int]) -> None:
        """Increment usage and activation scores for the specified SQLite entry IDs."""
        if not ids:
            return
        try:
            placeholders = ",".join(["?"] * len(ids))
            with self.conn:
                self.conn.execute(
                    f"UPDATE memory_entries SET usage_count = usage_count + 1, activation_score = MIN(1.0, activation_score + 0.1), last_retrieved = CURRENT_TIMESTAMP WHERE id IN ({placeholders})",
                    tuple(ids),
                )
        except Exception:
            logger.exception("SQLite boost failed")

    def add_soft_link(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        initial_strength: str = "Weak",
    ) -> bool:
        """Add a soft link (association) between two memories in SQLite."""
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT OR REPLACE INTO memory_associations (source_id, target_id, relationship_type, strength) VALUES (?, ?, ?, ?)",
                    (int(source_id), int(target_id), rel_type, initial_strength),
                )
            return True
        except Exception:
            logger.exception("SQLite add_soft_link failed")
            return False

    def get_all_active(self) -> list[dict[str, Any]]:
        """Return all SQLite memory entries currently in non-archived states."""
        try:
            cur = self.conn.execute("SELECT * FROM memory_entries WHERE state != 'Archived'")
            rows = cur.fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d["tags"] = d["tags"].split(",") if d["tags"] else []
                d["vector"] = json.loads(d["vector"]) if d["vector"] else None
                results.append(d)
            return results
        except Exception:
            logger.exception("SQLite get_all_active failed")
            return []


class MemorySystem:
    """Sovereign Memory System for Axion.
    Coordinates storage, retrieval, and cognitive lifecycle.
    """

    # Constants mirrored from MemoryProtocols for backward compatibility
    THRESHOLD_FADING = MemoryProtocols.THRESHOLD_FADING
    THRESHOLD_CONSOLIDATED = MemoryProtocols.THRESHOLD_CONSOLIDATED
    MIN_USAGE_CONSOLIDATED = MemoryProtocols.MIN_USAGE_CONSOLIDATED
    THRESHOLD_ARCHIVED = MemoryProtocols.THRESHOLD_ARCHIVED
    THRESHOLD_REACTIVATE = MemoryProtocols.THRESHOLD_REACTIVATE
    RECENCY_HALFLIFE = MemoryProtocols.RECENCY_HALFLIFE
    COHERENCE_SYNC_THRESHOLD = MemoryProtocols.COHERENCE_SYNC_THRESHOLD

    # Layer Constants
    LAYER_GEMS = MemoryProtocols.LAYER_GEMS
    LAYER_KINETIC = MemoryProtocols.LAYER_KINETIC
    LAYER_SEMANTIC = MemoryProtocols.LAYER_SEMANTIC
    LAYER_SOVEREIGN = MemoryProtocols.LAYER_SOVEREIGN
    LAYER_META = MemoryProtocols.LAYER_META

    def __init__(
        self,
        db_config: dict[str, Any] | None = None,
        db_path: str | None = None,
        obsidian_bridge: Any | None = None,
    ) -> None:
        # 1. Initialize Storage (Polymorphic)
        self.params = db_config or {}
        self.storage: MemoryStorage | None = None

        if HAS_PSYCOPG2 and self.params:
            try:
                # Attempt to connect to PostgreSQL
                conn = psycopg2.connect(**self.params)
                conn.close()
                self.storage = PostgresMemoryStorage(self.params)
                logger.info("Using PostgreSQL storage.")
            except Exception:
                logger.warning("PostgreSQL initialization failed. Falling back to default SQLite.")
                self.storage = None

        if not self.storage:
            # Sovereign SQLite path resolution (OMEGA v15.0)
            # Prioritize 'data/' for canonical knowledge base
            data_db = r"c:\Users\Chris\Synarche_Workspace\axion-core\data\axion_memory.db"
            storage_db = r"c:\Users\Chris\Synarche_Workspace\axion-core\storage\axion_memory.db"

            final_db_path = db_path or (data_db if os.path.exists(data_db) else storage_db)
            os.makedirs(os.path.dirname(final_db_path), exist_ok=True)
            self.storage = SQLiteMemoryStorage(final_db_path)
            logger.info(f"Using SQLite storage at {final_db_path}")

        # 2. Sovereign Memory Path (OMEGA v15.0 Pathing)
        self.sovereign_memory_path = WORKSPACE_ROOT / "_governance" / "06_Learning" / "GVRN.Learning.Evolution.md"

        self.cognition: AxionCognition | None = None
        self.retriever: RetrievalEngine | None = None
        self.associations: AssociationManager | None = None
        self.emotions = EmotionAnalyzer() if HAS_NLP_ENGINE else None
        self.obsidian_bridge = obsidian_bridge
        self.muse = GemMemoryAgent(self)

        if HAS_NLP_ENGINE:
            try:
                self.cognition = AxionCognition()
                self.retriever = RetrievalEngine(self.cognition)
                self.associations = AssociationManager(self)
            except Exception:
                logger.exception("Failed to initialize cognitive components")

    @property
    def sync_status(self) -> bool:
        """Check synchronization status of memory state."""
        return True

    @property
    def conn(self) -> Any:
        """Expose storage connection for legacy/direct access if needed."""
        return getattr(self.storage, "conn", None) if self.storage else None

    def add_memory(
        self,
        content: str,
        domain: str = "GeneralKnowledge",
        relevance: float = 0.5,
        confidence: float = 1.0,
        tags: list[str] | None = None,
        source: str = "Unknown",
        layer: int = 2,
    ) -> int:
        """Add a memory entry to the system with automated cognitive processing."""
        if tags is None:
            tags = []
        if not self.storage:
            return -1

        try:
            vector = self.cognition.process(content).get("vector") if self.cognition else None
            entry = {
                "content": content,
                "domain": domain,
                "relevance": relevance,
                "confidence": confidence,
                "tags": tags,
                "vector": vector,
                "source": source,
                "memory_layer": layer,
                "is_sovereign": (layer == MemorySystem.LAYER_SOVEREIGN),
            }
            # Automatically detect emotions and add to tags
            if self.emotions:
                detected = self.emotions.detect_emotions(content)
                for emo in detected:
                    if emo not in tags:
                        tags.append(emo)

            memory_id = self.storage.add_memory(entry)

            if memory_id == -1:
                return -1

            self.log_experience("MEMORY_ADD", "MemorySystem", {"id": memory_id, "domain": domain}, 0.1)

            # Trigger automatic linking
            if self.associations:
                self.associations.trigger_tag_based_linking(str(memory_id), tags)

            # 2. InsForge Recording (The Chronicler)
            if hasattr(insforge, "log_event"):
                try:
                    loop = asyncio.get_event_loop()
                    event_type = "MEMORY_ADD"
                    desc = f"New memory added to {domain} layer {layer}."

                    if loop.is_running():
                        _ = loop.create_task(
                            insforge.log_event(
                                type=event_type,
                                description=desc,
                                payload={
                                    "id": memory_id,
                                    "domain": domain,
                                    "layer": layer,
                                },
                            )
                        )
                        # Divine Bridge: Full Sync
                        _ = loop.create_task(insforge_bridge.sync_memory_entry(entry))
                except Exception as e:
                    logger.debug(f"InsForge recording deferred for memory {memory_id}: {e}")

            return memory_id
        except Exception:
            logger.exception("Failed to add memory")
            return -1

    def maintenance_cycle(self) -> int:
        """Triggers the cognitive decay and transition loop for all active memories.
        Returns the count of transitioned memories.
        """
        if not self.storage:
            return 0

        logger.info("--- [COG-MEM] Starting Maintenance Cycle ---")
        active_memories = self.storage.get_all_active()
        transitions = 0

        for mem in active_memories:
            # 1. Parse timestamps (SQLite compatibility)
            created_at = mem.get("created_at")
            last_retrieved = mem.get("last_retrieved")

            if isinstance(created_at, str):
                try:
                    created_at = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                except ValueError:
                    created_at = datetime.datetime.now(datetime.timezone.utc)
            if isinstance(last_retrieved, str):
                try:
                    last_retrieved = datetime.datetime.fromisoformat(last_retrieved.replace("Z", "+00:00"))
                except ValueError:
                    last_retrieved = None

            # 2. Reconstruct MemoryEntry
            entry = MemoryEntry(
                id=mem["id"],
                content=mem["content"],
                domain=mem.get("domain", "General"),
                relevance=mem.get("relevance", 0.5),
                confidence=mem.get("confidence", 1.0),
                tags=mem.get("tags") if isinstance(mem.get("tags"), list) else [],
                activation_score=mem.get("activation_score", 0.5),
                state=mem.get("state", "Active"),
                source=mem.get("source", "Unknown"),
                usage_count=mem.get("usage_count", 0),
                layer=mem.get("memory_layer", 2),
                vector=mem.get("vector"),
                created_at=created_at,
                last_retrieved=last_retrieved,
            )

            old_layer = entry.layer
            old_state = entry.state
            old_score = entry.activation_score

            # 3. Apply Decay & Transition logic
            entry.decay()
            entry.transition()

            # 4. Persistence if shifted significantly (>0.01 score or state/layer change)
            if entry.layer != old_layer or entry.state != old_state or abs(entry.activation_score - old_score) > 0.01:
                updates = {
                    "memory_layer": entry.layer,
                    "state": entry.state,
                    "activation_score": entry.activation_score,
                }
                self.storage.update_memory(entry.id, updates)
                transitions += 1

                # Divine Bridge: Sync evolved state
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        _ = loop.create_task(insforge_bridge.sync_memory_entry(vars(entry)))
                except Exception:
                    pass

                # 5. Chronicler Signal for Layer Ascension
                if (entry.layer > old_layer or entry.state != old_state) and hasattr(insforge, "log_event"):
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            _ = loop.create_task(
                                insforge.log_event(
                                    type="MEMORY_EVOLUTION",
                                    description=f"Memory {entry.id} evolved: {old_state}(L{old_layer}) -> {entry.state}(L{entry.layer})",
                                    payload={
                                        "id": entry.id,
                                        "from_layer": old_layer,
                                        "to_layer": entry.layer,
                                        "score": entry.activation_score,
                                    },
                                )
                            )
                    except Exception:
                        pass

        logger.info(f"--- [COG-MEM] Maintenance Complete. Transitions: {transitions} ---")
        return transitions

    def gemify(self, entry_id: int, insight_label: str, importance: float = 1.0) -> bool:
        """Shortcut to elevate a memory to an L1 Gem."""
        return self.muse.gemify(entry_id, insight_label, importance)

    def retrieve_by_layer(self, layer: int, limit: int = 10) -> list[dict[str, Any]]:
        """Retrieve all memories belonging to a specific layer."""
        if not self.storage:
            return []
        try:
            conn = getattr(self.storage, "conn", None)
            if not conn:
                return []

            cur = conn.cursor()
            try:
                if isinstance(self.storage, PostgresMemoryStorage):
                    cur.execute(
                        "SELECT * FROM memory_entries WHERE memory_layer = %s LIMIT %s",
                        (layer, limit),
                    )
                else:
                    cur.execute(
                        "SELECT * FROM memory_entries WHERE memory_layer = ? LIMIT ?",
                        (layer, limit),
                    )
                return [dict(row) for row in cur.fetchall()]
            finally:
                cur.close()
        except Exception:
            logger.exception(f"Failed to retrieve by layer {layer}")
            return []

    def retrieve_memories(
        self, query: str, limit: int = 5, conversation_history: list[dict] | None = None
    ) -> list[dict[str, Any]]:
        """Perform contextual hybrid search across all active memory layers and external bridges."""
        if not self.storage:
            return []
        try:
            # 1. Base Retrieval (Keyword + Semantic)
            # In a partitioned system, we might search specific domains first
            memories = self.storage.retrieve_memories(query, limit)

            # 2. Hybrid Retrieval (Obsidian Vault Integration)
            if self.obsidian_bridge:
                try:
                    # Obsidian Local REST API expects a JSON query object
                    search_query = {"query": query, "contextLength": 100}
                    obsidian_results = self.obsidian_bridge.search(search_query)

                    for res in obsidian_results:
                        # Transmute to memory candidate format
                        # Extract tags from content if possible (very basic)
                        tags = res.get("tags", [])
                        candidate = {
                            "id": f"obs_{res.get('path', '').split('/')[-1]}",
                            "content": res.get("content", ""),
                            "source": "Obsidian",
                            "tags": tags,
                            "metadata": {
                                "path": res.get("path"),
                                "score": res.get("score", 0.0),
                            },
                        }
                        # Deduplicate by content (basic)
                        if not any(m["content"] == candidate["content"] for m in memories):
                            memories.append(candidate)
                except Exception as e:
                    logger.warning(f"Obsidian search failed: {e}")

            # 3. Apply Multi-Factor Ranking
            rewards = {"insight_xp": 0, "coherence_impact": 0.05}
            if self.retriever and memories:
                # Upgraded to support conversation_history for contextual bonus
                memories, rewards = self.retriever.score_memories(
                    query, memories, conversation_history=conversation_history
                )

                # Boost activation for top results
                self._boost_memory_access([m["id"] for m in memories[:3]])

            # 3. Handle No Information (Uncertainty Protocol)
            if not memories:
                analysis = self.cognition.process(query) if self.cognition else {}
                logger.info(f"Memory Gap Detected for query: {query}")
                # Log gap to database for future learning
                self.log_experience(
                    "MEMORY_GAP",
                    "MemorySystem",
                    {"query": query, "analysis": analysis},
                    -0.1,
                )
                memories = []

            # Log the experience
            self.log_experience(
                "MEMORY_RETRIEVE",
                "MemorySystem",
                {"query": query, "match_count": len(memories), "rewards": rewards},
                rewards.get("coherence_impact", 0.05),
            )
            return memories
        except Exception:
            logger.exception("Failed to retrieve memories")
            return []

    def handle_no_information(self, query: str, query_analysis: dict[str, Any]) -> str:
        """Generate agent response when no relevant memories are found (GGMA Standard)."""
        topics = query_analysis.get("entities", [])
        if not topics:
            topics = query_analysis.get("lemmas", [])

        # Log this missing information to the system
        memory_id = -1
        if self.cognition:
            memory_id = self.add_memory(
                content=f"No direct information found for: {query}",
                tags=topics,
                source="Sentinel_Fallback",
            )
            if self.associations and memory_id != -1:
                self.associations.trigger_tag_based_linking(str(memory_id), topics)

        response_parts = [f"I couldn't find specific information about '{query[:30]}' in my core memory."]

        if topics:
            primary_topic = topics[0][0] if isinstance(topics[0], tuple) else topics[0]
            response_parts.append(f"Could you provide more context about '{primary_topic}'?")
        else:
            response_parts.append("Could you please rephrase or provide more details?")

        response_parts.append("I've noted this gap to improve my internal model.")
        return " ".join(response_parts)

    def request_clarification(self, query: str) -> str:
        """Generate a clarification request for ambiguous queries."""
        return f"Could you please provide more details or rephrase your request regarding '{query[:50]}...'? I need a bit more context to be accurate."

    def _boost_memory_access(self, ids: list[int]) -> None:
        """Increments usage and resets last_retrieved."""
        if not self.storage or not ids:
            return
        try:
            self.storage.boost_access(ids)
        except Exception:
            logger.exception("Failed to boost memory access")

    def perform_maintenance(self) -> None:
        """[OMEGA-V14] Automated maintenance and 'Healing' cycle.

        Directive: 'Anticipate Failure' (Handbook 1.1.3).
        Triggers decay, state transitions, and structural integrity checks.
        """
        if not self.storage:
            return

        logger.info("Maintenance cycle initiated.")
        try:
            # 1. Structural Healing: Verify DB stability (Anticipate Failure)
            if isinstance(self.storage, SQLiteMemoryStorage):
                try:
                    self.storage.conn.execute("PRAGMA integrity_check;")
                except sqlite3.DatabaseError:
                    logger.critical("Memory Database Corruption detected. Initiating recovery protocols.")
                    # In a production scenario, this would trigger backup restoration or re-indexing

            # 2. Cognitive Decay & State Transitions
            active_memories = self.storage.get_all_active()
            decayed_count = 0
            for row in active_memories:
                # Reconstruct entry for lifecycle logic
                # We use the row dictionary directly as kwargs
                mem = MemoryEntry(**row)

                old_state = mem.state
                old_score = mem.activation_score

                mem.decay()
                mem.transition()

                # Update storage if state, score, or layer changed
                if mem.activation_score != old_score or mem.state != old_state or mem.layer != row.get("memory_layer"):
                    self.storage.update_memory(
                        mem.id,
                        {
                            "activation_score": mem.activation_score,
                            "state": mem.state,
                            "usage_count": mem.usage_count,
                            "memory_layer": mem.layer,
                        },
                    )
                    decayed_count += 1

            logger.info(f"Cognitive maintenance cycle completed. Decayed {decayed_count} entries.")
        except Exception:
            logger.exception("Maintenance cycle failed")

    def log_experience(self, event_type: str, module: str, details: dict[str, Any], impact: float = 0.0) -> None:
        """Logs experiences to Kinetic Memory (DB) and potentially Sovereign Memory (MD)."""
        if not self.storage:
            return

        # 1. Kinetic Memory (DB)
        try:
            # We use direct connection if available for legacy consistency, or storage methods
            conn = getattr(self.storage, "conn", None)
            if conn:
                cur = conn.cursor()
                try:
                    if isinstance(self.storage, PostgresMemoryStorage):
                        cur.execute(
                            "INSERT INTO experience_logs (event_type, module, details, coherence_impact) VALUES (%s, %s, %s, %s)",
                            (event_type, module, Json(details), impact),
                        )
                    else:  # SQLite
                        cur.execute(
                            "INSERT INTO experience_logs (event_type, module, details, coherence_impact) VALUES (?, ?, ?, ?)",
                            (event_type, module, json.dumps(details), impact),
                        )
                    conn.commit()
                finally:
                    cur.close()
        except Exception:
            logger.exception("Failed to log experience to Kinetic Memory")

        # 2. Sovereign Memory (MD Sync) - Only for significant impact or specific event types
        if impact >= self.COHERENCE_SYNC_THRESHOLD or event_type in [
            "ASCENSION",
            "SYNERGY_FOUND",
            "CRITICAL_LEARNING",
        ]:
            self._sync_to_sovereign(event_type, module, details)

        # 3. Divine Bridge (InsForge Sync) - Mirror experience logs
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                _ = loop.create_task(insforge_bridge.sync_experience_log(event_type, details))
        except Exception:
            pass

    def _sync_to_sovereign(self, event_type: str, module: str, details: dict[str, Any]) -> None:
        """Synchronizes high-impact events with the Sovereign Memory Ledger."""
        if not self.sovereign_memory_path.exists():
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        entry = f"### [{timestamp}] {event_type} ({module})\n"
        entry += f"- **Insight:** {details.get('content', details.get('insight', 'No summary provided.'))}\n"
        if "impact" in details:
            entry += f"- **Coherence Impact:** {details['impact']}\n"
        entry += "\n"

        try:
            with open(self.sovereign_memory_path, encoding="utf-8") as f:
                content = f.read()

            # Find the "[ARTIFACT START]" or "## **[ARTIFACT START]**" section (OMEGA v15.0)
            marker = "[ARTIFACT START]"
            if marker in content:
                parts = content.split(marker)
                # Insert below the marker with a blank line
                new_content = parts[0] + marker + "\n\n" + entry + parts[1]
                with open(self.sovereign_memory_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                logger.info(f"Sovereign Memory synchronized: {event_type}")
        except Exception as e:
            logger.error(f"Failed to sync with Sovereign Memory: {e}")

    def __del__(self) -> None:
        """Ensure storage connections are safely closed upon object destruction."""
        if hasattr(self, "storage") and getattr(self, "storage", None):
            try:
                conn = getattr(self.storage, "conn", None)
                if conn:
                    conn.close()
            except Exception:
                pass


# ---
#
# ### **Block G: The Omni-Anchor (System Snapshot)**
#
# `[OMNI-ARTIFACT-ANCHOR] ID: CORE.memory.system VER: v15.0 [OMEGA] DOMAIN: CORE STATUS: [SYNTHESIZED] TS: 2026-03-28 HASH: OMEGA-V15`
#
