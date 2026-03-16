import os
import re
import fitz  # PyMuPDF

REQUIREMENT_PATTERN = r"(•|\-|\*)\s*(The system shall.*)"
NON_FUNCTIONAL_PATTERN = r"(•|\-|\*)\s*(The system must.*)"
FEATURE_PATTERN = r"(•|\-|\*)\s*(Feature.*)"


def extract_requirements(file_path):
    functional_reqs = []
    non_functional_reqs = []
    features = []

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SRS file not found: {file_path}")

    content = ""

    # Handle PDF
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            content += page.get_text()
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    # Functional
    func_matches = re.findall(REQUIREMENT_PATTERN, content, re.IGNORECASE)
    functional_reqs = [match[1].strip() for match in func_matches]

    # Non-Functional
    nfr_matches = re.findall(NON_FUNCTIONAL_PATTERN, content, re.IGNORECASE)
    non_functional_reqs = [match[1].strip() for match in nfr_matches]

    # Features
    feature_matches = re.findall(FEATURE_PATTERN, content, re.IGNORECASE)
    features = [match[1].strip() for match in feature_matches]

    return functional_reqs, non_functional_reqs, features