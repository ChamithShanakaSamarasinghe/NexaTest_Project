import sqlite3
import os

DB_PATH = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add metrics column to fpr_results if missing
cursor.execute("PRAGMA table_info(fpr_results)")
columns = [col[1] for col in cursor.fetchall()]
if "metrics" not in columns:
    print("Adding 'metrics' column to fpr_results table...")
    cursor.execute("ALTER TABLE fpr_results ADD COLUMN metrics TEXT DEFAULT '{}'")
else:
    print("'metrics' column already exists.")

# Optional: print existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in DB:", tables)

conn.commit()
conn.close()
print("Migration complete ✅")