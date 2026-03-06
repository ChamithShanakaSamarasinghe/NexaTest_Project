# confidence_scorer/validator.py

def validate(scores: dict, final_score: float) -> list:
    warnings = []

    if scores["safety"] < 0.5:
        warnings.append("Unsafe content detected")

    if final_score < 0.6:
        warnings.append("Low confidence: human review recommended")

    return warnings
