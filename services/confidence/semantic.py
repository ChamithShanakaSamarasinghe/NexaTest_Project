# analyzers/semantic.py

from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

class SemanticAnalyzer:
    def __init__(self):
        self.model = load_model()
        #self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def analyze(self, question: str, answer: str) -> float:
        q_emb = self.model.encode(question, convert_to_tensor=True)
        a_emb = self.model.encode(answer, convert_to_tensor=True)
        score = util.cos_sim(q_emb, a_emb).item()
        return max(0.0, min(1.0, score))
