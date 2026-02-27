import sqlite3
from pathlib import Path

DB_PATH = Path("db/feature_encoding.db")

def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        cluster_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clusters (
        cluster_id INTEGER PRIMARY KEY,
        keywords TEXT,
        silhouette_score REAL
    )
    """)

    conn.commit()
    conn.close()

    print(f"✅ Database created at {DB_PATH}")

if __name__ == "__main__":
    create_database()