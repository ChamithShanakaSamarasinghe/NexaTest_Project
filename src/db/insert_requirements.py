import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "db.sqlite3")
INPUT_FILE = "data/output/atomic_requirements.txt"
SECTION_ID = 3  # Functional Requirements section ID


def insert_requirements():
    """Insert raw functional requirements from a file into the database."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Atomic requirements file not found at {INPUT_FILE}")

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


def insert_confidence_result(requirement_id: int, final_score: float, band: str, breakdown: dict):
    """
    Insert confidence scores into the requirements table.

    :param requirement_id: ID of the requirement
    :param final_score: Final confidence score
    :param band: Confidence band (Low / Medium / High)
    :param breakdown: Dictionary of individual scores
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requirements
        SET confidence_score = ?,
            confidence_band = ?,
            confidence_breakdown = ?
        WHERE id = ?
    """, (
        final_score,
        band,
        json.dumps(breakdown),
        requirement_id
    ))

    conn.commit()
    conn.close()

    print(f"✅ Confidence updated for requirement ID {requirement_id}")