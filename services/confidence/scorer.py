# confidence_scorer/scorer.py

class ConfidenceScorer:
    """
    Computes the final confidence score using a weighted sum
    of individual analyzer scores.
    """

    def __init__(self, weights: dict):
        """
        weights: dictionary with keys matching analyzer names
                 e.g. {"semantic": 0.4, "completeness": 0.35, "safety": 0.25}
        """
        self.weights = weights

        # Safety check: weights should sum to ~1.0
        if not abs(sum(weights.values()) - 1.0) < 1e-6:
            raise ValueError("ConfidenceScorer weights must sum to 1.0")

    def score(self, scores: dict) -> float:
        """
        scores: dictionary with analyzer scores (0–1)
                e.g. {"semantic": 0.8, "completeness": 0.7, "safety": 1.0}

        Returns:
            final confidence score between 0 and 1
        """
        final_score = 0.0

        for name, value in scores.items():
            weight = self.weights.get(name, 0)
            final_score += value * weight

        # Clamp result just in case
        return max(0.0, min(1.0, final_score))
