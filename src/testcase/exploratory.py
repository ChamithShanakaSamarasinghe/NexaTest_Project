def generate_exploratory_tests(requirement, index):
    return [
        {
            "id": f"TC_{index}_EX_1",
            "technique": "Exploratory Testing",
            "requirement": requirement,
            "input": "Random unexpected inputs",
            "expected": "System handles gracefully"
        }
    ]