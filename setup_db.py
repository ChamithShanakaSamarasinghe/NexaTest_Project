import sqlite3
import os

DB_FILE = "db.sqlite3"

# Create DB if it doesn't exist
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    section_name TEXT,
    content TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    requirement_text TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    feature_name TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id INTEGER,
    test_name TEXT,
    status TEXT,
    FOREIGN KEY(doc_id) REFERENCES documents(id)
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")
