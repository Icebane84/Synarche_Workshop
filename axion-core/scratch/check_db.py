import os
import sqlite3

db_path = r"c:\Users\Chris\Synarche_Workspace\axion-core\data\axion_memory.db"
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        print(f"Schema for {table_name}:", cursor.fetchall())
    conn.close()
