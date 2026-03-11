# test_srs_extractor.py
import os
import sys
import argparse
from pathlib import Path

from src.srs_extractor.requirement_feature_extractor import SRSExtractor

DEFAULT_CANDIDATES = ["sample_srs.pdf", "sample.pdf", "sample.docx", "sample.doc"]

def find_srs_file(provided_path: str | None) -> str | None:
    # If user provided a path, use it (but check it exists)
    if provided_path:
        p = Path(provided_path)
        if p.exists():
            return str(p)
        return None

    # Otherwise try default candidates in current directory
    cwd = Path.cwd()
    for name in DEFAULT_CANDIDATES:
        p = cwd / name
        if p.exists():
            return str(p)

    return None

def list_files_in_cwd():
    cwd = Path.cwd()
    files = [f.name for f in cwd.iterdir() if f.is_file()]
    return files

def main():
    parser = argparse.ArgumentParser(description="Run SRS extractor and save results.")
    parser.add_argument("file", nargs="?", help="Path to SRS PDF/DOCX (optional).")
    args = parser.parse_args()

    file_path = find_srs_file(args.file)
    if not file_path:
        print("Error: No SRS file found.")
        print("Searched for (in this directory):", ", ".join(DEFAULT_CANDIDATES))
        print("Files present in current folder:")
        for fn in list_files_in_cwd():
            print("  -", fn)
        print("\nDo one of the following")
        print("  1) Place the SRS file needed so that it can be named as the default, or")
        print("  2) Run this script with the file path, e.g.:")
        print("       python test_srs_extractor.py sample.pdf")
        sys.exit(1)

    print(f"Using SRS file: {file_path}\n")

    extractor = SRSExtractor()

    try:
        results = extractor.extract(file_path)

        functional_count = len(results.get("functional_requirements", []))
        nfr_count = len(results.get("non_functional_requirements", []))
        feature_count = len(results.get("features", []))

        print("\n===================================")
        print("      SRS ANALYSIS COMPLETED")
        print("===================================")
        print(f"Functional Requirements      : {functional_count}")
        print(f"Non Functional Requirements  : {nfr_count}")
        print(f"Extracted Features           : {feature_count}")
        print("\nOutput file saved successfully.")
        print("Database updated successfully.")
        print("===================================\n")

    except FileNotFoundError as e:
        print("File error:", e)
        print("Make sure the file exists and the path is correct.")
    except Exception as e:
        print("An error occurred during extraction:")
        print(e)

if __name__ == "__main__":
    main()