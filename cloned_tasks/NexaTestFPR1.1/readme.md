# Feature Encoding Pipeline (Non TF-IDF)

## 📌 Overview
This project implements a Feature Pattern Recognition pipeline that identifies recurring patterns in structured and unstructured text **without using TF-IDF**.
Instead, it evaluates alternative feature encoding techniques such as:

- One-Hot Encoding (OHE)
- One-Word Statistics (OWS)
- One-Class Bag of Objects (OCBO)

The pipeline performs clustering, keyword extraction, and persists results into a SQLite database for further analysis.

## 🎯 Objective
Identify recurring patterns in text using statistical / ML-based methods by experimenting with alternative feature encodings instead of TF-IDF.

## 🧠 Feature Encoding Methods
- **OHE**: Binary word presence
- **OWS**: Word frequency counts
- **OCBO**: Word co-occurrence representation

## 🗂️ Project Structure
Feature_Encoding_Pipeline/
├── data/
├── output/
├── db/
├── src/
├── main.py
├── requirements.txt
└── README.md

## ▶️ How to Run
1. Create virtual environment
2. Install requirements
3. Run:
   python main.py

## 🗄️ Database
- SQLite database stored in `db/feature_encoding.db`
- Insert data using:
  python src/insert_data.py

## 📈 Evaluation
- Silhouette Score used for clustering evaluation

## ✅ Conclusion
This project demonstrates modular and controlled experimentation with alternative text feature encodings.
