# ================================================================
# boardroom/matrix.py  |  FINAL
#
# 5×5 Agreement Matrix Engine.
# No LangChain memory — just a prompt per cell.
# Each exec reviews every other exec's Round 1 position.
# ================================================================

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from langchain_core.prompts import ChatPromptTemplate

from ..boardroom.core import (
    Role, BoardState, MatrixCell,
    get_priority_agent, last_message
)
from ..LLMs.llm import get_llm


MATRIX_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are {reviewer_role} in a board meeting. Your goal: {reviewer_goal}\n"
     "Read the position below from {target_role}.\n"
     "Respond with EXACTLY two lines — nothing else:\n"
     "AGREEMENT: AGREE or DISAGREE\n"
     "REASON: one sentence from your role's perspective."
    ),
    ("human",
     "Phase: {phase} | Startup: {startup_name}\n\n"
     "{target_role} said:\n{target_position}\n\n"
     "Fill both lines now."
    )
])


ROLE_GOALS = {
    Role.CEO: "Win the market. Set the right strategy.",
    Role.CTO: "Ship what is technically feasible. Cut what isn't.",
    Role.CFO: "Protect runway. Validate unit economics.",
    Role.CMO: "Acquire first paying customers. Build momentum.",
    Role.COO: "Turn decisions into owned tasks with deadlines.",
}


def _parse_cell(text: str) -> Tuple[str, str]:
    upper     = text.upper()
    agreement = "DISAGREE"

    if "AGREEMENT: AGREE" in upper:
        agreement = "AGREE"
    elif "AGREEMENT: DISAGREE" in upper:
        agreement = "DISAGREE"
    elif upper.count("AGREE") > upper.count("DISAGREE"):
        agreement = "AGREE"

    reason_match = re.search(r"REASON\s*[:\-]\s*(.+)", text, re.IGNORECASE)
    reason = reason_match.group(1).strip()[:200] if reason_match else text.strip()[:200]

    return agreement, reason


def build_agreement_matrix(state: BoardState, llm=None) -> List[MatrixCell]:
    if llm is None:
        llm = get_llm()

    chain  = MATRIX_PROMPT | llm
    roles  = list(Role)
    cells: List[MatrixCell] = []

    for reviewer in roles:
        for target in roles:
            if reviewer == target:
                continue

            target_position = last_message(state, target)
            if not target_position:
                continue

            raw = chain.invoke({
                "reviewer_role":   reviewer.value,
                "reviewer_goal":   ROLE_GOALS[reviewer],
                "target_role":     target.value,
                "target_position": target_position[:350],
                "phase":           state.phase,
                "startup_name":    state.startup_name,
            })

            text      = str(getattr(raw, "content", raw)).strip()
            agreement, reason = _parse_cell(text)

            cells.append(MatrixCell(
                reviewer=reviewer,
                target=target,
                agreement=agreement,
                reason=reason,
            ))

    state.agreement_matrix = cells
    return cells


def matrix_to_dict(cells: List[MatrixCell]) -> Dict[str, Any]:
    roles = [r.value for r in Role]
    grid: Dict[str, Dict] = {r: {} for r in roles}

    for cell in cells:
        grid[cell.reviewer.value][cell.target.value] = {
            "agreement": cell.agreement,
            "reason":    cell.reason,
        }

    return grid


def get_disagreements(cells: List[MatrixCell]) -> List[Tuple[Role, Role, str]]:
    """Returns list of (reviewer, target, reason) for all DISAGREE cells."""
    return [
        (c.reviewer, c.target, c.reason)
        for c in cells if c.agreement == "DISAGREE"
    ]


def get_priority_conflicts(cells: List[MatrixCell], phase: str) -> List[Tuple[Role, str]]:
    """Returns (target, reason) where priority agent DISAGREES."""
    priority  = get_priority_agent(phase)
    return [
        (c.target, c.reason)
        for c in cells
        if c.reviewer == priority and c.agreement == "DISAGREE"
    ]


def print_matrix(cells: List[MatrixCell], phase: str):
    roles    = list(Role)
    priority = get_priority_agent(phase)

    header = "          " + "  ".join(f"{r.value:<7}" for r in roles)
    print(f"\n{header}")
    print("  " + "─" * (len(header) - 2))

    for reviewer in roles:
        star = "★" if reviewer == priority else " "
        row  = f"  {star}{reviewer.value:<6}"
        for target in roles:
            if reviewer == target:
                row += "   —      "
            else:
                cell = next(
                    (c for c in cells if c.reviewer == reviewer and c.target == target),
                    None
                )
                symbol = "✓" if (cell and cell.agreement == "AGREE") else "✗"
                row   += f"   {symbol}      "
        print(row)

    print(f"\n  ★ = Priority agent ({priority.value})")