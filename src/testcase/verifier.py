def verify_test_cases(test_cases, requirements):
    verified_results = []

    for tc in test_cases:
        issues = []
        score = 1.0

        req = tc.get("requirement", "").lower()
        inp = tc.get("input", "").lower()
        expected = tc.get("expected", "").lower()

        # 1. Requirement Match Check
        if not any(r.lower() in req for r in requirements):
            issues.append("Weak requirement mapping")
            score -= 0.2

        # 2. Logical Validation
        if "invalid" in inp and "success" in expected:
            issues.append("Invalid input cannot result in success")
            score -= 0.3

        if "valid" in inp and "failure" in expected:
            issues.append("Valid input should not fail")
            score -= 0.3

        # 3. Empty Fields
        if not inp or not expected:
            issues.append("Missing input/expected")
            score -= 0.3

        # 4. Duplicate Detection (basic)
        duplicate_flag = False
        for other in test_cases:
            if other != tc and other.get("input") == tc.get("input"):
                duplicate_flag = True

        if duplicate_flag:
            issues.append("Possible duplicate test case")
            score -= 0.1

        # Normalize score
        score = max(score, 0)

        verified_results.append({
            "id": tc.get("id"),
            "requirement": tc.get("requirement"),
            "input": tc.get("input"),
            "expected": tc.get("expected"),
            "technique": tc.get("technique"),
            "score": round(score, 2),
            "status": "PASSED" if score >= 0.7 else "FAILED",
            "issues": issues
        })

    return verified_results