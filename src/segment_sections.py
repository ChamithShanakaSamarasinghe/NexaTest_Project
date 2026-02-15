import re
import os

INPUT_TEXT_PATH = "data/output/extracted_text.txt"
OUTPUT_DIR = "data/output"
CONSOLIDATED_FILE = os.path.join(OUTPUT_DIR, "segmented_sections.txt")

SECTION_PATTERNS = {
    "Introduction": r"\n1\. Introduction",
    "Overall Description": r"\n2\. Overall Description",
    "Functional Requirements": r"\n3\. Functional Requirements",
    "Non-Functional Requirements": r"\n4\. Non-Functional Requirements"
}


def load_extracted_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_section(name, content):
    filename = f"section_{name.lower().replace(' ', '_')}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SAVED] {filepath}")


def save_all_sections(sections):
    with open(CONSOLIDATED_FILE, "w", encoding="utf-8") as f:
        for name, content in sections.items():
            f.write(f"========== {name.upper()} ==========\n\n")
            f.write(content)
            f.write("\n\n")

    print(f"[SAVED] Consolidated file: {CONSOLIDATED_FILE}")


def segment_sections(text):
    sections = {}
    keys = list(SECTION_PATTERNS.keys())

    for i, key in enumerate(keys):
        start_match = re.search(SECTION_PATTERNS[key], text)

        if not start_match:
            print(f"[WARNING] Section not found: {key}")
            continue

        start_index = start_match.start()

        if i + 1 < len(keys):
            next_match = re.search(SECTION_PATTERNS[keys[i + 1]], text)
            end_index = next_match.start() if next_match else len(text)
        else:
            end_index = len(text)

        sections[key] = text[start_index:end_index].strip()

    return sections


if __name__ == "__main__":
    print("Loading extracted text...")
    text = load_extracted_text(INPUT_TEXT_PATH)

    print("Segmenting SRS sections...")
    sections = segment_sections(text)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for name, content in sections.items():
        print(f"\n========== {name.upper()} ==========\n")
        print(content[:700])
        save_section(name, content)

    # NEW: Save consolidated output for DB ingestion
    save_all_sections(sections)

#This code is the same code I am using from SRS segmentation task in sprint 1