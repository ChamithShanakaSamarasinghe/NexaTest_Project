import sqlite3

DB_PATH = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if column exists
cursor.execute("PRAGMA table_info(requirements)")
columns = [col[1] for col in cursor.fetchall()]

if "fpr_id" not in columns:
    cursor.execute("ALTER TABLE requirements ADD COLUMN fpr_id INTEGER")
    print("Added 'fpr_id' column to requirements ✅")
else:
    print("'fpr_id' column already exists.")

conn.commit()
conn.close()