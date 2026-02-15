import sqlite3
import os
import json

ANALYSIS_DIR = "analysis"
os.makedirs(ANALYSIS_DIR, exist_ok=True)

DB_FILE = "db.sqlite3"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

analysis = {}

# Fetching the documents
cursor.execute("SELECT id, filename FROM documents")
documents = cursor.fetchall()
analysis["documents"] = [{"id": doc[0], "filename": doc[1]} for doc in documents]

# Fetching the requirements
cursor.execute("SELECT document_id, requirement_text FROM requirements")
requirements = cursor.fetchall()
analysis["requirements"] = [{"document_id": r[0], "requirement": r[1]} for r in requirements]

# Fetching the features
cursor.execute("SELECT document_id, feature_name FROM features")
features = cursor.fetchall()
analysis["features"] = [{"document_id": f[0], "feature": f[1]} for f in features]

conn.close()

# Saving the analysis
with open(os.path.join(ANALYSIS_DIR, "analysis_summary.json"), "w") as f:
    json.dump(analysis, f, indent=4)

print("Analysis saved to analysis/analysis_summary.json")
