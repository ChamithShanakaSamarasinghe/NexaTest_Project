# File: srs_app.py
import streamlit as st
import os
import shutil
import json
from docx import Document
import sqlite3
from datetime import datetime

# --- Paths ---
DB_FILE = "db.sqlite3"
SRS_FOLDER = "srs_docs"
RESULTS_FOLDER = "results"

os.makedirs(SRS_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# --- Utility functions ---
def insert_into_db(doc_filename, sections, requirements, features, test_results):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert document
    cursor.execute("INSERT INTO documents (filename) VALUES (?)", (doc_filename,))
    doc_id = cursor.lastrowid

    # Insert sections
    for sec in sections:
        cursor.execute(
            "INSERT INTO sections (document_id, section_name, content) VALUES (?, ?, ?)",
            (doc_id, sec["section_name"], sec["content"]),
        )

    # Insert requirements
    for req in requirements:
        cursor.execute(
            "INSERT INTO requirements (document_id, requirement_text) VALUES (?, ?)",
            (doc_id, req),
        )

    # Insert features
    for feat in features:
        cursor.execute(
            "INSERT INTO features (document_id, feature_name) VALUES (?, ?)",
            (doc_id, feat),
        )

    # Insert test results
    for test_name, status in test_results.items():
        cursor.execute(
            "INSERT INTO test_results (doc_id, test_name, status) VALUES (?, ?, ?)",
            (doc_id, test_name, status),
        )

    conn.commit()
    conn.close()
    return doc_id

# --- Streamlit UI ---
st.title("SRS Automation Platform")

uploaded_file = st.file_uploader("Upload your SRS (.docx) file", type=["docx"])

if uploaded_file:
    # Save uploaded file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    srs_filename = f"{timestamp}_{uploaded_file.name}"
    srs_path = os.path.join(SRS_FOLDER, srs_filename)

    with open(srs_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"SRS file saved: {srs_filename}")

    # --- Extract content ---
    doc = Document(srs_path)
    sections = []
    requirements = []
    features = []
    current_section = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if para.style.name.startswith("Heading"):
            current_section = text
            sections.append({"section_name": current_section, "content": ""})
        else:
            if current_section:
                sections[-1]["content"] += text + " "
            if text.lower().startswith("the system shall"):
                requirements.append(text)
            if "feature" in text.lower():
                features.append(text)

    # --- Dummy test results ---
    test_results = {
        "test_requirement_extraction": "PASSED",
        "test_testcase_generation": "PASSED",
        "test_srs_upload": "PASSED"
    }

    # Save to JSON
    output_json = os.path.join(RESULTS_FOLDER, f"{srs_filename}.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "sections": sections,
            "requirements": requirements,
            "features": features,
            "test_results": test_results
        }, f, indent=4)

    # --- Insert into database ---
    doc_id = insert_into_db(srs_filename, sections, requirements, features, test_results)
    st.success(f"Data saved to database with doc_id {doc_id}")

    # --- Display summary ---
    st.subheader("Summary")
    st.write(f"Sections extracted: {len(sections)}")
    st.write(f"Requirements extracted: {len(requirements)}")
    st.write(f"Features extracted: {len(features)}")
    st.write(f"Test results: {len(test_results)}")

    # Optional: show first 3 sections and requirements
    st.subheader("Sample Sections")
    for sec in sections[:3]:
        st.markdown(f"**{sec['section_name']}**: {sec['content'][:200]}...")

    st.subheader("Sample Requirements")
    for req in requirements[:5]:
        st.markdown(f"- {req}")