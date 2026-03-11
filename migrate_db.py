import sqlite3
import os

DB_PATH = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Checking columns
cursor.execute("PRAGMA table_info(fpr_results)")
columns = [col[1] for col in cursor.fetchall()]

if "metrics" not in columns:
    print("Adding 'metrics' column...")
    cursor.execute("ALTER TABLE fpr_results ADD COLUMN metrics TEXT DEFAULT '{}'")

else:
    print("metrics column already exists")

# Showing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:", tables)

conn.commit()
conn.close()

print("Migration complete")