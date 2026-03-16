import json

#Helper function created to generate dynamic test steps based on requirement type
def generate_test_steps(req_type, requirement):
    steps = []
    if req_type == "Functional":
        steps = [
            "Open the application",
            "Navigate to the relevant feature",
            f"Perform action described in requirement: {requirement}",
            "Verify the action succeeds"
        ]

    elif req_type == "NonFunctional":
        steps = [
            "Open the application",
            "Perform action relevant to the requirement",
            f"Measure or validate: {requirement}",
            "Verify requirement is met"
        ]

    elif req_type == "Feature":
        steps = [
            "Open the application",
            "Navigate to the feature or settings",
            f"Verify feature works as decribed: {requirement}"
        ]
    return steps

#Helper function to generate edge cases
def genrate_edge_cases(req_type, requirement):
    edge_cases = []
    if req_type == "Functional":
        edge_cases = [
            f"Test invalid input for: {requirement}",
            f"Test maximum input length for: {requirement}"
        ]
    elif req_type == "NonFunctional":
        edge_cases = [
            f"Test system under load for: {requirement}",
            f"Test system under peak usage for: {requirement}"
        ]
    elif req_type == "Feature":
        edge_cases = [
            f"Test feature with unusual settings: {requirement}",
            f"Test feature under maximum limits: {requirement}"
        ]
    return edge_cases

#Creating a detailed test case
def create_test_case(test_id, requirement, category, priority):
    return {
        "TestID": test_id,
        "Category": category,
        "Requirement": requirement,
        "Precondition": "System is running and user has access",
        "TestSteps": generate_test_steps(category, requirement),
        "ExpectedResult": f"The system successfully satisfies the requirement: {requirement}",
        "EdgeCases": genrate_edge_cases(category, requirement),
        "Priority": priority
    }

# Main function to generate the full test suite
def generate_test_suite(functional_reqs, non_functional_reqs, features):
    suite = {
        "FunctionalTests": [],
        "NonFunctionalTests": [],
        "FeatureTests": []
    }

    for i, fr in enumerate(functional_reqs, start=1):
        suite["FunctionalTests"].append(create_test_case(f"FR-{i:03d}", fr, "Functional", "High"))

    for i, nfr in enumerate(non_functional_reqs, start=1):
        suite["NonFunctionalTests"].append(create_test_case(f"NFR-{i:03d}", nfr, "NonFunctional", "Medium"))

    for i, feat in enumerate(features, start=1):
        suite["FeatureTests"].append(create_test_case(f"FEAT-{i:03d}", feat, "Feature", "Low"))

    return suite

# Save test suite to JSON
def save_test_suite(test_suite, filename="advanced_test_suite.json"):
    with open(filename, "w") as f:
        json.dump(test_suite, f, indent=4)
    print(f"[INFO] Test suite saved to {filename}")