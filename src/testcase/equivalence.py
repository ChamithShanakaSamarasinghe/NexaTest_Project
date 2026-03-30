def generate_equivalence_tests(requirement):
    test_cases = []

    req_lower = requirement.lower()

    # Email based test cases
    if "email" in req_lower:
        test_cases.append({
            "technique": "Equivalence Partitioning",
            "input": "valid email",
            "expected": "Accepted"
        })
        test_cases.append({
            "technique": "Equivalence Partitioning",
            "input": "invalid email",
            "expected": "Rejected"
        })

    # Password based test cases
    if "password" in req_lower:
        test_cases.append({
            "technique": "Equivalence Partitioning",
            "input": "Valid password",
            "expected": "Accepted"
        })
        test_cases.append({
            "technique": "Equivalence Partitioning",
            "input": "empty password",
            "expected": "Rejected"
        })

    # Generic fallback
    if not test_cases:
        test_cases.append({
            "technique": "Equivalence Partitioning",
            "input": "invalid input",
            "expected": "Failure"
        })

    return test_cases