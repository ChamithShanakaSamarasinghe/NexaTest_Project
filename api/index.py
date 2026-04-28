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

# Fix numpy issue
np.float = float

# PATH SETUP
BASE_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = BASE_PATH / "src"

sys.path.insert(0, str(BASE_PATH))
sys.path.insert(0, str(SRC_PATH))

# SAFE IMPORTS
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

# DATABASE
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

def convert_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): convert_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_json_safe(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    return obj

# ROOT
@app.get("/")
def home():
    return {"message": "✅ NexaTest Backend Running"}

# FULL ANALYSIS
@app.post("/full-analysis")
def full_analysis(file_path: str = None, doc_id: int = None):
    try:
        # GET TEXT
        full_text = ""

        if orc and file_path:
            result = orc.process(job_id="JOB-002", file_path=file_path)
            full_text = result["content"].get("text", "")

        elif doc_id:
            reqs = query_db(
                "SELECT requirement_text FROM requirements WHERE document_id=?",
                (doc_id,)
            )
            full_text = "\n".join([r["requirement_text"] for r in reqs])

        if not full_text:
            raise HTTPException(400, "No text found for processing")

        # SECTIONS
        sections = segment_sections(full_text)

        # REQUIREMENTS
        requirements = []
        for sec_text in sections.values():
            requirements.extend(extract_requirements(sec_text))

        # FEATURES
        features = [
            r for r in requirements
            if any(word in r.lower() for word in ["system", "feature", "module"])
        ]

        # TEST CASES
        test_cases = [
            {
                "id": f"TC-{i+1}",
                "requirement": req,
                "expected": "System should handle requirement correctly"
            }
            for i, req in enumerate(requirements[:5])
        ]

        # FPR PIPELINE
        fpr_result = {"clusters": [], "keywords": {}, "metrics": {}}

        if requirements:
            res = run_fpr_pipeline(requirements)
            fpr_result = {
                "clusters": res.get("clusters", []),
                "keywords": convert_json_safe(res.get("keywords", {})),
                "metrics": convert_json_safe(res.get("metrics", {}))
            }

        # FINAL RESPONSE
        return {
            "sections": sections,
            "requirements": requirements,
            "features": features,
            "test_cases": test_cases,
            "fpr": fpr_result
        }

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(500, str(e))

# FILE UPLOAD API 
UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process(files: list[UploadFile] = File(...)):
    try:
        requirements, features, test_cases = [], [], []

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            extracted_text = ""

            if file.filename.endswith(".txt"):
                extracted_text = open(file_path, "r", encoding="utf-8", errors="ignore").read()

            elif file.filename.endswith(".docx"):
                from docx import Document
                doc = Document(file_path)
                extracted_text = "\n".join([p.text for p in doc.paragraphs])

            elif file.filename.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(file_path)
                extracted_text = "\n".join([p.extract_text() or "" for p in reader.pages])

            sentences = extracted_text.split(".")

            for s in sentences:
                s = s.strip()
                if len(s) > 10:
                    if any(w in s.lower() for w in ["shall", "must", "should"]):
                        requirements.append(s)
                    if any(w in s.lower() for w in ["system", "feature", "module"]):
                        features.append(s)

        for i, req in enumerate(requirements[:5]):
            test_cases.append({
                "id": f"TC-{i+1}",
                "requirement": req,
                "expected": "System should handle requirement correctly"
            })

        return {
            "requirements": requirements,
            "features": features,
            "test_cases": test_cases
        }

    except Exception as e:
        raise HTTPException(500, str(e))

# VERCEL HANDLER
handler = Mangum(app)