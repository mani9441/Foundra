# ===============================================================
# UPGRADE 1/3
# FILE: boardroom/core.py
# FINAL PRODUCTION VERSION
#
# Upgrades:
# - phase aware state
# - weighted voting
# - dominant roles per phase
# - iteration tracking
# - secretary circuit breaker flags
# - approval thresholds
# - richer serializers
# ===============================================================

from __future__ import annotations

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


# ===============================================================
# ENUMS
# ===============================================================

class Role(str, Enum):
    CEO = "CEO"
    CTO = "CTO"
    CFO = "CFO"
    CMO = "CMO"
    COO = "COO"


class Sentiment(str, Enum):
    SUPPORT = "SUPPORT"
    NEUTRAL = "NEUTRAL"
    OPPOSE = "OPPOSE"


class DecisionType(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REVISE = "REVISE"
    PRIORITIZE = "PRIORITIZE"
    DELAY = "DELAY"
    PIVOT = "PIVOT"
    FORCED_COMPROMISE = "FORCED_COMPROMISE"


class PressureState(str, Enum):
    CALM = "CALM"
    URGENT = "URGENT"
    DEFENSIVE = "DEFENSIVE"
    AGGRESSIVE = "AGGRESSIVE"


# ===============================================================
# PHASE MAP
# ===============================================================

PHASE_ROLE_WEIGHT = {
    "validation": {
        Role.CEO: 1.4,
        Role.CMO: 1.3,
        Role.CFO: 1.0,
        Role.CTO: 1.0,
        Role.COO: 1.0
    },

    "market": {
        Role.CMO: 1.4,
        Role.CEO: 1.2,
        Role.CFO: 1.2,
        Role.CTO: 1.0,
        Role.COO: 1.0
    },

    "business_model": {
        Role.CFO: 1.4,
        Role.CEO: 1.3,
        Role.CMO: 1.1,
        Role.CTO: 1.0,
        Role.COO: 1.0
    },

    "product": {
        Role.CTO: 1.5,
        Role.COO: 1.3,
        Role.CEO: 1.2,
        Role.CFO: 1.0,
        Role.CMO: 1.0
    },

    "gtm": {
        Role.CMO: 1.5,
        Role.CEO: 1.2,
        Role.COO: 1.2,
        Role.CFO: 1.0,
        Role.CTO: 1.0
    }
}


PHASE_APPROVAL_THRESHOLD = {
    "validation": 6.8,
    "market": 7.0,
    "business_model": 7.4,
    "product": 7.5,
    "gtm": 7.4
}


# ===============================================================
# DATA MODELS
# ===============================================================

@dataclass
class BoardMessage:
    id: str
    speaker: Role
    round_no: int
    content: str
    sentiment: Sentiment
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )
    reply_to: Optional[str] = None


@dataclass
class Vote:
    role: Role
    vote: DecisionType
    confidence: int
    reason: str
    weight: float = 1.0


@dataclass
class ActionItem:
    owner: str
    task: str
    deadline: str
    priority: str = "MEDIUM"


@dataclass
class BoardState:
    startup_name: str
    startup_stage: str

    phase: str
    agenda: str

    reports: Dict[str, Any]
    metrics: Dict[str, Any]

    round_no: int = 0
    iteration_count: int = 0
    max_rounds: int = 4
    max_iterations: int = 3

    approval_threshold: float = 7.0

    forced_compromise_triggered: bool = False

    messages: List[BoardMessage] = field(default_factory=list)
    votes: List[Vote] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)

    final_decision: Optional[DecisionType] = None
    decision_reason: Optional[str] = None

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


# ===============================================================
# HELPERS
# ===============================================================

def new_message(
    speaker: Role,
    round_no: int,
    content: str,
    sentiment: Sentiment = Sentiment.NEUTRAL,
    reply_to: Optional[str] = None
) -> BoardMessage:

    return BoardMessage(
        id=str(uuid.uuid4()),
        speaker=speaker,
        round_no=round_no,
        content=content,
        sentiment=sentiment,
        reply_to=reply_to
    )


def add_message(state: BoardState, msg: BoardMessage):
    state.messages.append(msg)


def get_role_weight(
    phase: str,
    role: Role
) -> float:

    return PHASE_ROLE_WEIGHT.get(
        phase,
        {}
    ).get(role, 1.0)


def add_vote(
    state: BoardState,
    vote: Vote
):
    vote.weight = get_role_weight(
        state.phase,
        vote.role
    )

    state.votes = [
        v for v in state.votes
        if v.role != vote.role
    ]

    state.votes.append(vote)


def add_action(
    state: BoardState,
    owner: str,
    task: str,
    deadline: str,
    priority: str = "MEDIUM"
):
    state.action_items.append(
        ActionItem(
            owner=owner,
            task=task,
            deadline=deadline,
            priority=priority
        )
    )


# ===============================================================
# PRESSURE ENGINE
# ===============================================================

def detect_pressure(
    metrics: Dict[str, Any]
) -> PressureState:

    runway = metrics.get("runway_months", 6)
    competitor = metrics.get("competitor_pressure", False)
    growth = metrics.get("growth_rate", 0)

    if runway <= 3:
        return PressureState.DEFENSIVE

    if competitor:
        return PressureState.URGENT

    if growth >= 20:
        return PressureState.AGGRESSIVE

    return PressureState.CALM


# ===============================================================
# VOTE ENGINE
# ===============================================================

def weighted_vote_score(
    state: BoardState
) -> Dict[str, float]:

    scores = {}

    for v in state.votes:

        base = v.weight * (v.confidence / 10)

        scores[v.vote.value] = (
            scores.get(v.vote.value, 0) + base
        )

    return scores


def resolve_final_decision(
    state: BoardState
) -> DecisionType:

    if not state.votes:
        state.final_decision = DecisionType.REVISE
        return state.final_decision

    scores = weighted_vote_score(state)

    winner = max(scores, key=scores.get)

    state.final_decision = DecisionType(winner)
    state.decision_reason = (
        f"Weighted board consensus selected {winner}."
    )

    return state.final_decision


def approval_score(
    state: BoardState
) -> float:

    if not state.votes:
        return 0.0

    total = 0.0

    for v in state.votes:
        total += v.weight * (v.confidence / 10)

    return round(total / len(state.votes), 2)


def is_approved(
    state: BoardState
) -> bool:

    score = approval_score(state)

    if state.final_decision in [
        DecisionType.APPROVE,
        DecisionType.PRIORITIZE,
        DecisionType.FORCED_COMPROMISE
    ]:
        return True

    if score >= state.approval_threshold:
        return True

    return False


# ===============================================================
# SERIALIZER
# ===============================================================

def board_to_dict(
    state: BoardState
) -> Dict[str, Any]:

    return {
        "startup_name": state.startup_name,
        "startup_stage": state.startup_stage,
        "phase": state.phase,
        "agenda": state.agenda,
        "round_no": state.round_no,
        "iteration_count": state.iteration_count,
        "approval_threshold": state.approval_threshold,

        "messages": [
            {
                "speaker": m.speaker.value,
                "round": m.round_no,
                "content": m.content,
                "sentiment": m.sentiment.value
            }
            for m in state.messages
        ],

        "votes": [
            {
                "role": v.role.value,
                "vote": v.vote.value,
                "confidence": v.confidence,
                "weight": v.weight,
                "reason": v.reason
            }
            for v in state.votes
        ],

        "final_decision": (
            state.final_decision.value
            if state.final_decision else None
        ),

        "decision_reason": state.decision_reason,

        "approved": is_approved(state),

        "actions": [
            {
                "owner": a.owner,
                "task": a.task,
                "deadline": a.deadline,
                "priority": a.priority
            }
            for a in state.action_items
        ]
    }