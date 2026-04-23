# ============================================================
# File: phase2_validation/agents/icp_agent.py
# ============================================================

from typing import Dict, Any

from backend.agentic_engine.LLMs.llm import get_llm
from ..prompts import SYSTEM_ANALYST, ICP_PROMPT
from ..utils.json_parser import extract_json

from ..tools.medium.persona_builder_tool import run_persona_builder


def run_icp_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Output:
    state["icp"]
    """

    llm = get_llm()

    persona = run_persona_builder(
        state["problem_statement"],
        state["target_user_segment"],
        state["pain_evidence"]
    )

    prompt = ICP_PROMPT.format(
        problem=state["problem_statement"],
        users=state["target_user_segment"],
        pain=state["pain_evidence"]
    )

    result = llm.invoke(
        [
            ("system", SYSTEM_ANALYST),
            ("human", prompt)
        ]
    )

    data = extract_json(result.content)
    data["persona_model"] = persona

    state["icp"] = data
    return state