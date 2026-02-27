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

    # Clustering
    n_clusters = min(5, len(requirements))  # avoid crash
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(X)

    # Keywords extraction
    feature_names = vectorizer.get_feature_names_out()
    keywords = {}

    for cluster_id in set(labels):
        mask = labels == cluster_id
        summed = X[mask].sum(axis=0)
        top_indices = summed.A1.argsort()[::-1][:5]
        keywords[cluster_id] = [feature_names[i] for i in top_indices]

    # Metrics
    score = silhouette_score(X, labels) if len(requirements) > 2 else 0

    return {
        "clusters": labels.tolist(),
        "keywords": keywords,
        "metrics": {"silhouette_score": float(score)}
    }