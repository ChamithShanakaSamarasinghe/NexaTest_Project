from collections import Counter
from typing import List, Dict


class Tokenizer:

    def __init__(self):
        pass

    def tokenize(self, text: str) -> List[str]:
        
        return text.split()

    def get_frequencies(self, tokens: List[str]) -> Dict[str, int]:
        
        return dict(Counter(tokens))

    def process(self, text: str) -> Dict[str, int]:
        
        tokens = self.tokenize(text)
        frequencies = self.get_frequencies(tokens)
        return frequencies


# Test block
if __name__ == "__main__":
    sample_text = "this is a sample text this is test"

    tokenizer = Tokenizer()
    freq = tokenizer.process(sample_text)

    print("Token Frequencies:")
    for k, v in freq.items():
        print(k, ":", v)
