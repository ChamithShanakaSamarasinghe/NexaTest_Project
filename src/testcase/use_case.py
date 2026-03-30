def generate_use_case_tests(requirement, index):
    return [
        {
            "id": f"TC_{index}_UC_1",
            "technique": "Use Case Testing",
            "requirement": requirement,
            "input": "User follows normal flow",
            "expected": "Successful extraction"
        },
        {
            "id": f"TC_{index}_UC_2",
            "technique": "Use Case Testing",
            "requirement": requirement,
            "input": "User deviates from flow",
            "expected": "Handled with proper error"
        },
    ]