import sys
from src.extract_requirements import extract_requirements
from advanced_test_suite import generate_test_suite, save_test_suite


def main():

    # Checking if file path is provided
    if len(sys.argv) < 2:
        print("Usage: python run_advanced_suite.py <path_to_srs_file>")
        sys.exit(1)

    # Getting SRS file path from command line
    srs_file = sys.argv[1]

    print(f"\n[INFO] Processing SRS file: {srs_file}")

    # Extracting requirements
    functional_reqs, non_functional_reqs, features = extract_requirements(srs_file)

    # Generating test suite
    suite = generate_test_suite(functional_reqs, non_functional_reqs, features)

    # Printing summary
    for category, tests in suite.items():
        print(f"\n--- {category} ---")
        for test in tests:
            print(f"{test['TestID']} | {test['Requirement']}")

    # Saving JSON
    save_test_suite(suite, "advanced_test_suite.json")

    print("\n[INFO] Test suite saved to advanced_test_suite.json")


if __name__ == "__main__":
    main()