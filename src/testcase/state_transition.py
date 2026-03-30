def generate_state_transition_tests(requirement, index):
    return [
        {
            "id": f"TC_{index}_ST_1",
            "technique": "State Transition Testing",
            "requirement": requirement,
            "input": "Initial → Action → Next State",
            "expected": "Correct state transition"
        }
    ]