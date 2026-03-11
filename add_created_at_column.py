import sqlite3

DB_PATH = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if column exists
cursor.execute("PRAGMA table_info(fpr_results)")
columns = [col[1] for col in cursor.fetchall()]

if "created_at" not in columns:
    cursor.execute("ALTER TABLE fpr_results ADD COLUMN created_at TEXT")
    print("Added 'created_at' column to fpr_results ✅")
else:
    print("'created_at' column already exists.")

conn.commit()
conn.close()