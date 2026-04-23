# ===============================================================
# FILE: boardroom/executives.py
# NATURAL SPEECH MODE (OLLAMA / LOCAL MODEL FRIENDLY)
#
# No JSON parser
# No structured output dependency
# Real executive speech
# Hidden vote extraction from text
# Best for Ollama / local models
# ===============================================================

from __future__ import annotations

import re
import json
from typing import Optional, List

from langchain_classic.prompts import ChatPromptTemplate

from ..boardroom.core import (
    Role,
    Sentiment,
    DecisionType,
    Vote,
    BoardState,
    add_vote,
    add_message,
    new_message,
    detect_pressure
)

# IMPORTANT:
# Replace below import with your own llm wrapper if needed
from ..LLMs.llm import get_llm


# ===============================================================
# MEMORY
# ===============================================================

class Memory:

    def __init__(self):
        self.logs: List[str] = []

    def add(self, text: str):
        self.logs.append(text)

    def recent(self, n=5):
        return self.logs[-n:]


# ===============================================================
# PERSONALITIES
# ===============================================================

PROFILES = {
    Role.CEO: {
        "style": "Founder. Sharp. Strategic. Decisive.",
        "goal": "Choose direction and win market."
    },

    Role.CTO: {
        "style": "Engineering realist. Skeptical. Practical.",
        "goal": "Ship what is possible, reject fantasy."
    },

    Role.CFO: {
        "style": "Cold numbers thinker. Risk aware.",
        "goal": "Protect runway and economics."
    },

    Role.CMO: {
        "style": "Aggressive growth operator.",
        "goal": "Acquire customers and create momentum."
    },

    Role.COO: {
        "style": "Execution disciplinarian.",
        "goal": "Owners, systems, deadlines."
    }
}


# ===============================================================
# PARSING HELPERS
# ===============================================================

VALID_VOTES = [
    "APPROVE",
    "REJECT",
    "REVISE",
    "PRIORITIZE",
    "DELAY",
    "PIVOT"
]


def extract_vote(text: str) -> DecisionType:

    upper = text.upper()

    for vote in VALID_VOTES:
        if f"[VOTE:{vote}]" in upper:
            return DecisionType(vote)

    # fallback keyword scan
    if "APPROVE" in upper:
        return DecisionType.APPROVE

    if "REJECT" in upper:
        return DecisionType.REJECT

    if "PIVOT" in upper:
        return DecisionType.PIVOT

    return DecisionType.REVISE


def clean_message(text: str) -> str:

    text = re.sub(
        r"\[VOTE:.*?\]",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def detect_sentiment(text: str) -> Sentiment:

    t = text.lower()

    if any(x in t for x in [
        "disagree",
        "wrong",
        "risk",
        "cannot",
        "oppose"
    ]):
        return Sentiment.OPPOSE

    if any(x in t for x in [
        "strong",
        "good",
        "support",
        "agree"
    ]):
        return Sentiment.SUPPORT

    return Sentiment.NEUTRAL


# ===============================================================
# BASE AGENT
# ===============================================================

class ExecutiveAgent:

    def __init__(
        self,
        role: Role,
        temperature: float = 0.5
    ):

        self.role = role
        self.profile = PROFILES[role]
        self.memory = Memory()

        self.llm = get_llm(
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
You are a REAL startup executive in a live board meeting.

Never sound like AI.
Never output JSON.
Speak naturally like a human leader.

Your role: {role}

Style:
{style}

Goal:
{goal}

Rules:
1. Speak in 1-3 sharp sentences.
2. React to report details.
3. If another executive is wrong, challenge them.
4. Mention concrete risks/opportunities.
5. Sound like your role.
6. End with exactly one vote tag.

Allowed tags:
[VOTE:APPROVE]
[VOTE:REJECT]
[VOTE:REVISE]
[VOTE:PRIORITIZE]
[VOTE:DELAY]
[VOTE:PIVOT]
"""
            ),
            (
                "human",
                """
Startup: {startup_name}
Stage: {startup_stage}
Phase: {phase}
Agenda: {agenda}

Pressure: {pressure}

Operational Reports:
{reports}

Recent Transcript:
{messages}

Memory:
{memory}

Direct Target:
{target}

Speak now.
"""
            )
        ])

        self.chain = self.prompt | self.llm

    # ===========================================================
    # THINK
    # ===========================================================

    def think(
        self,
        state: BoardState,
        target: Optional[str] = None
    ):

        transcript = [
            f"{m.speaker.value}: {m.content}"
            for m in state.messages[-10:]
        ]

        pressure = detect_pressure(state.metrics)

        raw = self.chain.invoke({
            "role": self.role.value,
            "style": self.profile["style"],
            "goal": self.profile["goal"],
            "startup_name": state.startup_name,
            "startup_stage": state.startup_stage,
            "phase": state.phase,
            "agenda": state.agenda,
            "pressure": pressure.value,
            "reports": json.dumps(
                state.reports,
                indent=2
            ),
            "messages": "\n".join(transcript),
            "memory": "\n".join(
                self.memory.recent()
            ),
            "target": target or "None"
        })

        # some models return object
        text = getattr(raw, "content", raw)
        text = str(text)

        vote = extract_vote(text)
        speech = clean_message(text)
        sentiment = detect_sentiment(speech)

        add_message(
            state,
            new_message(
                speaker=self.role,
                round_no=state.round_no,
                content=speech,
                sentiment=sentiment
            )
        )

        add_vote(
            state,
            Vote(
                role=self.role,
                vote=vote,
                confidence=7,
                reason="Natural executive judgment."
            )
        )

        self.memory.add(speech)


# ===============================================================
# SPECIALISTS
# ===============================================================

class CEOAgent(ExecutiveAgent):
    def __init__(self):
        super().__init__(
            Role.CEO,
            temperature=0.4
        )


class CTOAgent(ExecutiveAgent):
    def __init__(self):
        super().__init__(
            Role.CTO,
            temperature=0.3
        )


class CFOAgent(ExecutiveAgent):
    def __init__(self):
        super().__init__(
            Role.CFO,
            temperature=0.2
        )


class CMOAgent(ExecutiveAgent):
    def __init__(self):
        super().__init__(
            Role.CMO,
            temperature=0.6
        )


class COOAgent(ExecutiveAgent):
    def __init__(self):
        super().__init__(
            Role.COO,
            temperature=0.3
        )


# ===============================================================
# FACTORY
# ===============================================================

def build_executive_team():

    return {
        Role.CEO: CEOAgent(),
        Role.CTO: CTOAgent(),
        Role.CFO: CFOAgent(),
        Role.CMO: CMOAgent(),
        Role.COO: COOAgent()
    }