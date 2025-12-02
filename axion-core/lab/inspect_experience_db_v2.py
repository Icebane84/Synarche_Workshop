import os
import sqlite3

db_path = r"c:\Users\Chris\Synarche_Workspace\axion-core\data\GVRN.Log.Experience.db"
print(f"Checking: {db_path}")

if not os.path.exists(db_path):
    print("File not found")
else:
    print(f"File size: {os.path.getsize(db_path)}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info({table_name});")
            print(f"Schema {table_name}: {cursor.fetchall()}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
