# ============================================================
# File: phase2_validation/tools_atomic/survey_generator.py
# Atomic Tool
# ============================================================

from typing import Dict, Any, List
from langchain.tools import tool


@tool("survey_generator_tool")
def survey_generator_tool(problem: str) -> Dict[str, Any]:
    """
    Generate validation survey questions.
    """

    return {
        "problem": problem,
        "questions": [
            "How often do you face this issue?",
            "How do you solve it today?",
            "How painful is this problem (1-10)?",
            "Would you pay for a solution?",
            "What would make you switch?"
        ]
    }