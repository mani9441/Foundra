# ============================================================
# File: phase2_validation/main.py
# Manual runner (Part 1 only scaffold)
# ============================================================

from pprint import pprint
from state import ValidationState


def sample_input() -> ValidationState:
    return {
        "problem_statement": "Small startups struggle to validate ideas quickly.",
        "target_user_segment": "Early stage founders",
        "pain_evidence": [
            "Waste months building wrong products",
            "No structured validation process",
            "Lack market research skills"
        ],
        "existing_alternatives": [
            "Consultants",
            "Google forms",
            "Guesswork"
        ],
        "founder_solution_ideas": [
            "AI startup validation engine"
        ],
        "team_constraints": [
            "2 engineers",
            "low budget",
            "4 week MVP"
        ],
        "basic_market_context": "Growing AI SaaS market",
        "prototype_mockup_capability": "Strong backend, weak design"
    }


if __name__ == "__main__":
    state = sample_input()
    pprint(state)
    print("\nPart 1 completed: Core foundation ready.")