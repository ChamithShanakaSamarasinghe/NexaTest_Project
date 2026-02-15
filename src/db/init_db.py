import sqlite3
import os
from .db_config import DB_PATH


def init_database():
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------------------------------
    # Table 1: SRS Documents
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------------
    # Table 2: SRS Sections
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            section_id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            section_name TEXT NOT NULL,
            section_text TEXT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(document_id)
        )
    """)

    # -------------------------------
    # Table 3: Functional Requirements
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requirements (
            requirement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER NOT NULL,
            requirement_text TEXT NOT NULL,
            FOREIGN KEY (section_id) REFERENCES sections(section_id)
        )
    """)

    # -------------------------------
    # Table 4: Feature Mapping
    # -------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS features (
            feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id INTEGER NOT NULL,
            feature_name TEXT NOT NULL,
            FOREIGN KEY (requirement_id) REFERENCES requirements(requirement_id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ SQLite database initialized successfully.")
    print(f"📁 Database location: {DB_PATH}")


if __name__ == "__main__":
    init_database()
