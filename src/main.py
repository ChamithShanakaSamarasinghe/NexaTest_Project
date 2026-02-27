from fastapi import FastAPI, UploadFile, File
import shutil
import os

from src.extract_text import extract_text_from_pdf
from src.segment_sections import segment_sections
from src.segment_requirements import extract_requirements

# Import enhancer
from src.enhancer import PipelineEnhancer

# NEW: Importing FPR pipeline
from src.fpr.fpr_pipeline import run_fpr_pipeline

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded files (doc_id -> file_path)
DOCS = {}
NEXT_DOC_ID = 1

# Initialize enhancer once
enhancer = PipelineEnhancer()


@app.get("/")
def root():
    return {"status": "NexaTest API running"}


# Upload SRS
@app.post("/upload-srs")
def upload_srs(file: UploadFile = File(...)):
    global NEXT_DOC_ID

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc_id = NEXT_DOC_ID
    NEXT_DOC_ID += 1

    # Save mapping
    DOCS[doc_id] = file_path

    return {
        "message": "SRS uploaded",
        "filename": file.filename,
        "doc_id": doc_id
    }


# Requirements (dummy for testing)
@app.get("/requirements/{doc_id}")
def get_requirements(doc_id: int):
    return {
        "id": doc_id,
        "doc_id": doc_id,
        "requirements": [
            "System shall allow login",
            "System shall generate reports"
        ]
    }


# Extract Requirements WITH Enhancer + FPR 🔥
@app.post("/extract-requirements/{doc_id}")
def extract_req_api(doc_id: int):
    file_path = DOCS.get(doc_id)

    if not file_path or not os.path.exists(file_path):
        return {"error": "File not found for this doc_id"}

    # Extract raw text
    raw_text = extract_text_from_pdf(file_path)

    # Run enhancer pipeline
    enhanced = enhancer.enhance(raw_text)
    clean_text = enhanced["clean_text"]

    # Segment sections
    sections = segment_sections(clean_text)

    # Extract requirements
    requirements = extract_requirements(clean_text)

    # RUN FEATURE PATTERN RECOGNITION
    fpr_result = run_fpr_pipeline(requirements)

    return {
        "doc_id": doc_id,
        "requirements": requirements,
        "clean_text": clean_text,
        "sections": sections,

        # NEW OUTPUTS
        "fpr_clusters": fpr_result["clusters"],
        "fpr_keywords": fpr_result["keywords"],
        "fpr_metrics": fpr_result["metrics"]
    }


# Generate Test Cases
@app.post("/generate-tests/{doc_id}")
def generate_tests(doc_id: int):
    return {
        "doc_id": doc_id,
        "testcases": [
            {
                "id": "TC-01",
                "title": "Login test",
                "steps": ["Open login page", "Enter credentials", "Submit"],
                "expected": "User logged in"
            }
        ]
    }