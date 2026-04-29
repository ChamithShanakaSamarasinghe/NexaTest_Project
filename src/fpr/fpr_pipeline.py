def run_fpr_pipeline(requirements):

    if not requirements:
        return {
            "clusters": [],
            "keywords": {},
            "metrics": {}
        }

    clusters = []
    keywords = {}

    for i, req in enumerate(requirements):
        # simple grouping logic (based on keywords)
        if "login" in req.lower():
            cluster_id = 0
        elif "payment" in req.lower():
            cluster_id = 1
        else:
            cluster_id = 2

        clusters.append(cluster_id)

        # collect keywords (very simple)
        words = req.lower().split()
        keywords.setdefault(str(cluster_id), [])
        keywords[str(cluster_id)].extend(words[:3])  # first few words

    # remove duplicates
    for k in keywords:
        keywords[k] = list(set(keywords[k]))[:5]

    return {
        "clusters": clusters,
        "keywords": keywords,
        "metrics": {
            "silhouette_score": 0.0,
            "total_requirements": len(requirements),
            "total_clusters": len(set(clusters))
        }
    }