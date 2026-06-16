import sqlite3

db_path = r"c:\Users\Chris\Synarche_Workspace\axion-core\data\axion_memory.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE experience_logs ADD COLUMN stardust_value REAL DEFAULT 0.0;"
    )
    print("Migration: Added stardust_value to experience_logs.")
except sqlite3.OperationalError as e:
    print(f"Migration Skipped (Already exists?): {e}")

try:
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS persona_state (id INTEGER PRIMARY KEY, persona_class TEXT, stardust_pool REAL, prestige_level INTEGER);"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO persona_state (id, persona_class, stardust_pool, prestige_level) VALUES (1, 'Novice', 0, 0);"
    )
    print("Migration: Created persona_state table.")
except sqlite3.OperationalError as e:
    print(f"Migration Failed: {e}")

conn.commit()
conn.close()
