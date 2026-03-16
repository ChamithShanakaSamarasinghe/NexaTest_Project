import json


def create_test_case(test_id, requirement, category, priority):
    """
    Creates a detailed test case structure
    """

    test_case = {
        "TestID": test_id,
        "Category": category,
        "Requirement": requirement,
        "Precondition": "System is running and user has access",
        "TestSteps": [
            "Open the application",
            "Navigate to the relevant feature",
            f"Perform action described in requirement: {requirement}"
        ],
        "ExpectedResult": f"The system successfully satisfies the requirement: {requirement}",
        "Priority": priority
    }

    return test_case


def generate_test_suite(functional_reqs, non_functional_reqs, features):

    test_suite = {
        "FunctionalTests": [],
        "NonFunctionalTests": [],
        "FeatureTests": []
    }

    # Functional Requirements
    for i, fr in enumerate(functional_reqs, start=1):
        test_id = f"FR-{i:03d}"
        test_case = create_test_case(test_id, fr, "Functional", "High")
        test_suite["FunctionalTests"].append(test_case)

    # Non Functional Requirements
    for i, nfr in enumerate(non_functional_reqs, start=1):
        test_id = f"NFR-{i:03d}"
        test_case = create_test_case(test_id, nfr, "NonFunctional", "Medium")
        test_suite["NonFunctionalTests"].append(test_case)

    # Features
    for i, feat in enumerate(features, start=1):
        test_id = f"FEAT-{i:03d}"
        test_case = create_test_case(test_id, feat, "Feature", "Low")
        test_suite["FeatureTests"].append(test_case)

    return test_suite


def save_test_suite(test_suite, filename="test_suite.json"):

    with open(filename, "w") as file:
        json.dump(test_suite, file, indent=4)

    print(f"[INFO] Test suite saved to {filename}")