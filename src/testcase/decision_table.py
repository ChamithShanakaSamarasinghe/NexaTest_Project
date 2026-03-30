def generate_decision_table_tests(requirement):
    test_cases = []

    req_lower = requirement.lower()

    if "email" in req_lower and "password" in req_lower:
        test_cases.extend([
            {
                "technique": "Decision Table",
                "input": "valid email + valid password",
                "expected": "Success"
            },
            {
                "technique": "Decision Table",
                "input": "invalid email + valid password",
                "expected": "Error"
            },
            {
                "technique": "Decision Table",
                "input": "valid email + invalid password",
                "expected": "Error"
            },
            {
                "technique": "Decision Table",
                "input": "invalid email + invalid password",
                "expected": "Error"
            }
        ])

    # ✅ fallback (IMPORTANT — prevents empty output)
    if not test_cases:
        test_cases.append({
            "technique": "Decision Table",
            "input": "condition combinations",
            "expected": "System behaves correctly"
        })

    return test_cases