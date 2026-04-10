# NexaTest 🚀  
### AI-Powered Multi-Modal SRS Intelligence Platform

NexaTest is an advanced AI-driven platform designed to **extract, analyze, validate, and enhance Software Requirement Specifications (SRS)** from real-world multi-format sources.

It transforms unstructured inputs into **structured, testable, and intelligent requirement insights** using Machine Learning and Large Language Models (LLMs).

---

## 🌟 Key Highlights

✅ Multi-modal SRS processing (Docs, Audio, Video, Email, Chat)  
✅ AI-powered requirement extraction & classification  
✅ Automated test case generation  
✅ Feature Priority Risk (FPR) clustering & analysis  
✅ Confidence scoring using LLM pipeline  
✅ Interactive Streamlit dashboard  
✅ Persistent SQLite database storage  

---

## 🚀 Core Technologies

- **Streamlit** → Interactive UI & visualization  
- **FastAPI** → High-performance backend APIs  
- **Machine Learning (Scikit-learn)** → Classification & clustering  
- **LLM Pipeline** → Intelligent requirement enhancement  
- **KeyBERT** → Keyword extraction  
- **spaCy NLP** → Named entity recognition  
- **DistilBART** → Text summarization  
- **Whisper (OpenAI)** → Audio/video transcription  
- **Tesseract OCR** → Image & handwritten text extraction  
- **SQLite** → Persistent storage  

---

## 📄 Multi-Modal Input Support 🔥

NexaTest processes real-world requirement sources beyond traditional documents:

### 📁 Documents
- `.docx`, `.pdf`, `.pptx`

### 🖼️ Images
- `.png`, `.jpg`, `.jpeg`  
- OCR-based text extraction

### 🎧 Audio
- `.mp3`, `.wav`  
- Speech-to-text via Whisper

### 🎬 Video
- `.mp4`, `.avi`, `.mov`  
- Audio extraction → Transcription → Processing

### 📧 Emails
- `.eml`  
- Header removal + signature cleanup

### 💬 Chat Data
- `.txt`  
- WhatsApp / Messenger parsing  
- Slang normalization (e.g., *pls → please*)

---

## ⚙️ System Capabilities

NexaTest automatically extracts and generates:

- 📌 Functional Requirements  
- 📌 Non-functional Requirements  
- 📌 System Features  
- 📌 Document Structure & Sections  
- 📌 Keywords & Clusters  
- 📌 Auto-generated Test Cases  

---

## 🧠 AI Processing Pipeline


Multi-Modal Input
↓
Text Extraction Layer
↓
Cleaning & Normalization
↓
Sentence Segmentation
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
Streamlit Visualization


---

## 🔍 Feature Priority Risk (FPR) Analysis

Advanced clustering-based analysis for:

- Requirement grouping  
- Feature mapping  
- Risk identification  
- Priority classification  

### 📊 Metrics:
- Silhouette Score  
- Cluster Similarity  
- Feature Density  

---

## 🧪 Automated Test Case Generation

Each requirement is transformed into structured test cases using:

- Equivalence Partitioning  
- Boundary Value Analysis  
- Decision Tables  
- State Transition Testing  
- Use Case Testing  
- Exploratory Testing  

---

## 📊 Confidence Scoring System

Evaluates requirement quality using weighted metrics:

| Metric              | Weight |
|--------------------|--------|
| Semantic Similarity | 0.40   |
| Completeness        | 0.35   |
| Safety              | 0.25   |

### Formula:

Final Score = (0.4 × Semantic) + (0.35 × Completeness) + (0.25 × Safety)


### Score Bands:

| Score  | Grade |
|--------|------|
| ≥ 0.85 | A |
| ≥ 0.70 | B |
| ≥ 0.50 | C |
| < 0.50 | D |

---

## 🧹 LLM Post-Processing

- Removes filler phrases  
- Cleans formatting  
- Normalizes whitespace  
- Improves readability  

---

## 💾 Database Architecture

Stored in `db.sqlite3`

| Table          | Description |
|---------------|------------|
| documents     | Uploaded files |
| sections      | Extracted sections |
| requirements  | Extracted requirements |
| features      | Identified features |
| fpr_results   | Clustering outputs |
| test_results  | Generated test cases |

---

## 📂 Project Structure


NexaTest/
│
├── src/
│ ├── srs_app.py # Streamlit UI
│ ├── fastapi_app.py # FastAPI backend
│ ├── enhancer.py # LLM enhancements
│ ├── db/ # Database modules
│ ├── fpr/ # Clustering logic
│ ├── testcase/ # Test case generation
│ └── services/ # Core services
│
├── srs_docs/ # Sample inputs
├── results/ # Outputs
├── db.sqlite3 # Database
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

Mac/Linux

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

▶️ Running the System

Start Streamlit UI

streamlit run src/srs_app.py

Start FastAPI Backend

uvicorn src.fastapi_app:app --reload

API Documentation

http://127.0.0.1:8000/docs

🎯 Use Cases

Software Development Teams

QA Engineers & Testers

Business Analysts

Research & Academic Projects

🔮 Future Enhancements

🔗 Retrieval-Augmented Generation (RAG)

☁️ Cloud Deployment (AWS / Azure)

🤖 Advanced LLM integrations (OpenAI, HuggingFace, Ollama)

📊 SRS Quality Scoring System

✍️ Advanced OCR for handwritten notes

🤝 Real-time collaboration features

🔄 CI/CD integration for requirement validation

👨‍💻 Author

Chamith Shanaka Samarasinghe
AI/ML & Data Science Intern — JW Infotech