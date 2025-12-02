import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv("POSTGRES_DB", "prs_db"),
        user=os.getenv("POSTGRES_USER", "prs_user"),
        password=os.getenv("POSTGRES_PASSWORD", "prs_password")
    )
    print("Success: Connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print(f"Error: Could not connect to database: {e}")
    exit(1)
