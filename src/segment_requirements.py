import os
import re

INPUT_SECTION_PATH = "data/output/section_functional_requirements.txt"
OUTPUT_PATH = "data/output/functional_requirements.txt"


def load_functional_section(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_requirements(text):
    """
    Extracts 'The system shall ...' statements using regex
    """
    pattern = r"The system shall .*?(?:\.|\n)"
    requirements = re.findall(pattern, text, re.IGNORECASE)
    return [r.strip() for r in requirements]


def save_requirements(requirements, path):
    with open(path, "w", encoding="utf-8") as f:
        for req in requirements:
            f.write(req + "\n")


if __name__ == "__main__":
    print("Loading Functional Requirements section...")
    text = load_functional_section(INPUT_SECTION_PATH)

    print("Extracting individual requirements...")
    requirements = extract_requirements(text)

    print(f"Total requirements extracted: {len(requirements)}\n")

    for r in requirements:
        print("-", r)

    save_requirements(requirements, OUTPUT_PATH)
    print("\n[SAVED] Functional requirements saved to:", OUTPUT_PATH)

#This code is the same code I am using from SRS segmentation task in sprint 1