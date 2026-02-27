# SRS Automation Project

This project automates the extraction, analysis, and storage of **Software Requirements Specification (SRS)** documents. It combines a **Streamlit interface** for uploading SRS files with a **FastAPI backend** for querying structured data, powered by **AI/ML models** for keyword extraction, entity recognition, summarization, and feature-priority-risk (FPR) analysis. All data is stored in **SQLite**.

---

## Features

### 1. **Streamlit App (`srs_app.py`)**

* Upload any `.docx` SRS document.
* Automatically extracts:

  * Sections
  * Requirements
  * Features
* Performs **AI-powered analysis**:

  * Keyword extraction using **KeyBERT**
  * Entity recognition
  * Document summarization using **DistilBART**
* Saves all extracted data to SQLite (`db.sqlite3`) and triggers FPR analysis.

### 2. **FastAPI App (`fastapi_app.py`)**

* Provides robust **API endpoints** for programmatic access:

  * `/documents` – List all uploaded documents
  * `/documents/{doc_id}/sections` – Get sections for a document
  * `/documents/{doc_id}/requirements` – Get extracted requirements
  * `/documents/{doc_id}/features` – Get features
  * `/documents/{doc_id}/test-results` – Get automated test results
  * `/documents/{doc_id}/fpr` – Get Feature-Priority-Risk (FPR) results including clusters, keywords, entities, and metrics
  * `/analytics/{doc_id}` – Summary of test results (total, passed, failed)
  * `/process-srs` – Process a new SRS file programmatically
  * `/full-analysis` – Returns summary, keywords, entities, and parsed sections
  * `/store-fpr/{doc_id}` – Store FPR clustering results into the database
* **Swagger UI** available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. **SQLite Database**

* Stores all documents, sections, requirements, features, test results, and FPR data.
* Automatically updated when a new SRS is uploaded via Streamlit or processed via the API.

### 4. **AI/ML Enhancements**

* **Keyword Extraction** using KeyBERT (`all-MiniLM-L6-v2`)
* **Summarization** with `sshleifer/distilbart-cnn-12-6`
* **Entity Recognition** with spaCy/NLP pipeline
* **FPR Analysis**:

  * Clusters related features and requirements
  * Assigns **priority** (High, Medium, Low)
  * Identifies potential **risks** (Security, Performance, etc.)
  * Generates **metrics** like silhouette score for cluster quality

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd SRS-NexaTest
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Run the Streamlit App

```bash
streamlit run src\srs_app.py
```

* Upload SRS `.docx` files
* Extracted sections, requirements, features, and FPR analysis are **automatically saved** to `db.sqlite3`.

### 2. Run the FastAPI App

```bash
python -m uvicorn src.fastapi_app:app --reload
```

* Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Programmatically query documents, sections, requirements, features, test results, analytics, and perform full analysis.

---


## Notes

* Ensure `srs_docs/` exists for uploads.
* Streamlit uploads automatically update the database, which is served by FastAPI.
* Use [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore and test API endpoints.
* Python **3.13+** recommended.
* Works on **Windows, macOS, and Linux**.

---

## Author

**Chamith Shanaka Samarasinghe**
AI/ML & Data Science Intern
