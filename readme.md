## NexaTest

## 🚀 Core Technologies

The platform combines multiple technologies:

- **Streamlit** → Interactive UI for SRS upload and analysis
- **FastAPI** → Backend API services
- **Machine Learning** → Requirement classification and feature clustering
- **LLM Pipeline** → AI-powered requirement analysis
- **KeyBERT** → Keyword extraction
- **spaCy NLP** → Named entity recognition
- **DistilBART** → Text summarization
- **SQLite** → Persistent database storage

## 📄 Supported SRS Input

NexaTest can process:

- `.docx` SRS documents (Streamlit UI)
- `.pdf` SRS documents (Extractor pipeline)

The system automatically extracts:

- Document sections
- Functional requirements
- Non-functional requirements
- System features

## 🧠 AI Requirement Analysis Pipeline

The platform implements an LLM-driven analysis pipeline.

**Flow:**

```
User Question / Requirement
        ↓
LLM Generator
        ↓
Raw Model Response
        ↓
Response Post-Processor
        ↓
Cleaned Response
        ↓
Analyzers
   • Semantic Analyzer
   • Completeness Analyzer
   • Safety Analyzer
        ↓
Confidence Scorer
        ↓
Validation Rules
        ↓
Database Storage
        ↓
Streamlit UI Output
```

This pipeline evaluates the quality and reliability of AI-generated answers.

## 📊 Confidence Scoring System

The confidence score evaluates the reliability of model responses.

| Metric              | Weight |
|--------------------|--------|
| Semantic Similarity | 0.40   |
| Completeness       | 0.35   |
| Safety             | 0.25   |

**Final Score Formula:**

```
Final Score = (0.4 × Semantic) +
              (0.35 × Completeness) +
              (0.25 × Safety)
```

**Confidence Bands:**

| Score  | Band |
|--------|------|
| ≥ 0.85 | A    |
| ≥ 0.70 | B    |
| ≥ 0.50 | C    |
| < 0.50 | D    |

## 🧹 LLM Response Post-Processing (Task 196)

Functions include:

- Removing filler phrases
- Cleaning formatting
- Normalizing whitespace
- Improving readability

**Example:**

**Raw Response**

```
Sure! Here's the answer:
Users can reset their password.
```

**Processed Response**

```
Users can reset their password.
```

## 🔍 Feature Priority Risk (FPR) Analysis

Capabilities include:

- Feature clustering
- Requirement-feature mapping
- Risk identification
- Priority classification
- Cluster quality evaluation

**Metrics calculated:**

- Silhouette Score
- Cluster similarity
- Feature density

## 🧾 Automated SRS Extraction Pipeline

Pipeline steps:

```
SRS PDF
   ↓
Text Cleaning
   ↓
Section Detection
   ↓
Requirement Extraction
   ↓
Feature Identification
   ↓
Embedding Generation
   ↓
FPR Clustering
   ↓
Database Storage
```

## 💾 Database Architecture

All extracted data is stored in `db.sqlite3`.

**Main tables:**

| Table               | Description                            |
|--------------------|----------------------------------------|
| documents           | Uploaded SRS files                     |
| sections            | Extracted document sections            |
| requirements        | Functional & non-functional requirements |
| features            | Extracted features                     |
| fpr_results         | Feature priority risk analysis runs    |
| confidence_scores   | AI response confidence scores          |

## 📂 Project Structure

```
NexaTest
│
├── src
│   ├── srs_app.py
│   ├── fastapi_app.py
│   ├── db
│   │   └── insert_requirements.py
│   ├── llm
│   │   └── generator.py
│   └── services
│       ├── confidence
│       │   ├── pipeline.py
│       │   ├── semantic.py
│       │   ├── completeness.py
│       │   ├── safety.py
│       │   ├── scorer.py
│       │   └── validator.py
│       └── post_processing
│           └── post_processor.py
├── srs_docs
├── test_srs_extractor.py
├── add_fpr_id_column.py
├── test_pipeline.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
git clone <your-repository-url>
cd NexaTest

python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the System

**Run Streamlit UI**

```bash
streamlit run src/srs_app.py
```

**Run FastAPI Backend**

```bash
python -m uvicorn src.fastapi_app:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

**Run SRS Extraction Pipeline**

```bash
python test_srs_extractor.py srs_docs/OSMS_SRS.pdf
```

**Run LLM Testing Interface**

```bash
streamlit run test_pipeline.py
```

## 🔮 Future Improvements

- Retrieval Augmented Generation (RAG)
- OpenAI / HuggingFace / Ollama integration
- Requirement ambiguity detection
- Automated requirement validation
- SRS quality scoring
- Interactive analytics dashboards
- CI/CD integration for requirement testing

## 👨‍💻 Author

Chamith Shanaka Samarasinghe  
AI/ML & Data Science Intern — JW Infotech