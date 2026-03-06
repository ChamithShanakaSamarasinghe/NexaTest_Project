import sqlite3
import os
from db_config import DB_PATH

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]
    return column in columns

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"⚠️ Database not found at {DB_PATH}. Please initialize it first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Add confidence columns if missing
    if not column_exists(cursor, "requirements", "confidence_score"):
        cursor.execute("ALTER TABLE requirements ADD COLUMN confidence_score REAL")

    if not column_exists(cursor, "requirements", "confidence_band"):
        cursor.execute("ALTER TABLE requirements ADD COLUMN confidence_band TEXT")

    if not column_exists(cursor, "requirements", "confidence_breakdown"):
        cursor.execute("ALTER TABLE requirements ADD COLUMN confidence_breakdown TEXT")

    conn.commit()
    conn.close()

    print("✅ Migration completed: confidence columns added.")

if __name__ == "__main__":
    migrate()