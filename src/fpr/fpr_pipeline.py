import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def run_fpr_pipeline(requirements):
    if not requirements:
        return {
            "clusters": [],
            "keywords": {},
            "metrics": {}
        }

    # Vectorization
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(requirements)

    # Clustering (SAFE)
    n_clusters = min(5, len(requirements))

    # 🔥 IMPORTANT FIX:
    # KMeans requires n_clusters < n_samples
    if n_clusters >= len(requirements):
        n_clusters = max(1, len(requirements) - 1)

    # If still invalid, fallback
    if n_clusters <= 1:
        labels = [0] * len(requirements)
    else:
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = model.fit_predict(X)

    # Keywords extraction
    feature_names = vectorizer.get_feature_names_out()
    keywords = {}

    for cluster_id in set(labels):
        mask = [i == cluster_id for i in labels]
        summed = X[mask].sum(axis=0)
        top_indices = summed.A1.argsort()[::-1][:5]
        keywords[str(cluster_id)] = [feature_names[i] for i in top_indices]

    # 🔥 SAFE silhouette score calculation
    score = 0
    try:
        unique_labels = len(set(labels))

        # Valid only if:
        # 1. More than 1 cluster
        # 2. Less clusters than number of samples
        if 1 < unique_labels < len(requirements):
            score = silhouette_score(X, labels)
        else:
            score = 0

    except Exception as e:
        print(f"[WARNING] Silhouette score skipped: {e}")
        score = 0

    return {
        "clusters": list(map(int, labels)),
        "keywords": keywords,
        "metrics": {
            "silhouette_score": float(score),
            "total_requirements": len(requirements),
            "total_clusters": len(set(labels))
        }
    }