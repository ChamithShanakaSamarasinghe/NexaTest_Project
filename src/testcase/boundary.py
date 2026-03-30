def generate_boundary_tests(requirement):
    test_cases = []

    req_lower = requirement.lower()

    # Password boundary example
    if "password" in req_lower:
        test_cases.extend([
            {
                "technique": "Boundary Value Analysis",
                "input": "7 characters",
                "expected": "Rejected"
            },
            {
                "technique": "Boundary Value Analysis",
                "input": "8 characters",
                "expected": "Accepted"
            },
            {
                "technique": "Boundary Value Analysis",
                "input": "20 characters",
                "expected": "Accepted"
            },
            {
                "technique": "Boundary Value Analysis",
                "input": "21 characters",
                "expected": "Rejected"
            }
        ])

    # Generic fallback
    if not test_cases:
        test_cases.extend([
            {
                "technique": "Boundary Value Analysis",
                "input": "minimum value",
                "expected": "Accepted"
            },
            {
                "technique": "Boundary Value Analysis",
                "input": "just below minimum",
                "expected": "Rejected"
            }
        ])

    return test_cases