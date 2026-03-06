import streamlit as st
from services.confidence.pipeline import run_pipeline

st.title("NexaTest Confidence Pipeline")
st.write("Test the requirement confidence scoring pipeline.")

# User input
question = st.text_area(
    "Requirement / Question",
    "The system shall allow users to reset their password securely."
)

requirement_id = st.number_input(
    "Requirement ID",
    min_value=1,
    value=1
)

# Run pipeline button
if st.button("Run Pipeline"):
    result = run_pipeline(question, requirement_id)

    st.subheader("Pipeline Result")

    # ✅ Show raw LLM answer before post-processing
    st.write("**Raw LLM Answer (before post-processing):**")
    st.write(result.get("raw_answer", "[No raw answer available]"))

    # ✅ Show cleaned answer after post-processing
    st.write("**Cleaned Answer (after post-processing):**")
    st.write(result["answer"])

    # Confidence scores
    st.write("**Final Score:**")
    st.write(result["final_score"])

    st.write("**Confidence Band:**")
    st.write(result["band"])

    st.write("**Scores Breakdown:**")
    st.json(result["scores"])

    st.write("**Warnings:**")
    if result["warnings"]:
        st.write(result["warnings"])
    else:
        st.success("No warnings")