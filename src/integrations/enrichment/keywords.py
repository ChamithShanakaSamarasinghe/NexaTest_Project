from keybert import KeyBERT
import warnings

warnings.filterwarnings("ignore")

class KeywordExtractor:
    def __init__(self, model="all-MiniLM-L6-v2"):
        # KeyBERT uses sentence-transformers. 
        # "all-MiniLM-L6-v2" is fast and effective.
        try:
            print(f"Loading KeyBERT Model: {model}...")
            self.kw_model = KeyBERT(model=model)
            print("KeyBERT Model Loaded.")
        except Exception as e:
            print(f"Failed to load KeyBERT: {e}")
            self.kw_model = None

    def extract(self, text: str, top_n=10):
        if not self.kw_model:
            return []
            
        try:
            # extract_keywords returns list of (keyword, score)
            # keyphrase_ngram_range=(1, 2) allows 1-2 word phrases
            keywords = self.kw_model.extract_keywords(
                text, 
                keyphrase_ngram_range=(1, 2), 
                stop_words='english', 
                top_n=top_n
            )
            # Match standard structure: [{"text": kw, "score": score}]
            return [{"text": kw, "score": score} for kw, score in keywords]
        except Exception as e:
            print(f"Keyword extraction failed: {e}")
            return []
