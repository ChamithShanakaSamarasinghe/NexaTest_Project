from transformers import pipeline
import warnings

# Suppress warnings that might clutter logs
warnings.filterwarnings("ignore")

class Summarizer:
    def __init__(self, model="sshleifer/distilbart-cnn-12-6"):
        # Initialize the summarization pipeline
        # "cpu" is -1 in device map for transformers, but pipeline handles it.
        try:
            print(f"Loading Summarization Model: {model}...")
            self.summarizer = pipeline("summarization", model=model)
            print("Summarization Model Loaded.")
        except Exception as e:
            print(f"Failed to load summarization model: {e}")
            self.summarizer = None

    def summarize(self, text: str, max_length=150, min_length=30):
        if not self.summarizer:
            return "Summarizer not available."
            
        # Basic check for text length
        if len(text.strip()) < 100:
            return text
            
        # Transformers have token limits (usually 1024 tokens ~ 3000-4000 chars). 
        # We must truncate. A simple char limit is safest for now.
        clean_text = text.replace("\n", " ")[:3500]
        
        # Summarize
        try:
            summary = self.summarizer(clean_text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Summarization failed: {e}")
            return "Summarization failed."
