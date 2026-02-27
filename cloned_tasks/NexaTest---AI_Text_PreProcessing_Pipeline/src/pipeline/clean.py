import re
import yaml


class TextCleaner:
    
    def __init__(self, config_path="config/rules.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.stopwords = set(
            self.config.get("cleaning", {}).get("stopwords", [])
        )

    def clean_text(self, text: str) -> str:
        # Lowercase
        text = text.lower()

        # Remove special characters except basic punctuation
        text = re.sub(r"[^a-z0-9\s.,!?]", " ", text)

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove stopwords
        words = text.split()
        words = [w for w in words if w not in self.stopwords]

        return " ".join(words)


# Test block
if __name__ == "__main__":
    sample = "This IS a Sample TEXT!!! with   extra spaces and symbols ###."

    cleaner = TextCleaner()
    result = cleaner.clean_text(sample)

    print("Original:", sample)
    print("Cleaned:", result)
