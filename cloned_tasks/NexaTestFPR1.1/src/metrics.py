from sklearn.metrics import silhouette_score

def compute_metrics(X, labels):
    return {
        "silhouette_score": silhouette_score(X, labels)
    }