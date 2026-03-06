import re

class CompletenessAnalyzer:
    def analyze(self, question: str, answer: str) -> float:
        keywords = re.findall(r"\b\w+\b", question.lower())
        keywords = [k for k in keywords if len(k) > 3]

        if not keywords:
            return 0.5

        hits = sum(1 for k in keywords if k in answer.lower())
        return min(1.0, hits / len(keywords))
