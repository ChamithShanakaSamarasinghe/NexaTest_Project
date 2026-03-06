from llm.generator import generate_answer

# ✅ Updated imports
from services.confidence.semantic import SemanticAnalyzer
from services.confidence.completeness import CompletenessAnalyzer
from services.confidence.safety import SafetyAnalyzer
from services.confidence.scorer import ConfidenceScorer
from services.confidence.result import confidence_band
from services.confidence.validator import validate

# ✅ Import DB insertion function
from src.db.insert_requirements import insert_confidence_result

# ✅ Corrected Import for Post-Processing
from services.post_processing.response_processing.post_processor import ResponsePostProcessor

# Fixed weights (sum = 1.0)
WEIGHTS = {
    "semantic": 0.4,
    "completeness": 0.35,
    "safety": 0.25
}

# Initialize the post-processor once
post_processor = ResponsePostProcessor()


def run_pipeline(question: str, requirement_id: int):
    """
    Runs the full QA + confidence scoring pipeline,
    cleans the LLM output, and stores results into SRS database.

    :param question: Text of the requirement or query
    :param requirement_id: Corresponding ID in requirements table
    :return: Dict containing answer, scores, band, and warnings
    """

    # 1️⃣ Generate raw answer (LLM or mock)
    raw_answer = generate_answer(question)

    # 2️⃣ Post-process model response (Task 196)
    answer = post_processor.clean(raw_answer)

    # 3️⃣ Run analyzers
    semantic_score = SemanticAnalyzer().analyze(question, answer)
    completeness_score = CompletenessAnalyzer().analyze(question, answer)
    safety_score = SafetyAnalyzer().analyze(question, answer)

    scores = {
        "semantic": semantic_score,
        "completeness": completeness_score,
        "safety": safety_score
    }

    # 4️⃣ Compute confidence score (Task 200)
    scorer = ConfidenceScorer(WEIGHTS)
    final_score = scorer.score(scores)
    band = confidence_band(final_score)

    # 5️⃣ Validation rules
    warnings = validate(scores, final_score)

    # 6️⃣ Store results in DB
    insert_confidence_result(
        requirement_id=requirement_id,
        final_score=final_score,
        band=band,
        breakdown=scores
    )

    # 7️⃣ Return everything UI or caller needs
    return {
        "raw_answer": raw_answer,
        "answer": answer,
        "final_score": final_score,
        "band": band,
        "scores": scores,
        "warnings": warnings
    }