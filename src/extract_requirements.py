import os
import re
import fitz  # PyMuPDF

# Updated patterns (stop capture at next bullet or period)
REQUIREMENT_PATTERN = r"The system shall[^.]*\."
NON_FUNCTIONAL_PATTERN = r"The system must[^.]*\."
FEATURE_PATTERN = r"Feature[^.]*\."


def extract_requirements(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SRS file not found: {file_path}")

    content = ""

    # Reading Files
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            content += page.get_text()
        doc.close()
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

    # Cleaning text
    content = content.replace("\n", " ")
    content = re.sub(r"\s+", " ", content)

    # Extracting Requirements
    functional_matches = re.findall(REQUIREMENT_PATTERN, content, re.IGNORECASE)
    non_functional_matches = re.findall(NON_FUNCTIONAL_PATTERN, content, re.IGNORECASE)
    feature_matches = re.findall(FEATURE_PATTERN, content, re.IGNORECASE)

    # Removing duplicates and cleaning
    functional_reqs = list(set([req.strip() for req in functional_matches if req.strip()]))
    non_functional_reqs = list(set([req.strip() for req in non_functional_matches if req.strip()]))
    features = list(set([req.strip() for req in feature_matches if req.strip()]))

    return functional_reqs, non_functional_reqs, features