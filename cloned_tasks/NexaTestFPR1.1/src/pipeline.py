import pandas as pd
from src.preprocessing import clean_text
from src.feature_extraction import extract_ohe, extract_ows
from src.clustering import cluster_documents
from src.keywords import extract_cluster_keywords
from src.metrics import compute_metrics

def run_pipeline(feature_type="OHE"):
    df = pd.read_csv("data/text_data.csv")
    texts = df["text"].astype(str).apply(clean_text).tolist()

    if feature_type == "OHE":
        X, vectorizer = extract_ohe(texts)
    elif feature_type == "OWS":
        X, vectorizer = extract_ows(texts)
    else:
        raise ValueError("Unsupported feature type")

    labels, _ = cluster_documents(X)
    metrics = compute_metrics(X, labels)
    keywords = extract_cluster_keywords(X, labels, vectorizer)

    df["cluster"] = labels
    df.to_csv("output/output_with_clusters.csv", index=False)

    return metrics, keywords