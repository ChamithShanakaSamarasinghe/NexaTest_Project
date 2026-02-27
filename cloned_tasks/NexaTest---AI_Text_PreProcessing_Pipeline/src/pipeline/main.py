from src.pipeline.ingest import DataIngestor
from src.pipeline.clean import TextCleaner
from src.pipeline.tokenize import Tokenizer
from src.pipeline.embed import EmbeddingGenerator
from src.pipeline.similarity import SimilarityAnalyzer
from src.pipeline.rules import RuleEngine

from src.pipeline.database import (
    insert_tokens,
    insert_embeddings,
    insert_similarity,
    insert_rule_mappings
)

class DataPipeline:
    
    def __init__(self):
        self.ingestor = DataIngestor()
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer()
        self.embedder = EmbeddingGenerator(vector_size=50)
        self.rule_engine = RuleEngine()

    def run(self, file_path: str):
        print("\n--- PIPELINE STARTED ---")

        # 1. Ingest
        file_id, raw_text = self.ingestor.ingest(file_path)
        print("File ingested. File ID:", file_id)

        # 2. Clean
        clean_text = self.cleaner.clean_text(raw_text)
        print("Text cleaned.")

        # 3. Tokenize
        token_freq = self.tokenizer.process(clean_text)
        insert_tokens(file_id, token_freq)
        print("Tokens stored in DB.")

        # 4. Prepare sentences
        sentences = [clean_text.split()]

        # 5. Embeddings
        self.embedder.train(sentences)
        embeddings = self.embedder.get_embeddings()
        insert_embeddings(embeddings)
        print("Embeddings stored in DB.")

        # 6. Similarity
        similarity_analyzer = SimilarityAnalyzer(embeddings)
        sample_word = list(embeddings.keys())[0]
        similar_words = similarity_analyzer.top_n_similar(sample_word, 5)
        insert_similarity(sample_word, similar_words)
        print("Similarity stored in DB.")

        # 7. Rules
        rule_mappings = self.rule_engine.apply_rules(token_freq)
        insert_rule_mappings(rule_mappings)
        print("Rule mappings stored in DB.")

        print("--- PIPELINE FINISHED ---\n")

        return {
         "file_id": file_id,
        "tokens": token_freq,
        "embeddings": embeddings,
        "similarity": similar_words,
        "rules": rule_mappings
    }

# Test block
if __name__ == "__main__":
    pipeline = DataPipeline()
    result = pipeline.run("data/raw/sample.txt")
