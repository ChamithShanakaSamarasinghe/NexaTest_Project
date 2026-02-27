import re
import yaml
from typing import Dict


class RuleEngine:
    """
    Applies regex-based semantic rules.
    """

    def __init__(self, config_path="config/rules.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.rules = self.config.get("rules", [])

    def apply_rules(self, token_frequencies: Dict[str, int]) -> Dict[str, str]:
        """
        Map tokens to categories using regex rules.
        """
        mappings = {}

        for token in token_frequencies.keys():
            for rule in self.rules:
                if re.search(rule["pattern"], token):
                    mappings[token] = rule["category"]

        return mappings


# Test block
if __name__ == "__main__":
    sample_tokens = {
        "ai": 3,
        "software": 2,
        "price": 1,
        "today": 4,
        "tree": 2
    }

    engine = RuleEngine()
    result = engine.apply_rules(sample_tokens)

    print("Rule Mappings:")
    for k, v in result.items():
        print(k, "=>", v)
