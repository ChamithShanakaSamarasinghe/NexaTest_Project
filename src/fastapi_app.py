# File: src/fastapi_app.py
from fastapi import FastAPI, HTTPException
import sqlite3

DB_FILE = "db.sqlite3"

app = FastAPI(title="SRS Automation API")

# --- Utility function ---
def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

# --- Endpoints ---

@app.get("/documents")
def get_documents():
    docs = query_db("SELECT * FROM documents")
    return {"documents": docs}

@app.get("/documents/{doc_id}/sections")
def get_sections(doc_id: int):
    sections = query_db("SELECT * FROM sections WHERE document_id=?", (doc_id,))
    if not sections:
        raise HTTPException(status_code=404, detail="Sections not found")
    return {"sections": sections}

@app.get("/documents/{doc_id}/requirements")
def get_requirements(doc_id: int):
    reqs = query_db("SELECT * FROM requirements WHERE document_id=?", (doc_id,))
    if not reqs:
        raise HTTPException(status_code=404, detail="Requirements not found")
    return {"requirements": reqs}

@app.get("/documents/{doc_id}/features")
def get_features(doc_id: int):
    feats = query_db("SELECT * FROM features WHERE document_id=?", (doc_id,))
    if not feats:
        raise HTTPException(status_code=404, detail="Features not found")
    return {"features": feats}

@app.get("/documents/{doc_id}/test-results")
def get_test_results(doc_id: int):
    results = query_db("SELECT * FROM test_results WHERE doc_id=?", (doc_id,))
    if not results:
        raise HTTPException(status_code=404, detail="Test results not found")
    return {"test_results": results}

# --- Optional: Analytics endpoint ---
@app.get("/analytics/{doc_id}")
def get_analytics(doc_id: int):
    results = query_db("SELECT * FROM test_results WHERE doc_id=?", (doc_id,))
    total = len(results)
    passed = len([r for r in results if r["status"] == "PASSED"])
    failed = len([r for r in results if r["status"] != "PASSED"])
    return {"total_tests": total, "passed": passed, "failed": failed}