# SRS Automation Project

This project automates the extraction, storage, and analysis of Software Requirements Specification (SRS) documents. It provides a **Streamlit interface** to upload SRS files, stores extracted data in **SQLite**, and exposes a **FastAPI** backend to query sections, requirements, features, and test results.

---

## Features

1. **Streamlit App (`srs_app.py`)**
   - Upload any `.docx` SRS document.
   - Automatically extracts:
     - Sections
     - Requirements
     - Features
   - Saves data to SQLite database (`db.sqlite3`).

2. **FastAPI App (`fastapi_app.py`)**
   - Provides API endpoints to access:
     - `/documents` – List all uploaded documents
     - `/documents/{doc_id}/sections` – Get sections for a document
     - `/documents/{doc_id}/requirements` – Get requirements
     - `/documents/{doc_id}/features` – Get features
     - `/documents/{doc_id}/test-results` – Get test results
     - `/analytics/{doc_id}` – Test results summary (total, passed, failed)
   - Swagger UI available at `http://127.0.0.1:8000/docs`.

3. **SQLite Database**
   - Stores documents, sections, requirements, features, and test results.
   - Automatically updated when a new SRS is uploaded via Streamlit.

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd SRS-NexaTest

Create and activate a virtual environment:
 python -m venv venv
 venv\Scripts\activate      # Windows
 # source venv/bin/activate  # macOS/Linux

Install dependencies:
pip install -r requirements.txt

Usage
1. Run the Streamlit App
streamlit run src\srs_app.py

Upload SRS .docx files.

Extracted data is stored in db.sqlite3.

2. Run the FastAPI App
python -m uvicorn src.fastapi_app:app --reload

    Open Swagger UI at http://127.0.0.1:8000/docs.
    Query documents, sections, requirements, features, test results, and analytics.

# Folder Structure
Folder Structure
SRS-NexaTest/
│
├─ src/
│   ├─ srs_app.py          # Streamlit app
│   ├─ fastapi_app.py      # FastAPI app
│   └─ extract_srs_data.py # Extract sections, requirements, features from SRS
│
├─ srs_docs/               # Upload folder for SRS documents
├─ results/                # Test results JSON
├─ db.sqlite3              # SQLite database
├─ save_results.py         # Insert test results into DB
├─ setup_db.py             # Create DB and tables
├─ requirements.txt        # Python dependencies
└─ README.md               # Project documentation

Notes
#Make sure srs_docs/ folder exists for uploads.
#Streamlit uploads automatically update the database, which is then served by FastAPI.
#Use http://127.0.0.1:8000/docs to explore and test the API endpoints.
#Python 3.13+ recommended.

Task done by
Chamith Shanaka Samarasinghe
AI/ML & Data Science Intern
