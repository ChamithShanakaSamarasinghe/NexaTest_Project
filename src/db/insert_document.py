import sqlite3
import os
from .db_config import DB_PATH


def insert_document(file_name):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. Run init_db.py first."
        )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents (file_name) VALUES (?)",
        (file_name,)
    )

    conn.commit()
    document_id = cursor.lastrowid
    conn.close()

    print("Document inserted successfully.")
    print(f"Document ID: {document_id}")
    print(f"File Name: {file_name}")

    return document_id
