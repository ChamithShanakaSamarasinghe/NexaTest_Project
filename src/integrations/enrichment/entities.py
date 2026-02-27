import spacy

class EntityExtractor:
    def __init__(self, model="en_core_web_sm"):
        # model must me installed before use
        try:
            self.nlp = spacy.load(model)
        except OSError:
            from spacy.cli import download
            download(model)
            self.nlp = spacy.load(model)

    def extract(self, text: str):
        doc = self.nlp(text)
        from collections import Counter
        # Key: (text, label), Value: count
        entity_counts = Counter()
        
        for ent in doc.ents:
            # Normalize text slightly (strip)
            clean_text = ent.text.strip()
            if len(clean_text) > 1:
                entity_counts[(clean_text, ent.label_)] += 1
                
        results = []
        for (text, label), count in entity_counts.items():
            results.append({
                "text": text,
                "label": label,
                "count": count
            })
            
        return results
