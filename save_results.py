import sqlite3
import json
import os
from datetime import datetime

# Paths
DB_FILE = "db.sqlite3"
RESULTS_FILE = os.path.join("results", "test_results.json")

#Connecting to DB
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

#Inserting the SRS document
srs_filename = "NexaTest_SRS.docx"  # Update dynamically if needed
cursor.execute("INSERT INTO documents (filename) VALUES (?)", (srs_filename,))
doc_id = cursor.lastrowid  # get the ID to link everything

print(f"SRS document '{srs_filename}' inserted with ID {doc_id}")

#Loading the JSON data
with open(RESULTS_FILE) as f:
    data = json.load(f)

#Inserting sections
for section in data.get("sections", []):
    cursor.execute("""
        INSERT INTO sections (document_id, section_name, content)
        VALUES (?, ?, ?)
    """, (doc_id, section.get("section_name", ""), section.get("content", "")))
print(f"{len(data.get('sections', []))} sections inserted")

#Inserting the requirements
for req in data.get("requirements", []):
    cursor.execute("""
        INSERT INTO requirements (document_id, requirement_text)
        VALUES (?, ?)
    """, (doc_id, req))
print(f"{len(data.get('requirements', []))} requirements inserted")

#Inserting the features
for feat in data.get("features", []):
    cursor.execute("""
        INSERT INTO features (document_id, feature_name)
        VALUES (?, ?)
    """, (doc_id, feat))
print(f"{len(data.get('features', []))} features inserted")

#Inserting the test results
test_results = data.get("test_results", {})
for test_name, status in test_results.items():
    cursor.execute("""
        INSERT INTO test_results (doc_id, test_name, status)
        VALUES (?, ?, ?)
    """, (doc_id, test_name, status))
print(f"{len(test_results)} test results inserted")

#Commit and close
conn.commit()
conn.close()

print("All data saved to database successfully!")
