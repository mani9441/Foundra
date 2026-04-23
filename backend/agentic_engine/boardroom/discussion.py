# ===============================================================
# FILE: boardroom/discussion.py
# REAL-TIME EXECUTIVE WAR ROOM (TERMINAL MODE)
#
# Features:
# - live terminal board meeting feel
# - executives join room
# - thinking indicators
# - real conversational rounds
# - transcript capture
# - strategic final resolution
#
# Depends:
#   boardroom/core.py
#   boardroom/executives.py
# ===============================================================

from __future__ import annotations

import time
from typing import Dict, Any, List

from ..boardroom.core import (
    Role,
    BoardState,
    Sentiment,
    add_message,
    add_action,
    new_message
)

from ..executive_agents.executives import build_executive_team


# ===============================================================
# TERMINAL SETTINGS
# ===============================================================

LIVE_MODE = True
THINK_DELAY = 0.8
SPEAK_DELAY = 0.4


# ===============================================================
# UTILITIES
# ===============================================================

def slow_print(text: str, delay: float = SPEAK_DELAY):
    print(text, flush=True)
    if LIVE_MODE:
        time.sleep(delay)


def announce(text: str):
    slow_print(f"\n{text}\n", 0.5)


def role_tag(role: Role):
    return f"[{role.value}]"


def terminal_message(role: Role, text: str):
    slow_print(f"{role_tag(role)} {text}")


def terminal_thinking(role: Role):
    slow_print(f"{role_tag(role)} thinking...", THINK_DELAY)


def save_msg(
    state: BoardState,
    role: Role,
    text: str,
    mood=Sentiment.NEUTRAL
):
    add_message(
        state,
        new_message(
            speaker=role,
            round_no=state.round_no,
            content=text,
            sentiment=mood
        )
    )


def latest_role_msg(state: BoardState, role: Role):

    for m in reversed(state.messages):
        if m.speaker == role:
            return m.content

    return ""


# ===============================================================
# ROOM ENTRY
# ===============================================================

def open_room(state: BoardState):

    announce("=" * 60)
    announce("FOUNDRA EXECUTIVE BOARD ROOM")
    announce("=" * 60)

    slow_print(f"Startup : {state.startup_name}")
    slow_print(f"Phase   : {state.phase}")
    slow_print(f"Agenda  : {state.agenda}")

    announce("Executives entering room...")

    for role in [
        Role.CEO,
        Role.CTO,
        Role.CFO,
        Role.CMO,
        Role.COO
    ]:
        slow_print(f"{role_tag(role)} joined.")

    announce("Meeting begins.")


# ===============================================================
# ROUND 1 - OPENING POSITIONS
# ===============================================================

def round_opening(state: BoardState, team):

    state.round_no += 1
    announce("ROUND 1 — OPENING POSITIONS")

    order = [
        Role.CEO,
        Role.CTO,
        Role.CFO,
        Role.CMO,
        Role.COO
    ]

    for role in order:

        terminal_thinking(role)

        before = len(state.messages)

        team[role].think(state)

        if len(state.messages) > before:
            msg = state.messages[-1].content
            terminal_message(role, msg)


# ===============================================================
# ROUND 2 - DIRECT CHALLENGES
# ===============================================================

def round_challenges(state: BoardState, team):

    state.round_no += 1
    announce("ROUND 2 — CHALLENGES")

    matchups = [
        (Role.CTO, Role.CEO),
        (Role.CFO, Role.CMO),
        (Role.CMO, Role.CFO),
        (Role.COO, Role.CEO),
        (Role.CEO, Role.CTO)
    ]

    for role, target in matchups:

        terminal_thinking(role)

        target_text = latest_role_msg(state, target)

        before = len(state.messages)

        team[role].think(
            state,
            target=f"{target.value} said: {target_text}"
        )

        if len(state.messages) > before:
            msg = state.messages[-1].content
            terminal_message(role, msg)


# ===============================================================
# ROUND 3 - STRATEGIC CONVERGENCE
# ===============================================================

def round_convergence(state: BoardState, team):

    state.round_no += 1
    announce("ROUND 3 — STRATEGIC CONVERGENCE")

    prompts = {
        Role.CTO: "Best simplified build path?",
        Role.CFO: "Safest commercial path?",
        Role.CMO: "Best growth wedge?",
        Role.COO: "Best execution model?",
        Role.CEO: "Final synthesis."
    }

    for role in [
        Role.CTO,
        Role.CFO,
        Role.CMO,
        Role.COO,
        Role.CEO
    ]:

        terminal_thinking(role)

        before = len(state.messages)

        team[role].think(
            state,
            target=prompts[role]
        )

        if len(state.messages) > before:
            msg = state.messages[-1].content
            terminal_message(role, msg)


# ===============================================================
# FINAL RESOLUTION
# ===============================================================

def final_resolution(state: BoardState):

    announce("=" * 60)
    announce("FINAL BOARD RESOLUTION")
    announce("=" * 60)

    ceo_last = latest_role_msg(state, Role.CEO)

    final_text = (
        "After hearing every side, "
        "we move with discipline.\n\n"
        f"{ceo_last}"
    )

    terminal_message(Role.CEO, final_text)

    save_msg(
        state,
        Role.CEO,
        final_text,
        Sentiment.SUPPORT
    )

    add_action(
        state,
        "COO",
        "Convert board outcome into execution sprint",
        "24h",
        "HIGH"
    )

    add_action(
        state,
        "Operational Layer",
        "Apply critiques and regenerate next phase output",
        "Immediate",
        "HIGH"
    )

    add_action(
        state,
        "CEO Office",
        "Review progress in next board session",
        "72h",
        "MEDIUM"
    )


# ===============================================================
# OUTPUT PACKER
# ===============================================================

def build_output(state: BoardState):

    transcript = [
        f"{m.speaker.value}: {m.content}"
        for m in state.messages
    ]

    return {
        "meeting_title": "Foundra Executive Board Room",
        "phase": state.phase,
        "agenda": state.agenda,
        "transcript": transcript,
        "actionables": [
            {
                "owner": a.owner,
                "task": a.task,
                "deadline": a.deadline,
                "priority": a.priority
            }
            for a in state.action_items
        ]
    }


# ===============================================================
# MAIN
# ===============================================================

def run_full_board_meeting(state: BoardState):

    team = build_executive_team()

    open_room(state)

    round_opening(state, team)

    round_challenges(state, team)

    round_convergence(state, team)

    final_resolution(state)

    announce("Meeting adjourned.")

    return state


# ===============================================================
# ENTRY NODE
# ===============================================================

def boardroom_node(payload: Dict[str, Any]):

    state = BoardState(
        startup_name=payload["startup_name"],
        startup_stage=payload["startup_stage"],
        phase=payload["phase"],
        agenda=payload.get(
            "agenda",
            "Strategic Review"
        ),
        reports=payload["reports"],
        metrics=payload.get("metrics", {})
    )

    final_state = run_full_board_meeting(state)

    return build_output(final_state)