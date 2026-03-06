# confidence_scorer/result.py

def confidence_band(score: float) -> str:
    """
    Maps a numeric confidence score (0–1)
    to a confidence band (A–E).
    """

    if score >= 0.85:
        return "A"   # Highly Confident
    elif score >= 0.70:
        return "B"   # Confident
    elif score >= 0.55:
        return "C"   # Moderate
    elif score >= 0.40:
        return "D"   # Low
    else:
        return "E"   # Unreliable
