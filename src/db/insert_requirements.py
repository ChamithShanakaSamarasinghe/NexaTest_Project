import sqlite3
import os

DB_PATH = "data/srs.db"
INPUT_FILE = "data/output/atomic_requirements.txt"
SECTION_ID = 3  # Functional Requirements section ID

def insert_requirements():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found.")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError("Atomic requirements file not found.")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        # Remove "1. ", "2. " etc.
        requirements = [line.strip().split(". ", 1)[1] for line in f if ". " in line]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for req in requirements:
        cursor.execute(
            """
            INSERT INTO requirements (section_id, requirement_text)
            VALUES (?, ?)
            """,
            (SECTION_ID, req)
        )

    conn.commit()
    conn.close()

    print(f"[DONE] Inserted {len(requirements)} requirements into database")


if __name__ == "__main__":
    insert_requirements()
