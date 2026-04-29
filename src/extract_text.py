import os

OUTPUT_PATH = "data/output/extracted_text.txt"

def extract_text_from_pdf(pdf_path):
    # 🔥 Lazy import (FIXES VERCEL CRASH)
    import pdfplumber

    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def save_text(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    pdf_path = "data/input/OSMS_SRS.pdf"

    print("Extracting text from:", pdf_path)
    text = extract_text_from_pdf(pdf_path)

    save_text(text, OUTPUT_PATH)

    print("Extraction completed.")
    print("Saved to:", OUTPUT_PATH)
    print("\n--- TEXT PREVIEW ---\n")
    print(text[:1000])