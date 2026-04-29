# ================================================================
# boardroom/core.py  |  FINAL
#
# No LangChain imports anywhere in this file.
# Pure Python dataclasses and enums.
# Universal — works for any startup idea, any phase.
# ================================================================

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


# ----------------------------------------------------------------
# ENUMS
# ----------------------------------------------------------------

class Role(str, Enum):
    CEO = "CEO"
    CTO = "CTO"
    CFO = "CFO"
    CMO = "CMO"
    COO = "COO"


class Sentiment(str, Enum):
    SUPPORT = "SUPPORT"
    NEUTRAL = "NEUTRAL"
    OPPOSE  = "OPPOSE"


class DecisionType(str, Enum):
    APPROVE              = "APPROVE"
    REJECT               = "REJECT"
    REVISE               = "REVISE"
    PRIORITIZE           = "PRIORITIZE"
    DELAY                = "DELAY"
    PIVOT                = "PIVOT"
    FORCED_COMPROMISE    = "FORCED_COMPROMISE"


class Verdict(str, Enum):
    ACCEPTED             = "ACCEPTED"
    ACCEPTED_WITH_CHANGES = "ACCEPTED_WITH_CHANGES"
    REJECTED             = "REJECTED"
    PENDING              = "PENDING"


class PressureState(str, Enum):
    CALM       = "CALM"
    URGENT     = "URGENT"
    DEFENSIVE  = "DEFENSIVE"
    AGGRESSIVE = "AGGRESSIVE"


# ----------------------------------------------------------------
# PHASE CONFIG
# Each phase has:
#   label          — human-readable name
#   priority_agent — whose vote anchors this phase
#   weight_boost   — multiplier on priority agent's vote
#   threshold      — minimum approval score to pass
#   next_phase     — which phase comes after (for handoff)
#   role_weights   — per-role vote weights
# ----------------------------------------------------------------

PHASE_CONFIG: Dict[str, Dict] = {
    "validation": {
        "label":          "Problem & Idea Validation",
        "priority_agent": Role.CEO,
        "weight_boost":   1.8,
        "threshold":      6.0,
        "next_phase":     "market",
        "role_weights":   {Role.CEO:1.8, Role.CMO:1.2, Role.CFO:1.0, Role.CTO:1.0, Role.COO:1.0},
    },
    "market": {
        "label":          "Market Research",
        "priority_agent": Role.CMO,
        "weight_boost":   1.8,
        "threshold":      6.2,
        "next_phase":     "business_model",
        "role_weights":   {Role.CMO:1.8, Role.CEO:1.2, Role.CFO:1.2, Role.CTO:1.0, Role.COO:1.0},
    },
    "business_model": {
        "label":          "Business Model Design",
        "priority_agent": Role.CFO,
        "weight_boost":   1.8,
        "threshold":      6.5,
        "next_phase":     "product",
        "role_weights":   {Role.CFO:1.8, Role.CEO:1.2, Role.CMO:1.1, Role.CTO:1.0, Role.COO:1.0},
    },
    "product": {
        "label":          "Product Strategy",
        "priority_agent": Role.CTO,
        "weight_boost":   1.8,
        "threshold":      6.5,
        "next_phase":     "gtm",
        "role_weights":   {Role.CTO:1.8, Role.COO:1.3, Role.CEO:1.1, Role.CFO:1.0, Role.CMO:1.0},
    },
    "gtm": {
        "label":          "Go-To-Market Strategy",
        "priority_agent": Role.CMO,
        "weight_boost":   1.8,
        "threshold":      6.5,
        "next_phase":     "branding",
        "role_weights":   {Role.CMO:1.8, Role.CEO:1.2, Role.COO:1.2, Role.CFO:1.0, Role.CTO:1.0},
    },
    "branding": {
        "label":          "Branding",
        "priority_agent": Role.CMO,
        "weight_boost":   1.8,
        "threshold":      6.0,
        "next_phase":     None,
        "role_weights":   {Role.CMO:1.8, Role.CEO:1.2, Role.COO:1.1, Role.CFO:1.0, Role.CTO:1.0},
    },
}


def get_phase_config(phase: str) -> Dict:
    return PHASE_CONFIG.get(phase, {
        "label":          phase.replace("_", " ").title(),
        "priority_agent": Role.CEO,
        "weight_boost":   1.5,
        "threshold":      6.0,
        "next_phase":     None,
        "role_weights":   {r: 1.0 for r in Role},
    })

def get_priority_agent(phase: str) -> Role:
    return get_phase_config(phase)["priority_agent"]

def get_threshold(phase: str) -> float:
    return get_phase_config(phase)["threshold"]

def get_next_phase(phase: str) -> Optional[str]:
    return get_phase_config(phase)["next_phase"]

def get_role_weight(phase: str, role: Role) -> float:
    return get_phase_config(phase)["role_weights"].get(role, 1.0)


# ----------------------------------------------------------------
# ROLE-FOCUSED REPORT SLICING
# Each exec sees only the fields relevant to their mandate.
# ----------------------------------------------------------------

ROLE_FOCUS: Dict[Role, List[str]] = {
    Role.CEO: ["idea", "verdict", "confidence_score", "risks", "uvp", "scores", "market_gaps", "summary", "phases"],
    Role.CTO: ["idea", "risks", "scores", "market_gaps", "pain_analysis", "product_strategy"],
    Role.CFO: ["pricing", "market_size", "financials", "scores", "risks", "unit_economics", "runway_impact"],
    Role.CMO: ["personas", "competition", "market_size", "uvp", "market_gaps", "pain_analysis", "customer_personas"],
    Role.COO: ["risks", "scores", "financials", "verdict", "personas", "runway_impact"],
}


def compress_report(reports: Dict[str, Any], role: Role) -> str:
    focus_keys = ROLE_FOCUS.get(role, list(reports.keys()))
    filtered   = {k: reports[k] for k in focus_keys if k in reports}
    if not filtered:
        filtered = dict(list(reports.items())[:5])

    lines: List[str] = []
    for k, v in filtered.items():
        if isinstance(v, dict):
            lines.append(f"[{k.upper()}]")
            for sk, sv in list(v.items())[:5]:
                lines.append(f"  {sk}: {sv}")
        elif isinstance(v, list):
            lines.append(f"[{k.upper()}]")
            for item in v[:4]:
                lines.append(f"  - {item}")
        else:
            lines.append(f"[{k.upper()}] {v}")
    return "\n".join(lines).strip()


# ----------------------------------------------------------------
# DATA MODELS
# ----------------------------------------------------------------

@dataclass
class BoardMessage:
    id:        str
    speaker:   Role
    round_no:  int
    content:   str
    sentiment: Sentiment
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Vote:
    role:       Role
    vote:       DecisionType
    confidence: int       # 0–10
    reason:     str
    weight:     float = 1.0


@dataclass
class MatrixCell:
    reviewer:  Role
    target:    Role
    agreement: str    # "AGREE" | "DISAGREE"
    reason:    str


@dataclass
class DebateExchange:
    turn:     int
    speaker:  Role
    type:     str     # CHALLENGE | DEFENSE | REBUTTAL | COUNTER | SYNTHESIS
    content:  str


@dataclass
class DebateRecord:
    id:                  int
    challenger:          Role
    defender:            Role
    disagreement_reason: str
    exchanges:           List[DebateExchange] = field(default_factory=list)


@dataclass
class ActionItem:
    owner:    str
    task:     str
    deadline: str
    priority: str = "MEDIUM"


@dataclass
class BoardState:
    startup_name:       str
    startup_stage:      str
    phase:              str
    agenda:             str
    reports:            Dict[str, Any]
    metrics:            Dict[str, Any]
    approval_threshold: float = 6.0
    settled_decisions:  str   = ""
    round_no:           int   = 0

    messages:          List[BoardMessage] = field(default_factory=list)
    votes:             List[Vote]         = field(default_factory=list)
    action_items:      List[ActionItem]   = field(default_factory=list)
    agreement_matrix:  List[MatrixCell]   = field(default_factory=list)
    debates:           List[DebateRecord] = field(default_factory=list)

    # Structured per-role Round 1 positions (parsed)
    round1_structured: Dict[str, Dict] = field(default_factory=dict)

    final_decision:  Optional[DecisionType] = None
    decision_reason: Optional[str]          = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ----------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------

def new_message(speaker, round_no, content, sentiment=None):
    return BoardMessage(
        id=str(uuid.uuid4()), speaker=speaker, round_no=round_no,
        content=content, sentiment=sentiment or Sentiment.NEUTRAL
    )

def add_message(state: BoardState, msg: BoardMessage):
    state.messages.append(msg)

def add_vote(state: BoardState, vote: Vote):
    vote.weight = get_role_weight(state.phase, vote.role)
    state.votes = [v for v in state.votes if v.role != vote.role]
    state.votes.append(vote)

def add_action(state, owner, task, deadline, priority="MEDIUM"):
    state.action_items.append(
        ActionItem(owner=owner, task=task, deadline=deadline, priority=priority)
    )

def last_message(state: BoardState, role: Role) -> str:
    for m in reversed(state.messages):
        if m.speaker == role:
            return m.content
    return ""

def messages_by_round(state: BoardState, rn: int) -> List[BoardMessage]:
    return [m for m in state.messages if m.round_no == rn]

def detect_pressure(metrics: Dict[str, Any]) -> PressureState:
    runway     = metrics.get("runway_months", 6)
    competitor = metrics.get("competitor_pressure", False)
    growth     = metrics.get("growth_rate", 0)
    if runway <= 3:  return PressureState.DEFENSIVE
    if competitor:   return PressureState.URGENT
    if growth >= 20: return PressureState.AGGRESSIVE
    return PressureState.CALM


# ----------------------------------------------------------------
# SCORING ENGINE
# ----------------------------------------------------------------

def weighted_vote_score(state: BoardState) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for v in state.votes:
        scores[v.vote.value] = scores.get(v.vote.value, 0) + (v.weight * v.confidence)
    return scores


def resolve_final_decision(state: BoardState) -> DecisionType:
    if not state.votes:
        state.final_decision = DecisionType.REVISE
        return state.final_decision
    scores    = weighted_vote_score(state)
    winner    = max(scores, key=scores.get)
    state.final_decision  = DecisionType(winner)
    state.decision_reason = f"Weighted consensus: {winner}"
    return state.final_decision


def approval_score(state: BoardState) -> float:
    if not state.votes:
        return 0.0
    total_w = sum(v.weight * v.confidence for v in state.votes)
    total   = sum(v.weight for v in state.votes)
    return round(total_w / total, 2) if total else 0.0


def derive_verdict(state: BoardState) -> Verdict:
    score    = approval_score(state)
    decision = state.final_decision
    threshold = state.approval_threshold

    if decision == DecisionType.REJECT:
        return Verdict.REJECTED

    if score >= threshold and decision in [
        DecisionType.APPROVE, DecisionType.PRIORITIZE, DecisionType.FORCED_COMPROMISE
    ]:
        return Verdict.ACCEPTED

    if score >= threshold and decision in [DecisionType.REVISE]:
        return Verdict.ACCEPTED_WITH_CHANGES

    return Verdict.REJECTED


def is_approved(state: BoardState) -> bool:
    return derive_verdict(state) in [Verdict.ACCEPTED, Verdict.ACCEPTED_WITH_CHANGES]