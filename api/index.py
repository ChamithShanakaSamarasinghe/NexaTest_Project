from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
import sqlite3
from pathlib import Path
import numpy as np
import shutil
import os
import sys

# Fixing NUMPY issue
np.float = float

# Path Setup
BASE_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = BASE_PATH / "src"

sys.path.insert(0, str(BASE_PATH))
sys.path.insert(0, str(SRC_PATH))

orc = None

# FASTAPI APP
app = FastAPI(title="NexaTest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = str(BASE_PATH / "db.sqlite3")


# Request Model
class AnalysisRequest(BaseModel):
    doc_id: int = None
    file_path: str = None


# Database
def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Load Helpers
def load_orchestrator():
    global orc
    if orc is None:
        try:
            from app.services.parsing.orchestrator import Orchestrator
            orc = Orchestrator()
        except Exception as e:
            print("Orchestrator disabled:", str(e))
            orc = None


def load_segments():
    try:
        from src.segment_sections import segment_sections
        from src.segment_requirements import extract_requirements
        return segment_sections, extract_requirements
    except Exception as e:
        print("Segment fallback:", str(e))
        return (
            lambda x: {"section": x},
            lambda x: [x]
        )


def safe_run_fpr_pipeline(requirements):
    try:
        from src.fpr.fpr_pipeline import run_fpr_pipeline
        return run_fpr_pipeline(requirements)
    except Exception as e:
        print("FPR disabled:", str(e))
        return {
            "clusters": [],
            "keywords": {},
            "metrics": {}
        }


# Routes

@app.get("/api")
def home():
    return {"message": "NexaTest Backend Running"}


@app.post("/api/full-analysis")
def full_analysis(request: AnalysisRequest):
    try:
        print("FULL ANALYSIS HIT")

        load_orchestrator()
        segment_sections, extract_requirements = load_segments()

        full_text = ""

        if orc and request.file_path:
            result = orc.process(
                job_id="JOB-002",
                file_path=request.file_path
            )
            full_text = result["content"].get("text", "")

        elif request.doc_id:
            reqs = query_db(
                "SELECT requirement_text FROM requirements WHERE document_id=?",
                (request.doc_id,)
            )
            full_text = "\n".join(
                [r["requirement_text"] for r in reqs]
            )

        if not full_text:
            return {
                "sections": {},
                "requirements": [],
                "features": [],
                "test_cases": [],
                "fpr": {
                    "clusters": [],
                    "keywords": {},
                    "metrics": {}
                }
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

        fpr_result = safe_run_fpr_pipeline(requirements)

        return {
            "sections": sections,
            "requirements": requirements,
            "features": features,
            "test_cases": test_cases,
            "fpr": fpr_result
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# File Proccessing

UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/api/process")
async def process(files: list[UploadFile] = File(...)):
    try:
        requirements = []
        features = []
        test_cases = []

        for file in files:
            path = os.path.join(UPLOAD_DIR, file.filename)

            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            text = ""

            if file.filename.endswith(".txt"):
                text = open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ).read()

            elif file.filename.endswith(".docx"):
                from docx import Document
                doc = Document(path)
                text = "\n".join([p.text for p in doc.paragraphs])

            elif file.filename.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(path)
                text = "\n".join(
                    [p.extract_text() or "" for p in reader.pages]
                )

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
        raise HTTPException(status_code=500, detail=str(e))


# Vercel Handler
handler = Mangum(app)