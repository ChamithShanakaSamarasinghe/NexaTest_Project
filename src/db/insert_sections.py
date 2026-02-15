import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../data/srs.db")

SECTIONS_FILE = os.path.join(BASE_DIR, "../../data/output/segmented_sections.txt")

def insert_sections(document_id):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found.")

    if not os.path.exists(SECTIONS_FILE):
        raise FileNotFoundError("Segmented sections file not found.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SECTIONS_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    sections = content.split("==========")
    
    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.splitlines()
        section_name = lines[0].strip()
        section_text = "\n".join(lines[1:]).strip()

        cursor.execute(
            """
            INSERT INTO sections (document_id, section_name, section_text)
            VALUES (?, ?, ?)
            """,
            (document_id, section_name, section_text)
        )

    conn.commit()
    conn.close()

    print("SRS sections inserted successfully into database.")


if __name__ == "__main__":
    insert_sections(document_id=1)
