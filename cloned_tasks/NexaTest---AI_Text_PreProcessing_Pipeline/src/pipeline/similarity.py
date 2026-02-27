from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Tuple


class SimilarityAnalyzer:
    """
    Computes similarity between word embeddings.
    """

    def __init__(self, embeddings: Dict[str, List[float]]):
        self.embeddings = embeddings
        self.words = list(embeddings.keys())
        self.vectors = np.array(list(embeddings.values()))

    def compute_matrix(self):
        """
        Compute cosine similarity matrix.
        """
        return cosine_similarity(self.vectors)

    def top_n_similar(self, word: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Get top-N similar words for a given word.
        """
        if word not in self.embeddings:
            raise ValueError("Word not found in embeddings")

        matrix = self.compute_matrix()
        idx = self.words.index(word)

        similarity_scores = matrix[idx]

        results = list(zip(self.words, similarity_scores))

        # Sort by similarity descending
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # Remove the word itself
        results = results[1:n+1]

        return results


# Test block
if __name__ == "__main__":
    sample_embeddings = {
        "text": [0.1, 0.2, 0.3],
        "word": [0.12, 0.18, 0.29],
        "car": [0.9, 0.1, 0.2],
        "vehicle": [0.88, 0.12, 0.25],
        "cat": [0.01, 0.9, 0.3]
    }

    analyzer = SimilarityAnalyzer(sample_embeddings)

    print("Top similar to 'text':")
    for w, s in analyzer.top_n_similar("text", 3):
        print(w, "=>", round(s, 3))
