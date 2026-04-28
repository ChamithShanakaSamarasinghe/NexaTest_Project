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

# FIX NUMPY ISSUE
np.float = float

# Path Setup
BASE_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = BASE_PATH / "src"

sys.path.insert(0, str(BASE_PATH))
sys.path.insert(0, str(SRC_PATH))

# SAFE IMPORT FLAGS (IMPORTANT FIX)
run_fpr_pipeline = None
segment_sections = None
extract_requirements = None
orc = None

# Lazy load functions ONLY when needed
def load_fpr():
    global run_fpr_pipeline
    if run_fpr_pipeline is None:
        try:
            from src.fpr.fpr_pipeline import run_fpr_pipeline as _run
            run_fpr_pipeline = _run
        except:
            run_fpr_pipeline = None

def load_segments():
    global segment_sections, extract_requirements
    if segment_sections is None or extract_requirements is None:
        try:
            from src.segment_sections import segment_sections as ss
            from src.segment_requirements import extract_requirements as er
            segment_sections = ss
            extract_requirements = er
        except:
            segment_sections = lambda x: {"section": x}
            extract_requirements = lambda x: [x]

def load_orchestrator():
    global orc
    if orc is None:
        try:
            from app.services.parsing.orchestrator import Orchestrator
            orc = Orchestrator()
        except:
            orc = None

# DATABASE
DB_FILE = str(BASE_PATH / "db.sqlite3")

# FASTAPI APP
app = FastAPI(title="🚀 SRS Automation API")

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
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def convert_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): convert_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_json_safe(i) for i in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return obj

# Root
@app.get("/")
def home():
    return {"message": "✅ NexaTest Backend Running"}

# Full Service
@app.post("/full-analysis")
def full_analysis(file_path: str = None, doc_id: int = None):
    try:
        print("🔥 FULL ANALYSIS HIT")

        load_orchestrator()
        load_segments()

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
            return {
                "sections": {},
                "requirements": [],
                "features": [],
                "test_cases": [],
                "fpr": {"clusters": [], "keywords": {}, "metrics": {}}
            }

        sections = segment_sections(full_text)
        requirements = []

        for sec in sections.values():
            requirements.extend(extract_requirements(sec))

        features = [
            r for r in requirements
            if any(w in r.lower() for w in ["system", "feature", "module"])
        ]

        test_cases = [
            {
                "id": f"TC-{i+1}",
                "requirement": r,
                "expected": "System should handle requirement correctly"
            }
            for i, r in enumerate(requirements[:5])
        ]

        # SAFE FPR
        fpr_result = {
            "clusters": [],
            "keywords": {},
            "metrics": {}
        }

        load_fpr()

        if run_fpr_pipeline and requirements:
            try:
                res = run_fpr_pipeline(requirements)
                fpr_result = {
                    "clusters": res.get("clusters", []),
                    "keywords": convert_json_safe(res.get("keywords", {})),
                    "metrics": convert_json_safe(res.get("metrics", {}))
                }
            except Exception as e:
                print("⚠️ FPR FAILED:", str(e))

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

# FILE UPLOAD
UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process(files: list[UploadFile] = File(...)):
    try:
        requirements, features, test_cases = [], [], []

        for file in files:
            path = os.path.join(UPLOAD_DIR, file.filename)

            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            text = ""

            if file.filename.endswith(".txt"):
                text = open(path, "r", encoding="utf-8", errors="ignore").read()

            elif file.filename.endswith(".docx"):
                from docx import Document
                doc = Document(path)
                text = "\n".join([p.text for p in doc.paragraphs])

            elif file.filename.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(path)
                text = "\n".join([p.extract_text() or "" for p in reader.pages])

            for s in text.split("."):
                s = s.strip()
                if len(s) > 10:
                    if any(w in s.lower() for w in ["shall", "must", "should"]):
                        requirements.append(s)
                    if any(w in s.lower() for w in ["system", "feature", "module"]):
                        features.append(s)

        for i, r in enumerate(requirements[:5]):
            test_cases.append({
                "id": f"TC-{i+1}",
                "requirement": r,
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