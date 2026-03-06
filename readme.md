# NexaTest --- AI-Powered SRS Requirement Analysis Platform

NexaTest is an **AI-powered Software Requirement Specification (SRS)
analysis platform** that automates the extraction, analysis, and
validation of requirements from SRS documents.

The system combines:

-   **Streamlit** for an interactive UI
-   **FastAPI** for backend APIs
-   **LLM-based requirement analysis**
-   **Machine Learning models** for keyword extraction, summarization,
    and entity recognition
-   **Confidence scoring and response validation**
-   **SQLite database** for persistent storage

This enables automated requirement analysis, intelligent question
answering, and quality evaluation of software requirements.

------------------------------------------------------------------------

# 🚀 Key Features

## 1. Streamlit Interface (`srs_app.py`)

Upload `.docx` SRS documents and automatically extract:

-   Sections
-   Requirements
-   Features

AI-powered analysis includes:

-   **Keyword Extraction** using KeyBERT (`all-MiniLM-L6-v2`)
-   **Entity Recognition** using spaCy NLP pipeline
-   **Summarization** using `sshleifer/distilbart-cnn-12-6`

All extracted information is automatically stored in **SQLite
(`db.sqlite3`)**.

------------------------------------------------------------------------

## 2. FastAPI Backend (`fastapi_app.py`)

Provides powerful API endpoints for programmatic access.

### Core Endpoints

  Endpoint                             Description
  ------------------------------------ ---------------------------------
  `/documents`                         List uploaded documents
  `/documents/{doc_id}/sections`       Retrieve document sections
  `/documents/{doc_id}/requirements`   Retrieve extracted requirements
  `/documents/{doc_id}/features`       Retrieve extracted features
  `/documents/{doc_id}/test-results`   Retrieve automated test results
  `/documents/{doc_id}/fpr`            Feature Priority Risk analysis
  `/analytics/{doc_id}`                Test result summary
  `/process-srs`                       Process SRS programmatically
  `/full-analysis`                     Complete document analysis
  `/store-fpr/{doc_id}`                Store FPR clustering results

Swagger API documentation available at:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 🧠 LLM Requirement Analysis Pipeline

The system also includes an **LLM-driven requirement analysis
pipeline**.

Pipeline Flow:

User Requirement / Question ↓ LLM Generator ↓ Raw Model Response ↓
Response Post‑Processor (Task 196) ↓ Cleaned Response ↓ Analyzers -
Semantic Analyzer - Completeness Analyzer - Safety Analyzer ↓ Confidence
Scorer (Task 200) ↓ Validation Rules ↓ Database Storage ↓ Streamlit UI
Output

This allows the system to evaluate how reliable the AI-generated
responses are.

------------------------------------------------------------------------

# 📊 Confidence Scoring System

The confidence score evaluates the reliability of model responses.

  Metric                Weight
  --------------------- --------
  Semantic Similarity   0.40
  Completeness          0.35
  Safety                0.25

Final Score:

Final Score = (0.4 × Semantic) + (0.35 × Completeness) + (0.25 × Safety)

Confidence Bands:

  Score     Band
  --------- ------
  ≥ 0.85    A
  ≥ 0.70    B
  ≥ 0.50    C
  \< 0.50   D

------------------------------------------------------------------------

# 🧹 Model Response Post‑Processing (Task 196)

The **post‑processing module** cleans LLM outputs before analysis.

Functions include:

-   Removing filler phrases
-   Trimming whitespace
-   Standardizing formatting

Example:

Raw Response:

Sure! Here's the answer: Users can reset their password.

Processed Response:

Users can reset their password.

------------------------------------------------------------------------

# 🔍 Feature Priority Risk (FPR) Analysis

The platform performs **advanced feature clustering and risk analysis**.

Capabilities:

-   Cluster related features and requirements
-   Assign **priority levels** (High / Medium / Low)
-   Identify potential **risks** (Security, Performance, etc.)
-   Calculate **metrics** such as silhouette score for cluster quality

This helps identify critical features and risks within SRS documents.

------------------------------------------------------------------------

# 💾 Database

All extracted and analyzed data is stored in:

SQLite Database → `db.sqlite3`

Stored data includes:

-   Documents
-   Sections
-   Requirements
-   Features
-   Test results
-   FPR analysis
-   Confidence scores
-   Score breakdowns

------------------------------------------------------------------------

# 📂 Project Structure

NexaTest/ │ ├── src/ │ ├── srs_app.py │ ├── fastapi_app.py │ │ │ ├── db/
│ │ └── insert_requirements.py │ │ │ ├── llm/ │ │ └── generator.py │ │ │
└── services/ │ ├── confidence/ │ │ ├── pipeline.py │ │ ├── semantic.py
│ │ ├── completeness.py │ │ ├── safety.py │ │ ├── scorer.py │ │ ├──
result.py │ │ └── validator.py │ │ │ └── post_processing/ │ └──
response_processing/ │ └── post_processor.py │ ├── srs_docs/ ├──
db.sqlite3 ├── test_pipeline.py ├── requirements.txt └── README.md

------------------------------------------------------------------------

# ⚙️ Installation

Clone the repository:

git clone `<your-repo-url>`{=html} cd SRS-NexaTest

Create virtual environment:

python -m venv venv

Activate environment:

Windows: venv`\Scripts`{=tex}`\activate`{=tex}

Mac/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

------------------------------------------------------------------------

# ▶️ Running the System

## 1. Run Streamlit Interface

streamlit run src`\srs`{=tex}\_app.py

Upload `.docx` SRS documents and automatically process them.

------------------------------------------------------------------------

## 2. Run FastAPI Backend

python -m uvicorn src.fastapi_app:app --reload

Open API documentation:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 3. Run LLM Testing Pipeline

streamlit run test_pipeline.py

This interface allows you to:

-   Enter a requirement question
-   Generate an LLM response
-   Run response post‑processing
-   Evaluate semantic, completeness, and safety scores
-   Compute final confidence score

------------------------------------------------------------------------

# 🧪 Example Pipeline Output

The system displays:

-   Raw LLM Answer
-   Cleaned Response
-   Semantic Score
-   Completeness Score
-   Safety Score
-   Final Confidence Score
-   Confidence Band
-   Validation Warnings

------------------------------------------------------------------------

# 🔮 Future Improvements

Possible enhancements:

-   OpenAI / HuggingFace / Ollama integration
-   Retrieval Augmented Generation (RAG)
-   Requirement ambiguity detection
-   Advanced SRS quality metrics
-   Visualization dashboards
-   Automated requirement validation
-   CI/CD integration for requirement testing

------------------------------------------------------------------------

# 👨‍💻 Author

Chamith Shanaka Samarasinghe\
AI/ML & Data Science Intern --- JW Infotech
