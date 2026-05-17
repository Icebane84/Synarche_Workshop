import sqlite3
import os

db_path = r'c:\Users\Chris\Synarche_Workspace\axion-core\data\axion_memory.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(experience_logs);")
print("Schema for experience_logs:", cursor.fetchall())
conn.close()
