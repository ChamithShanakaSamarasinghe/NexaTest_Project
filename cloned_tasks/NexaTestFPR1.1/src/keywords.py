def extract_cluster_keywords(X, labels, vectorizer, top_n=10):
    feature_names = vectorizer.get_feature_names_out()
    cluster_keywords = {}

    for cluster_id in set(labels):
        mask = labels == cluster_id
        summed = X[mask].sum(axis=0)
        top_indices = summed.A1.argsort()[::-1][:top_n]
        cluster_keywords[cluster_id] = [
            feature_names[i] for i in top_indices
        ]

    return cluster_keywords