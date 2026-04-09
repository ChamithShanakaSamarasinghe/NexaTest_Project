## NexaTest 🚀

An AI-powered SRS Automation Platform for extracting, analyzing, and generating insights from multi-format requirement sources.

---

## 🚀 Core Technologies

The platform combines multiple technologies:

- **Streamlit** → Interactive UI for SRS upload and visualization  
- **FastAPI** → Backend API services  
- **Machine Learning** → Requirement classification & clustering  
- **LLM Pipeline** → AI-powered requirement analysis  
- **KeyBERT** → Keyword extraction  
- **spaCy NLP** → Named entity recognition  
- **DistilBART** → Text summarization  
- **Whisper (OpenAI)** → Audio & video transcription  
- **Tesseract OCR** → Image & handwritten text extraction  
- **SQLite** → Persistent database storage  

---

## 📄 Supported SRS Input (MULTI-MODAL 🔥)

NexaTest now supports **real-world requirement sources**, not just documents:

### 📁 Documents
- `.docx` (Word)
- `.pdf` (PDF)
- `.pptx` (PowerPoint)

### 🖼️ Images
- `.png`, `.jpg`, `.jpeg`
- OCR-based text extraction (Tesseract)

### 🎧 Audio
- `.mp3`, `.wav`
- Speech-to-text using Whisper

### 🎬 Video
- `.mp4`, `.avi`, `.mov`
- Audio extracted → Transcribed → Processed

### 📧 Emails
- `.eml`
- Header removal (From, Subject, etc.)
- Signature & greeting cleanup

### 💬 Chat / Messaging
- `.txt`
- WhatsApp / Messenger-style chat parsing
- Slang normalization (e.g., *pls → please*)

---

## ⚙️ What the System Automatically Extracts

- 📌 Functional Requirements  
- 📌 Non-functional Requirements  
- 📌 System Features  
- 📌 Sections & Structure  
- 📌 Keywords & Clusters  
- 📌 Test Cases (Auto-generated)

---

## 🧠 AI Requirement Analysis Pipeline


Multi-Modal Input (Doc / Audio / Video / Email / Chat)
↓
Text Extraction Layer
↓
Text Cleaning & Normalization
↓
Sentence Splitting
↓
Requirement Extraction Engine
↓
Feature Detection
↓
Embedding Generation
↓
FPR Clustering
↓
Test Case Generation
↓
Database Storage
↓
Streamlit UI Visualization


---

## 🔍 Feature Priority Risk (FPR) Analysis

Capabilities include:

- Requirement clustering
- Feature mapping
- Risk identification
- Priority classification
- Cluster quality evaluation

**Metrics calculated:**

- Silhouette Score  
- Cluster similarity  
- Feature density  

---

## 🧪 Automated Test Case Generation

For each requirement, the system generates:

- Equivalence Partitioning  
- Boundary Value Analysis  
- Decision Tables  
- State Transition Testing  
- Use Case Testing  
- Exploratory Testing  

---

## 📊 Confidence Scoring System (LLM Pipeline)

| Metric              | Weight |
|--------------------|--------|
| Semantic Similarity | 0.40   |
| Completeness        | 0.35   |
| Safety              | 0.25   |

**Formula:**


Final Score = (0.4 × Semantic) +
(0.35 × Completeness) +
(0.25 × Safety)


**Bands:**

| Score  | Band |
|--------|------|
| ≥ 0.85 | A    |
| ≥ 0.70 | B    |
| ≥ 0.50 | C    |
| < 0.50 | D    |

---

## 🧹 LLM Response Post-Processing

Includes:

- Removing filler phrases  
- Cleaning formatting  
- Normalizing whitespace  
- Improving readability  

---

## 💾 Database Architecture

Stored in `db.sqlite3`

| Table             | Description |
|------------------|------------|
| documents        | Uploaded files |
| sections         | Extracted sections |
| requirements     | Extracted requirements |
| features         | Identified features |
| fpr_results      | Clustering results |
| test_results     | Test execution logs |

---

## 📂 Project Structure


NexaTest
│
├── src
│ ├── srs_app.py
│ ├── fastapi_app.py
│ ├── db
│ ├── enhancer.py
│ ├── fpr
│ ├── testcase
│ └── services
│
├── srs_docs
├── results
├── db.sqlite3
├── requirements.txt
└── README.md


---

## ⚙️ Installation

```bash
git clone <your-repository-url>
cd NexaTest

python -m venv venv
Activate Environment

Windows

venv\Scripts\activate

Mac / Linux

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

▶️ Running the System
Run Streamlit UI

streamlit run src/srs_app.py

Run FastAPI Backend

python -m uvicorn src.fastapi_app:app --reload

API Docs:

http://127.0.0.1:8000/docs
🎯 Key Highlights

✅ Multi-modal SRS processing (Doc, Audio, Video, Email, Chat)
✅ AI-powered requirement extraction
✅ Automated test case generation
✅ Feature clustering with FPR
✅ Real-time interactive dashboard
✅ Database-backed persistence

🔮 Future Improvements
Retrieval Augmented Generation (RAG)
OpenAI / HuggingFace / Ollama integration
Requirement ambiguity detection
SRS quality scoring
Handwritten note classification (advanced OCR)
Real-time collaboration features
CI/CD integration for requirement validation
👨‍💻 Author

Chamith Shanaka Samarasinghe
AI/ML & Data Science Intern — JW Infotech