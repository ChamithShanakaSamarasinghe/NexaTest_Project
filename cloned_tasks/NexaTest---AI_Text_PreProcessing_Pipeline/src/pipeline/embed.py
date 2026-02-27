from gensim.models import Word2Vec
from typing import Dict, List


class EmbeddingGenerator:
    
    def __init__(self, vector_size=100, window=5, min_count=1, workers=2):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.workers = workers
        self.model = None

    def train(self, token_sentences: List[List[str]]):
        
        self.model = Word2Vec(
            sentences=token_sentences,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers
        )

        return self.model

    def get_embeddings(self) -> Dict[str, List[float]]:
        
        embeddings = {}

        for word in self.model.wv.index_to_key:
            embeddings[word] = self.model.wv[word].tolist()

        return embeddings


# Test block
if __name__ == "__main__":
    sample_sentences = [
        ["this", "is", "a", "sample", "text"],
        ["this", "text", "is", "for", "testing"],
        ["we", "are", "learning", "word", "embeddings"]
    ]

    generator = EmbeddingGenerator(vector_size=50)
    generator.train(sample_sentences)

    vectors = generator.get_embeddings()

    print("Embedding size:", len(next(iter(vectors.values()))))
    print("Words:", list(vectors.keys())[:5])
