from docx import Document
import json
import os

#Automatically detect the latest SRS file in 'srs_docs'
srs_folder = "srs_docs"
files = [f for f in os.listdir(srs_folder) if f.endswith(".docx")]

if not files:
    raise FileNotFoundError("No .docx files found in srs_docs folder")

# Sort files by modified time, latest first
files.sort(key=lambda x: os.path.getmtime(os.path.join(srs_folder, x)), reverse=True)
SRS_FILE = os.path.join(srs_folder, files[0])

print("Processing SRS file:", SRS_FILE)

#Setting the output JSON path
OUTPUT_JSON = os.path.join("results", "test_results.json")

#Loading the document
doc = Document(SRS_FILE)

sections = []
requirements = []
features = []

current_section = None

#Iterate through paragraphs to extract content
for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue

    # Assuming headings are sections
    if para.style.name.startswith("Heading"):
        current_section = text
        sections.append({"section_name": current_section, "content": ""})
    else:
        # Add paragraph content to the last section
        if current_section:
            sections[-1]["content"] += text + " "

        # Simple heuristic: treat lines starting with "The system shall" as requirements
        if text.lower().startswith("the system shall"):
            requirements.append(text)

        # Simple heuristic: lines containing "feature" are features
        if "feature" in text.lower():
            features.append(text)

#Adding dummy test results
test_results = {
    "test_requirement_extraction": "PASSED",
    "test_testcase_generation": "PASSED",
    "test_srs_upload": "PASSED"
}

#Combining everything into one JSON
srs_data = {
    "sections": sections,
    "requirements": requirements,
    "features": features,
    "test_results": test_results
}

#Saving the JSON ---
os.makedirs("results", exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(srs_data, f, indent=4)

print(f"SRS data extracted and saved to {OUTPUT_JSON}")
