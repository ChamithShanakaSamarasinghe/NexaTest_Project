# File: api/index.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sqlite3
import sys
from pathlib import Path
import json
import numpy as np
import shutil
import os

# Fixing numpy issue
np.float = float

# PATH SETUP (FIXED)
BASE_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = BASE_PATH / "src"

sys.path.insert(0, str(BASE_PATH))
sys.path.insert(0, str(SRC_PATH))


# SAFE IMPORTS (FIXED)
try:
    from src.fpr.fpr_pipeline import run_fpr_pipeline
except:
    from fpr.fpr_pipeline import run_fpr_pipeline

try:
    from segment_sections import segment_sections
    from segment_requirements import extract_requirements
except:
    from src.segment_sections import segment_sections
    from src.segment_requirements import extract_requirements

# OPTIONAL ORCHESTRATOR
try:
    from app.services.parsing.orchestrator import Orchestrator
    orc = Orchestrator()
except Exception:
    orc = None

# DATABASE (FIXED)
DB_FILE = str(BASE_PATH / "db.sqlite3")

# FASTAPI APP
app = FastAPI(title="🚀 SRS Automation API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB UTILS
def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def execute_db(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def convert_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): convert_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_json_safe(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    else:
        return obj

# DB ENDPOINTS
@app.get("/documents")
def get_documents():
    return {"documents": query_db("SELECT * FROM documents")}

@app.get("/documents/{doc_id}/sections")
def get_sections(doc_id: int):
    data = query_db("SELECT * FROM sections WHERE document_id=?", (doc_id,))
    if not data:
        raise HTTPException(404, "Sections not found")
    return {"sections": data}

@app.get("/documents/{doc_id}/requirements")
def get_requirements_db(doc_id: int):
    data = query_db("SELECT * FROM requirements WHERE document_id=?", (doc_id,))
    if not data:
        raise HTTPException(404, "Requirements not found")
    return {"requirements": data}

@app.get("/documents/{doc_id}/features")
def get_features(doc_id: int):
    data = query_db("SELECT * FROM features WHERE document_id=?", (doc_id,))
    if not data:
        raise HTTPException(404, "Features not found")
    return {"features": data}

@app.get("/documents/{doc_id}/test-results")
def get_test_results(doc_id: int):
    data = query_db("SELECT * FROM test_results WHERE doc_id=?", (doc_id,))
    if not data:
        raise HTTPException(404, "Test results not found")
    return {"test_results": data}

@app.get("/documents/{doc_id}/fpr")
def get_fpr_results(doc_id: int):
    data = query_db("SELECT * FROM fpr_results WHERE document_id=?", (doc_id,))
    if not data:
        raise HTTPException(404, "FPR results not found")
    for row in data:
        row["clusters"] = json.loads(row.get("clusters") or "[]")
        row["keywords"] = json.loads(row.get("keywords") or "{}")
        row["metrics"] = json.loads(row.get("metrics") or "{}")
    return {"fpr_results": data}

@app.get("/analytics/{doc_id}")
def get_analytics(doc_id: int):
    results = query_db("SELECT * FROM test_results WHERE doc_id=?", (doc_id,))
    total = len(results)
    passed = len([r for r in results if r["status"] == "PASSED"])
    failed = total - passed
    return {"total_tests": total, "passed": passed, "failed": failed}

# FULL ANALYSIS
@app.post("/full-analysis")
def full_analysis(file_path: str = None, doc_id: int = None):
    try:
        if file_path:
            file_path = file_path.strip('"')

        if orc:
            result = orc.process(job_id="JOB-002", file_path=file_path)
            full_text = result["content"].get("text", "")
        else:
            if not doc_id:
                raise HTTPException(400, "Provide doc_id")
            reqs = query_db("SELECT requirement_text FROM requirements WHERE document_id=?", (doc_id,))
            full_text = "\n".join([r["requirement_text"] for r in reqs])

        sections = segment_sections(full_text)

        requirements = []
        for sec_text in sections.values():
            requirements.extend(extract_requirements(sec_text))

        fpr_result = {"clusters": [], "keywords": {}, "metrics": {}}

        if requirements:
            res = run_fpr_pipeline(requirements)
            fpr_result = {
                "clusters": res.get("clusters", []),
                "keywords": convert_json_safe(res.get("keywords", {})),
                "metrics": convert_json_safe(res.get("metrics", {}))
            }

        return {
            "sections": sections,
            "requirements": requirements,
            "fpr": fpr_result
        }

    except Exception as e:
        print("❌ FULL ANALYSIS ERROR:", str(e))
        raise HTTPException(500, str(e))

# FILE UPLOAD API (FIXED + DEBUG)
UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process(files: list[UploadFile] = File(...)):
    try:
        print("🔥 API HIT /process")

        requirements = []
        features = []
        test_cases = []

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            extracted_text = ""

            if file.filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()

            elif file.filename.endswith(".docx"):
                from docx import Document
                doc = Document(file_path)
                extracted_text = "\n".join([p.text for p in doc.paragraphs])

            elif file.filename.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(file_path)
                extracted_text = "\n".join([p.extract_text() or "" for p in reader.pages])

            elif file.filename.endswith((".mp3", ".wav", ".mp4")):
                extracted_text = f"Audio processed: {file.filename}"

            elif file.filename.endswith((".png", ".jpg", ".jpeg")):
                extracted_text = f"Image processed: {file.filename}"

            else:
                extracted_text = f"Unsupported file: {file.filename}"

            sentences = extracted_text.split(".")

            for s in sentences:
                s = s.strip()
                if len(s) > 10:
                    if any(w in s.lower() for w in ["shall", "must", "should"]):
                        requirements.append(s)

                    if any(w in s.lower() for w in ["system", "feature", "module"]):
                        features.append(s)

        fpr_result = {"clusters": [], "keywords": {}, "metrics": {}}

        if requirements:
            res = run_fpr_pipeline(requirements)
            fpr_result = {
                "clusters": res.get("clusters", []),
                "keywords": convert_json_safe(res.get("keywords", {})),
                "metrics": convert_json_safe(res.get("metrics", {}))
            }

        for i, req in enumerate(requirements[:5]):
            test_cases.append({
                "id": f"TC-{i+1}",
                "requirement": req,
                "expected": "System should handle requirement correctly"
            })

        return {
            "requirements": requirements,
            "features": features,
            "clusters": fpr_result.get("clusters", []),
            "test_cases": test_cases,
            "fpr": fpr_result
        }

    except Exception as e:
        print("❌ PROCESS ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# REQUIRED for Vercel FastAPI detection
handler = Mangum(app)