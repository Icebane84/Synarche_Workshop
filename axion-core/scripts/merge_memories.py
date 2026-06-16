import logging
import os
import sqlite3

# Try to load sqlite-vec
try:
    import sqlite_vec

    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("merge_memories")

SRC_DB = r"c:\Users\Chris\Synarche_Workspace\axion-core\storage\axion_memory.db"
DST_DB = r"c:\Users\Chris\Synarche_Workspace\axion-core\data\axion_memory.db"


def merge():
    if not os.path.exists(SRC_DB):
        logger.error(f"Source database not found: {SRC_DB}")
        return
    if not os.path.exists(DST_DB):
        logger.error(f"Destination database not found: {DST_DB}")
        return

    logger.info(f"Merging {SRC_DB} into {DST_DB}...")

    src_conn = sqlite3.connect(SRC_DB)
    src_conn.row_factory = sqlite3.Row
    dst_conn = sqlite3.connect(DST_DB)
    dst_conn.row_factory = sqlite3.Row

    if HAS_SQLITE_VEC:
        src_conn.enable_load_extension(True)
        sqlite_vec.load(src_conn)
        dst_conn.enable_load_extension(True)
        sqlite_vec.load(dst_conn)
        logger.info("sqlite-vec extension loaded.")

    id_map = {}  # old_id -> new_id

    try:
        # 1. Merge memory_entries
        logger.info("Syncing memory_entries...")
        src_entries = src_conn.execute("SELECT * FROM memory_entries").fetchall()
        for row in src_entries:
            # Check for duplicate content in destination
            exists = dst_conn.execute(
                "SELECT id FROM memory_entries WHERE content = ?", (row["content"],)
            ).fetchone()
            if exists:
                id_map[row["id"]] = exists["id"]
                logger.debug(
                    f"Skipping duplicate memory: {row['id']} -> {exists['id']}"
                )
                continue

            # Insert new entry
            cursor = dst_conn.execute(
                "INSERT INTO memory_entries (content, domain, relevance, confidence, tags, vector, activation_score, state, source, usage_count, memory_layer, last_retrieved, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    row["content"],
                    row["domain"],
                    row["relevance"],
                    row["confidence"],
                    row["tags"],
                    row["vector"],
                    row["activation_score"],
                    row["state"],
                    row["source"],
                    row["usage_count"],
                    row["memory_layer"],
                    row["last_retrieved"],
                    row["created_at"],
                ),
            )
            new_id = cursor.lastrowid
            id_map[row["id"]] = new_id

            # Sync vec_memory_entries if available
            if HAS_SQLITE_VEC:
                vec_row = src_conn.execute(
                    "SELECT embedding FROM vec_memory_entries WHERE id = ?",
                    (row["id"],),
                ).fetchone()
                if vec_row:
                    dst_conn.execute(
                        "INSERT INTO vec_memory_entries (id, embedding) VALUES (?, ?)",
                        (new_id, vec_row["embedding"]),
                    )

        logger.info(
            f"Memory entries merged. ID mapping established for {len(id_map)} items."
        )

        # 2. Merge memory_gems
        logger.info("Syncing memory_gems...")
        src_gems = src_conn.execute("SELECT * FROM memory_gems").fetchall()
        for row in src_gems:
            if row["entry_id"] in id_map:
                dst_conn.execute(
                    "INSERT OR REPLACE INTO memory_gems (entry_id, insight_label, importance, created_at) VALUES (?, ?, ?, ?)",
                    (
                        id_map[row["entry_id"]],
                        row["insight_label"],
                        row["importance"],
                        row["created_at"],
                    ),
                )

        # 3. Merge memory_associations
        logger.info("Syncing memory_associations...")
        src_assocs = src_conn.execute("SELECT * FROM memory_associations").fetchall()
        for row in src_assocs:
            if row["source_id"] in id_map and row["target_id"] in id_map:
                dst_conn.execute(
                    "INSERT OR REPLACE INTO memory_associations (source_id, target_id, relationship_type, strength, created_at) VALUES (?, ?, ?, ?, ?)",
                    (
                        id_map[row["source_id"]],
                        id_map[row["target_id"]],
                        row["relationship_type"],
                        row["strength"],
                        row["created_at"],
                    ),
                )

        # 4. Merge experience_logs
        logger.info("Syncing experience_logs...")
        src_logs = src_conn.execute("SELECT * FROM experience_logs").fetchall()
        for row in src_logs:
            dst_conn.execute(
                "INSERT INTO experience_logs (timestamp, event_type, module, details, coherence_impact) VALUES (?, ?, ?, ?, ?)",
                (
                    row["timestamp"],
                    row["event_type"],
                    row["module"],
                    row["details"],
                    row["coherence_impact"],
                ),
            )

        dst_conn.commit()
        logger.info("Merge complete and committed.")

    except Exception as e:
        logger.exception(f"Merge failed: {e}")
        dst_conn.rollback()
    finally:
        src_conn.close()
        dst_conn.close()


if __name__ == "__main__":
    merge()
