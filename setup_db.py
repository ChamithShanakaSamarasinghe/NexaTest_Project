# File: setup_db.py
import sqlite3
from pathlib import Path
import json

BASE_PATH = Path(__file__).resolve().parent
DB_FILE = BASE_PATH / "db.sqlite3"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 🔹 Documents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    file_path TEXT
)
""")

# 🔹 Sections table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    section_title TEXT,
    section_text TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

# 🔹 Requirements table
cursor.execute("""
CREATE TABLE IF NOT EXISTS requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    requirement_text TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

# 🔹 Features table
cursor.execute("""
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    feature_name TEXT,
    description TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

# 🔹 Test Results table
cursor.execute("""
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER,
    test_name TEXT,
    status TEXT,
    FOREIGN KEY(doc_id) REFERENCES documents(id)
)
""")

# 🔹 FPR Results table (full schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS fpr_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    feature TEXT,
    priority TEXT,
    risk TEXT,
    clusters TEXT,
    keywords TEXT,
    entities TEXT,
    metrics TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

conn.commit()
conn.close()

print("✅ Database setup complete. All tables are ready!")