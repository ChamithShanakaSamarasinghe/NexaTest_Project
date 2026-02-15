import os
import re

INPUT_FILE = "data/output/section_functional_requirements.txt"
OUTPUT_FILE = "data/output/atomic_requirements.txt"

REQUIREMENT_PATTERN = r"(•|\-|\*)\s*(The system shall.*)"

def extract_requirements(text):
    matches = re.findall(REQUIREMENT_PATTERN, text, re.IGNORECASE)
    return [match[1].strip() for match in matches]


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError("Functional requirements section not found.")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    requirements = extract_requirements(content)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, req in enumerate(requirements, start=1):
            f.write(f"{i}. {req}\n")

    print(f"[DONE] Extracted {len(requirements)} atomic requirements")

#This code is the same code I am using from SRS segmentation task in sprint 1