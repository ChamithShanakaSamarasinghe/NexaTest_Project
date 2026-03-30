from .equivalence import generate_equivalence_tests
from .boundary import generate_boundary_tests
from .decision_table import generate_decision_table_tests
from .state_transition import generate_state_transition_tests
from .use_case import generate_use_case_tests
from .exploratory import generate_exploratory_tests


def generate_test_cases(requirements):
    all_cases = []

    for index, req in enumerate(requirements, start=1):
        eq = generate_equivalence_tests(req)
        bva = generate_boundary_tests(req)
        dt = generate_decision_table_tests(req)
        st = generate_state_transition_tests(req, index)
        uc = generate_use_case_tests(req, index)
        ex = generate_exploratory_tests(req, index)

        combined = eq + bva + dt + st + uc + ex

        for i, tc in enumerate(combined, start=1):
            tc["id"] = tc.get("id", f"TC_{index}_{i}")
            tc["requirement"] = req
            tc["technique"] = tc.get("technique", "Unknown")

        all_cases.extend(combined)

    return all_cases