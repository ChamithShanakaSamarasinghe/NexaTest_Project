from test_suite_generator import generate_test_suite, save_test_suite

# Example extracted requirements
functional_reqs = [
    "The system shall allow user login",
    "The system shall allow password reset"
]

non_functional_reqs = [
    "The system must respond within 2 seconds",
    "The system must be secure against unauthorized access"
]

features = [
    "Multi-language support",
    "Dark mode option"
]

# Generate test suite
suite = generate_test_suite(functional_reqs, non_functional_reqs, features)

# Print summary
for category, tests in suite.items():
    print(f"\n--- {category} ---")
    for test in tests:
        print(f"{test['TestID']} | {test['Requirement']}")

# Save test suite
save_test_suite(suite, "generated_test_suite.json")