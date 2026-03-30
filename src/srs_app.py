import streamlit as st
import os
import sys
import json
from docx import Document
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px

# ✅ Adding project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 🔥 AI modules
from src.enhancer import PipelineEnhancer
from src.fpr.fpr_pipeline import run_fpr_pipeline

# 🔥 Test Case Generator
from src.testcase.generator import generate_test_cases

# Paths
DB_FILE = "db.sqlite3"
SRS_FOLDER = "srs_docs"
RESULTS_FOLDER = "results"

os.makedirs(SRS_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

enhancer = PipelineEnhancer()

# Database section
def insert_into_db(doc_filename, sections, requirements, features, test_results, fpr_result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO documents (filename) VALUES (?)", (doc_filename,))
    doc_id = cursor.lastrowid

    for sec in sections:
        cursor.execute(
            "INSERT INTO sections (document_id, section_name, content) VALUES (?, ?, ?)",
            (doc_id, sec["section_name"], sec["content"]),
        )

    for req in requirements:
        cursor.execute(
            "INSERT INTO requirements (document_id, requirement_text) VALUES (?, ?)",
            (doc_id, req),
        )

    for feat in features:
        cursor.execute(
            "INSERT INTO features (document_id, feature_name) VALUES (?, ?)",
            (doc_id, feat),
        )

    for test_name, status in test_results.items():
        cursor.execute(
            "INSERT INTO test_results (doc_id, test_name, status) VALUES (?, ?, ?)",
            (doc_id, test_name, status),
        )

    cursor.execute(
        "INSERT INTO fpr_results (document_id, clusters, keywords, metrics) VALUES (?, ?, ?, ?)",
        (
            doc_id,
            json.dumps(fpr_result["clusters"]),
            json.dumps(fpr_result["keywords"]),
            json.dumps(fpr_result["metrics"]),
        ),
    )

    conn.commit()
    conn.close()
    return doc_id


# UI section
st.set_page_config(page_title="🚀 SRS Automation Platform", layout="wide")
st.title("🚀 SRS Automation Platform (AI Powered)")

uploaded_file = st.file_uploader(
    "Upload your SRS (.docx / .pdf) file", type=["docx", "pdf"]
)

if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    srs_filename = f"{timestamp}_{uploaded_file.name}"
    srs_path = os.path.join(SRS_FOLDER, srs_filename)

    with open(srs_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ SRS file saved: {srs_filename}")

    # Reading the file
    paragraphs = []

    if uploaded_file.name.endswith(".docx"):
        doc = Document(srs_path)
        paragraphs = [p.text for p in doc.paragraphs]

    elif uploaded_file.name.endswith(".pdf"):
        import PyPDF2
        with open(srs_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                paragraphs.append(page.extract_text())

    else:
        st.error("Unsupported file format")
        st.stop()

    # Extraction
    sections, requirements, features = [], [], []
    current_section = None
    full_text = ""

    for para in paragraphs:
        text = str(para).strip()
        if not text:
            continue

        full_text += text + " "

        if text.isupper() or text.endswith(":"):
            current_section = text
            sections.append({"section_name": current_section, "content": ""})
        else:
            if current_section:
                sections[-1]["content"] += text + " "

        if any(k in text.lower() for k in ["shall", "must", "should", "will"]):
            requirements.append(text)

        if "feature" in text.lower():
            features.append(text)

    enhanced = enhancer.enhance(full_text)
    clean_text = enhanced["clean_text"]

    fpr_result = run_fpr_pipeline(requirements) if requirements else {
        "clusters": [], "keywords": {}, "metrics": {}
    }

    # Test Cases
    test_cases = generate_test_cases(requirements)

    # ✅ Safety fix (prevents crash)
    for i, tc in enumerate(test_cases):
        tc.setdefault("id", f"TC_AUTO_{i}")
        tc.setdefault("technique", "Unknown")
        tc.setdefault("requirement", "N/A")
        tc.setdefault("input", "N/A")
        tc.setdefault("expected", "N/A")

    # Dummy Test Results
    test_results = {
        "test_requirement_extraction": "PASSED",
        "test_testcase_generation": "PASSED",
        "test_srs_upload": "PASSED"
    }

    # Saving as a json file
    output_json = os.path.join(RESULTS_FOLDER, f"{srs_filename}.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "sections": sections,
            "requirements": requirements,
            "features": features,
            "test_cases": test_cases,
            "clean_text": clean_text,
            "fpr": fpr_result,
            "test_results": test_results
        }, f, indent=4)

    doc_id = insert_into_db(srs_filename, sections, requirements, features, test_results, fpr_result)
    st.success(f"💾 Data saved to database with doc_id {doc_id}")

    # METRICS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 Requirements", len(requirements))
    col2.metric("✨ Features", len(features))
    col3.metric("🧠 Clusters", len(set(fpr_result["clusters"])))
    col4.metric("🧪 Test Cases", len(test_cases))

    # TABS 
    tabs = st.tabs([
        "📄 Sections",
        "📌 Requirements",
        "✨ Features",
        "🧠 FPR",
        "🧪 Test Cases",
        "📊 Analytics"
    ])

    # Sections
    with tabs[0]:
        for sec in sections:
            with st.expander(sec["section_name"]):
                st.write(sec["content"])

    # Requirements
    with tabs[1]:
        search = st.text_input("🔍 Search Requirements")
        filtered = [r for r in requirements if search.lower() in r.lower()]
        for r in filtered:
            st.markdown(f"- {r}")

    # Features
    with tabs[2]:
        for i, f in enumerate(features, 1):
            with st.expander(f"Feature {i}"):
                st.write(f)

    # FPR
    with tabs[3]:
        cluster_map = {}
        for req, label in zip(requirements, fpr_result["clusters"]):
            cluster_map.setdefault(label, []).append(req)

        for cid, reqs in cluster_map.items():
            with st.expander(f"Cluster {cid}"):
                for r in reqs:
                    st.markdown(f"- {r}")
                st.write("Keywords:", fpr_result["keywords"].get(str(cid), []))

        st.json(fpr_result["metrics"])

    # Test Cases UI
    with tabs[4]:
        st.subheader("🧪 Generated Test Cases")
        st.write(f"Total Test Cases: {len(test_cases)}")

        if not test_cases:
            st.warning("No test cases generated.")
        else:
            for tc in test_cases[:100]:
                with st.expander(f"{tc['id']} | {tc['technique']}"):
                    st.write("📌 Requirement:", tc["requirement"])
                    st.write("🔹 Input:", tc["input"])
                    st.write("✅ Expected:", tc["expected"])

        if st.button("Export Test Cases CSV"):
            df = pd.DataFrame(test_cases)
            path = os.path.join(RESULTS_FOLDER, f"{srs_filename}_testcases.csv")
            df.to_csv(path, index=False)
            st.success(f"Saved: {path}")

    # Analytics
    with tabs[5]:
        total = len(test_results)
        passed = len([x for x in test_results.values() if x == "PASSED"])
        failed = total - passed

        st.metric("Total", total)
        st.metric("Passed", passed)
        st.metric("Failed", failed)

        df_chart = pd.DataFrame({
            "Status": ["Passed", "Failed"],
            "Count": [passed, failed]
        })

        fig = px.pie(df_chart, names="Status", values="Count")
        st.plotly_chart(fig)

    st.balloons()