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

# 🔥 Importing AI modules
from src.enhancer import PipelineEnhancer
from src.fpr.fpr_pipeline import run_fpr_pipeline

# Paths
DB_FILE = "db.sqlite3"
SRS_FOLDER = "srs_docs"
RESULTS_FOLDER = "results"

os.makedirs(SRS_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Initializing Enhancer
enhancer = PipelineEnhancer()

# Database Utility
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


# Streamlit UI
st.set_page_config(page_title="🚀 SRS Automation Platform", layout="wide")
st.title("🚀 SRS Automation Platform (AI Powered)")

# ✅Allow PDF + DOCX
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

    # ✅Handling DOCX + PDF
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

    # Extracting Sections, Requirements, Features
    sections, requirements, features = [], [], []
    current_section = None
    full_text = ""

    for para in paragraphs:
        text = str(para).strip()
        if not text:
            continue

        full_text += text + " "

        # Section detection (basic)
        if text.isupper() or text.endswith(":"):
            current_section = text
            sections.append({"section_name": current_section, "content": ""})
        else:
            if current_section:
                sections[-1]["content"] += text + " "

        # ✅Better requirement extraction
        if any(keyword in text.lower() for keyword in ["shall", "must", "should", "will"]):
            requirements.append(text)

        # Feature detection
        if "feature" in text.lower():
            features.append(text)

    # Running Enhancer
    enhanced = enhancer.enhance(full_text)
    clean_text = enhanced["clean_text"]

    # Running FPR
    fpr_result = run_fpr_pipeline(requirements) if requirements else {
        "clusters": [], "keywords": {}, "metrics": {}
    }

    # Dummy test results
    test_results = {
        "test_requirement_extraction": "PASSED",
        "test_testcase_generation": "PASSED",
        "test_srs_upload": "PASSED"
    }

    # Saving JSON
    output_json = os.path.join(RESULTS_FOLDER, f"{srs_filename}.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "sections": sections,
            "requirements": requirements,
            "features": features,
            "clean_text": clean_text,
            "fpr": fpr_result,
            "test_results": test_results
        }, f, indent=4)

    # Saving DB
    doc_id = insert_into_db(srs_filename, sections, requirements, features, test_results, fpr_result)
    st.success(f"💾 Data saved to database with doc_id {doc_id}")

    # 🔥 Metrics Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Requirements", len(requirements))
    col2.metric("✨ Features", len(features))
    col3.metric("🧠 Clusters", len(set(fpr_result["clusters"])))

    # Tabs
    tabs = st.tabs(["📄 Sections", "📌 Requirements", "✨ Features", "🧠 FPR", "📊 Analytics"])

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

        if st.button("Export CSV"):
            df = pd.DataFrame({"requirements": filtered})
            path = os.path.join(RESULTS_FOLDER, f"{srs_filename}_reqs.csv")
            df.to_csv(path, index=False)
            st.success(f"Saved: {path}")

    # Features
    with tabs[2]:
        for i, f in enumerate(features, 1):
            with st.expander(f"Feature {i}"):
                st.write(f)

    # ✅Proper FPR visualization
    with tabs[3]:
        clusters = fpr_result["clusters"]
        keywords = fpr_result["keywords"]

        cluster_map = {}
        for req, label in zip(requirements, clusters):
            cluster_map.setdefault(label, []).append(req)

        for cluster_id, reqs in cluster_map.items():
            with st.expander(f"Cluster {cluster_id}"):
                st.write("📌 Requirements:")
                for r in reqs:
                    st.markdown(f"- {r}")

                st.write("🔑 Keywords:")
                st.write(keywords.get(str(cluster_id), []))

        st.json(fpr_result["metrics"])

    # Analytics
    with tabs[4]:
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