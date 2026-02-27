import streamlit as st
import os
import pandas as pd

from src.pipeline.main import DataPipeline
from src.pipeline.database import fetch_tokens, fetch_rule_mappings
from src.pipeline.database import fetch_all_similarity

st.set_page_config(page_title="AI Text Pipeline", layout="wide")

st.title("AI Text Preprocessing Pipeline")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file:
    file_path = f"data/raw/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded successfully")

    if st.button("Run Pipeline"):
        pipeline = DataPipeline()
        result = pipeline.run(file_path)

        file_id = result["file_id"]

        st.success("Pipeline executed and data stored in database")

        # ----- TOKENS -----
        st.subheader("Token Frequencies (From Database)")
        tokens = fetch_tokens(file_id)

        df_tokens = pd.DataFrame(tokens, columns=["Token", "Frequency"])
        st.dataframe(df_tokens)

        # ----- SIMILARITY -----
        st.subheader("Similarity Results (From Database)")
        sim = fetch_all_similarity()

        if sim:
            df_sim = pd.DataFrame(sim, columns=["Token 1", "Token 2", "Similarity"])
            st.dataframe(df_sim)
        else:
            st.info("No similarity data found.")


        # ----- RULES -----
        st.subheader("Rule Mappings (From Database)")
        rules = fetch_rule_mappings()

        if rules:
            df_rules = pd.DataFrame(rules, columns=["Token", "Category"])
            st.dataframe(df_rules)
        else:
            st.info("No rule mappings found for this file.")
