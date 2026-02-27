# src/enhancer.py
import os
import sys
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# External Pipeline Paths
CLONED_REPO_PATH = os.path.join(
    BASE_DIR,
    "..",
    "cloned_tasks",
    "NexaTest---AI_Text_PreProcessing_Pipeline",
    "src",
    "pipeline"
)

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "..",
    "cloned_tasks",
    "NexaTest---AI_Text_PreProcessing_Pipeline",
    "config",
    "rules.yaml"
)

# FPR pipeline path
FPR_PATH = os.path.join(BASE_DIR, "fpr")

# Add paths
if os.path.exists(CLONED_REPO_PATH):
    sys.path.insert(0, CLONED_REPO_PATH)

if os.path.exists(FPR_PATH):
    sys.path.insert(0, FPR_PATH)

# Import External Components
TextCleaner = None
EmbeddingGenerator = None
run_fpr_pipeline = None

try:
    from clean import TextCleaner
    print("[INFO] Using real TextCleaner")
except:
    print("[WARNING] Using fallback cleaner")

try:
    from embed import EmbeddingGenerator
    print("[INFO] Using real EmbeddingGenerator")
except:
    print("[WARNING] Using fallback embedder")

try:
    from fpr_pipeline import run_fpr_pipeline
    print("[INFO] FPR pipeline loaded")
except:
    print("[WARNING] FPR pipeline not found")


# Fallbacks
class FallbackCleaner:
    def clean(self, text: str) -> str:
        return text.lower().strip()


class FallbackEmbedding:
    def __init__(self, vector_size=50):
        self.vector_size = vector_size

    def generate(self, tokens):
        return {t: np.random.rand(self.vector_size).tolist() for t in tokens}


# Enhancer Class
class PipelineEnhancer:
    def __init__(self, vector_size=50):

        # Cleaner
        try:
            self.cleaner = TextCleaner(config_path=CONFIG_PATH) if TextCleaner else FallbackCleaner()
        except:
            self.cleaner = FallbackCleaner()

        # Embedder
        try:
            self.embedder = EmbeddingGenerator(vector_size=vector_size) if EmbeddingGenerator else FallbackEmbedding(vector_size)
        except:
            self.embedder = FallbackEmbedding(vector_size)

        # Mode detect
        if hasattr(self.embedder, "train"):
            self.embed_mode = "train_get"
        elif hasattr(self.embedder, "generate"):
            self.embed_mode = "generate"
        else:
            self.embed_mode = "fallback"

        print(f"[INFO] embed_mode = {self.embed_mode}")

    # Cleaning
    def safe_clean(self, text):
        if hasattr(self.cleaner, "clean"):
            return self.cleaner.clean(text)
        return text.lower().strip()

    # Tokenization
    def tokenize(self, text):
        return text.split()

    # Embeddings
    def get_embeddings(self, tokens, text):

        if self.embed_mode == "train_get":
            try:
                self.embedder.train([tokens])
                emb = self.embedder.get_embeddings()
            except:
                emb = {}
        else:
            try:
                emb = self.embedder.generate(tokens)
            except:
                emb = {}

        if not emb:
            emb = {t: np.random.rand(16).tolist() for t in tokens}

        return emb

    # Similarity
    def compute_similarity(self, embeddings):
        keys = list(embeddings.keys())
        if len(keys) < 2:
            return []

        base = np.array(embeddings[keys[0]])
        sims = []

        for k in keys[1:]:
            v = np.array(embeddings[k])
            sim = np.dot(base, v) / ((np.linalg.norm(base) * np.linalg.norm(v)) + 1e-9)
            sims.append((k, float(sim)))

        return sorted(sims, key=lambda x: x[1], reverse=True)[:5]

    # Rules
    def extract_rules(self, tokens):
        rules = {}
        for t in tokens:
            if "email" in t:
                rules[t] = "EMAIL_FIELD"
            elif "password" in t:
                rules[t] = "PASSWORD_FIELD"
        return rules

    # FPR Integration
    def run_fpr(self, tokens):
        if run_fpr_pipeline:
            try:
                return run_fpr_pipeline(tokens)
            except Exception as e:
                print("[WARNING] FPR failed:", e)
        return {"clusters": [], "keywords": {}, "metrics": {}}

    # MAIN PIPELINE
    def enhance(self, text: str):

        # Step 1: Clean
        clean_text = self.safe_clean(text)

        # Step 2: Tokens
        tokens = self.tokenize(clean_text)
        token_counts = {t: tokens.count(t) for t in tokens}

        # Step 3: Embeddings
        embeddings = self.get_embeddings(tokens, clean_text)

        # Step 4: Similarity
        similarity = self.compute_similarity(embeddings)

        # Step 5: Rules
        rules = self.extract_rules(tokens)

        # 🔥 Step 6: FPR (NEW)
        fpr_result = self.run_fpr(tokens)

        return {
            "clean_text": clean_text,
            "tokens": token_counts,
            "embeddings": embeddings,
            "similarity": similarity,
            "rules": rules,
            "fpr": fpr_result   # 🚀 NEW OUTPUT
        }

# TEST
if __name__ == "__main__":
    enhancer = PipelineEnhancer()

    text = "User must login using email and password. System shall generate reports."

    result = enhancer.enhance(text)

    print("Clean:", result["clean_text"])
    print("Tokens:", list(result["tokens"].items())[:5])
    print("Similarity:", result["similarity"])
    print("Rules:", result["rules"])
    print("FPR:", result["fpr"])