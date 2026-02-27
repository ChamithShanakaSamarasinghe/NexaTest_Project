# Universal Document Ingestion & Enrichment Pipeline (Nexatest)

This project is a modular, high-performance document ingestion service built with **FastAPI**. It parses diverse file formats (PDF, DOCX, Images), enriches them with AI (Summarization, Keywords, Entity Extraction), and stores structured data in a **PostgreSQL** database for scalable querying and RAG applications.

---

## 🚀 Key Features

* **Universal Ingestion**: Accepts PDF (Digital & Scanned), DOCX, and Images.
* **Database Storage**: Stores Documents, Chunks, Tables, and Entities in **PostgreSQL** (via SQLModel).
* **Intelligent Parsing**: "Docling-First" strategy with OCR fallbacks.
* **AI Enrichment**:
  * **Summarization**: Transformer-based (DistilBART).
  * **Keywords**: Semantic extraction (KeyBERT).
  * **Entities**: Named Entity Recognition with counts (spaCy).
* **Ready for RAG**: Text is automatically chunked and hashed (SHA256) for deduplication.

---

## 🛠 Database Schema

We use a robust relational schema:

* **`Document`**: Metadata (Filename, SHA256, Size).
* **`DocumentChunk`**: Text split into paragraphs (for Search/RAG).
* **`DocumentImage`**: Extracted image paths & captions.
* **`DocumentTable`**: Structured table data (JSON).
* **`DocumentEntity`**: People/Orgs found (with frequency counts).

---

## 📂 Project Structure

```
nexatest/
├── app/
│   ├── api/             # Endpoints (Upload, Job Status)
│   ├── core/            # Database Config (SQLModel)
│   ├── models/          # DB Models (Job, Document, Chunk...)
│   ├── services/
│   │   ├── parsing/     # Docling, OCR, Orchestrator
│   │   ├── enrichment/  # AI Models (Summarizer, KeyBERT)
│   │   └── background.py# Parsing Worker
│   └── main.py          # App Entrypoint
├── docs/                # Setup Guides
├── docker-compose.yaml  # DB & pgAdmin Config
├── requirements.txt     # Python Dependencies
└── verify_migration.py  # Test Script
```

---

## ⚡ Quick Start (New User Guide)

### 1. Prerequisites

* **Docker Installed** (Required for Database).
* **Python 3.10+**.

### 2. Start Database

Run the following to start PostgreSQL and pgAdmin:

```powershell
docker-compose up -d
```

* **Check**: Run `docker ps` to ensure `nexatest_db` is running.

### 3. Install Dependencies

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

*(This installs 1.5GB+ of AI models. Be patient!)*

### 4. Run API Server

```powershell
uvicorn app.main:app --reload
```

API runs at: `http://localhost:8000`

### 5. Access Database GUI

* **URL**: `http://localhost:5050` (pgAdmin)
* **Login**: `admin@admin.com` / `admin`
* **Add Server**:
  * Host: `db` (or `localhost` if connecting from host machine, but use `db` inside docker network).
  * Username: `postgres`
  * Password: `admin`

---

## 🔍 Testing

### Option A: Swagger UI

1. Go to `http://localhost:8000/docs`.
2. Use `/upload` to send a file.
3. Use `/jobs/{id}` to check results.



---

## 📝 Change Log

* **v1.3**: **Database Migration** (PostgreSQL). precise Schema (Chunks/Tables), Docker support.
* **v1.2**: Transformer Upgrade (BART/KeyBERT).
* **v1.0**: Initial Release.
