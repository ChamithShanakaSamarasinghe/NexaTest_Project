# File: src/fastapi_app.py change to api/fastapi_app.py
from fastapi import FastAPI, HTTPException
import sqlite3
import sys
from pathlib import Path
import json
import numpy as np
from fastapi import UploadFile, File
import shutil
import os


# 🔹 Temporary patch for deprecated np.float (NumPy ≥1.24)
np.float = float  # ✅ Fixes store-fpr Internal Server Error

# 🔥 Importing the Feature Pattern Recognition pipeline
from src.fpr.fpr_pipeline import run_fpr_pipeline

# Setup paths
BASE_PATH = Path(__file__).resolve().parent.parent
SRC_PATH = Path(__file__).resolve().parent

sys.path.insert(0, str(SRC_PATH))
sys.path.insert(0, str(BASE_PATH))

# Cloned repo paths
CLONED_CANDIDATES = [
    BASE_PATH / "Cloned tasks" / "Nexatest",
    BASE_PATH / "cloned_tasks" / "Nexatest",
]

for cand in CLONED_CANDIDATES:
    if cand.exists() and (cand / "app").exists():
        sys.path.insert(0, str(cand))
        break

# Importing orchestrator safely
try:
    from app.services.parsing.orchestrator import Orchestrator
    orc = Orchestrator()
except Exception:
    orc = None  # Fallback if not available

# Local modules
from segment_sections import segment_sections
from segment_requirements import extract_requirements

# ✅ DB path
DB_FILE = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

app = FastAPI(title="🚀 SRS Automation API")

# 🔧 Utility DB functions
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

# 🔧 Convert keys/values to JSON-safe
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

# 📂 DB Endpoints
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

# 🧠 SRS Processing
@app.post("/process-srs")
def process_srs(file_path: str = None, doc_id: int = None):
    try:
        if file_path:
            file_path = file_path.strip('"')
        if orc:
            result = orc.process(job_id="JOB-001", file_path=file_path)
        else:
            if not doc_id:
                raise HTTPException(400, "Provide doc_id since Orchestrator is missing")
            reqs = query_db("SELECT requirement_text FROM requirements WHERE document_id=?", (doc_id,))
            result = {
                "enrichment": {"summary": "", "features": {"keywords": [], "entities": []}},
                "content": {"text": "\n".join([r["requirement_text"] for r in reqs])},
                "parsing_method": "orchestrator_missing"
            }
        return {
            "summary": result["enrichment"].get("summary", ""),
            "keywords": result["enrichment"]["features"].get("keywords", []),
            "entities": result["enrichment"]["features"].get("entities", []),
            "parsing_method": result.get("parsing_method", "")
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/full-analysis")
def full_analysis(file_path: str = None, doc_id: int = None):
    try:
        if file_path:
            file_path = file_path.strip('"')
        if orc:
            result = orc.process(job_id="JOB-002", file_path=file_path)
            full_text = result["content"].get("text", "")
            summary = result["enrichment"].get("summary", "")
            keywords = result["enrichment"]["features"].get("keywords", [])
            entities = result["enrichment"]["features"].get("entities", [])
            parsing_method = result.get("parsing_method", "")
        else:
            if not doc_id:
                raise HTTPException(400, "Provide doc_id since Orchestrator is missing")
            reqs = query_db("SELECT requirement_text FROM requirements WHERE document_id=?", (doc_id,))
            full_text = "\n".join([r["requirement_text"] for r in reqs])
            summary, keywords, entities, parsing_method = "", [], [], "orchestrator_missing"

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
            "summary": summary,
            "keywords": keywords,
            "entities": entities,
            "sections": sections,
            "requirements": requirements,
            "fpr": fpr_result,
            "parsing_method": parsing_method
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# 💾 Store FPR safely
@app.post("/store-fpr/{doc_id}")
def store_fpr(doc_id: int):
    try:
        reqs = query_db("SELECT requirement_text FROM requirements WHERE document_id=?", (doc_id,))
        if not reqs:
            raise HTTPException(404, "No requirements found")
        texts = [r["requirement_text"] for r in reqs]

        res = run_fpr_pipeline(texts)
        fpr_result = {
            "clusters": res.get("clusters", []),
            "keywords": convert_json_safe(res.get("keywords", {})),
            "metrics": convert_json_safe(res.get("metrics", {}))
        }

        execute_db(
            "INSERT INTO fpr_results (document_id, clusters, keywords, metrics) VALUES (?, ?, ?, ?)",
            (
                doc_id,
                json.dumps(fpr_result["clusters"]),
                json.dumps(fpr_result["keywords"]),
                json.dumps(fpr_result["metrics"])
            ),
        )

        return {"message": "FPR stored successfully", "fpr": fpr_result}
    except Exception as e:
        raise HTTPException(500, f"store_fpr failed: {str(e)}")
    
    # ================================
# 🚀 FRONTEND FILE UPLOAD ENDPOINT
# ================================

UPLOAD_DIR = "/tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/process")
async def process(files: list[UploadFile] = File(...)):
    try:
        requirements = []
        features = []
        test_cases = []

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            extracted_text = ""

            # -----------------------------
            # 📄 TEXT FILE
            # -----------------------------
            if file.filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()

            # -----------------------------
            # 📄 DOCX FILE
            # -----------------------------
            elif file.filename.endswith(".docx"):
                from docx import Document
                doc = Document(file_path)
                extracted_text = "\n".join([p.text for p in doc.paragraphs])

            # -----------------------------
            # 📄 PDF FILE
            # -----------------------------
            elif file.filename.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(file_path)
                extracted_text = "\n".join(
                    [page.extract_text() or "" for page in reader.pages]
                )

            # -----------------------------
            # 🎤 AUDIO / VIDEO (placeholder for Whisper)
            # -----------------------------
            elif file.filename.endswith((".mp3", ".wav", ".mp4")):
                extracted_text = f"Audio/Video processed: {file.filename}"

            # -----------------------------
            # 🖼 IMAGE (placeholder OCR)
            # -----------------------------
            elif file.filename.endswith((".png", ".jpg", ".jpeg")):
                extracted_text = f"Image processed: {file.filename}"

            else:
                extracted_text = f"Unsupported file: {file.filename}"

            # -----------------------------
            # 🧠 SIMPLE EXTRACTION LOGIC
            # (reuses your existing idea)
            # -----------------------------
            sentences = extracted_text.split(".")

            for s in sentences:
                s = s.strip()

                if len(s) > 10:
                    if any(w in s.lower() for w in ["shall", "must", "should"]):
                        requirements.append(s)

                    if any(w in s.lower() for w in ["system", "feature", "module"]):
                        features.append(s)

        # -----------------------------
        # 🧠 RUN YOUR EXISTING FPR PIPELINE
        # -----------------------------
        fpr_result = {"clusters": [], "keywords": {}, "metrics": {}}

        if requirements:
            res = run_fpr_pipeline(requirements)
            fpr_result = {
                "clusters": res.get("clusters", []),
                "keywords": convert_json_safe(res.get("keywords", {})),
                "metrics": convert_json_safe(res.get("metrics", {}))
            }

        # -----------------------------
        # 🧪 TEST CASES (TEMP GENERATION)
        # -----------------------------
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
        raise HTTPException(status_code=500, detail=str(e))
    
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)