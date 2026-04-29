# ================================================================
# executive_agents/executives.py  |  FINAL
#
# Universal board member agents.
# No LangChain memory — state is managed in BoardState.messages.
# Each role has:
#   - A fixed output schema for Round 1 (parsed into structured JSON)
#   - A debate_turn method (capped at 3 lines for speed)
#   - A parser that extracts structured fields from free text
# ================================================================

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate

from ..boardroom.core import (
    Role, Sentiment, DecisionType, Vote, BoardState,
    add_vote, add_message, new_message,
    detect_pressure, compress_report, last_message,
    get_priority_agent,
)
from ..LLMs.llm import get_llm


# ----------------------------------------------------------------
# ROLE PERSONALITIES — universal, no domain assumptions
# ----------------------------------------------------------------

PERSONALITIES: Dict[Role, Dict[str, str]] = {
    Role.CEO: {
        "title": "Chief Executive Officer",
        "voice": "Decisive, big-picture, mission-driven. You make the hard call.",
        "goal":  "Win the market. Set the right strategy.",
    },
    Role.CTO: {
        "title": "Chief Technology Officer",
        "voice": "Engineering realist. Blunt. You hate fantasy scope.",
        "goal":  "Ship a feasible, maintainable product on time.",
    },
    Role.CFO: {
        "title": "Chief Financial Officer",
        "voice": "Numbers-first. Skeptical. You ask for proof before committing.",
        "goal":  "Protect runway. Ensure positive unit economics.",
    },
    Role.CMO: {
        "title": "Chief Marketing Officer",
        "voice": "Growth-obsessed, customer-centric. You see market gaps first.",
        "goal":  "Acquire first paying customers. Build momentum fast.",
    },
    Role.COO: {
        "title": "Chief Operating Officer",
        "voice": "Execution disciplinarian. You turn strategy into owned tasks.",
        "goal":  "Make sure decisions become real actions with owners and timelines.",
    },
}


# ----------------------------------------------------------------
# ROUND 1 QUESTIONS — per role, universal
# ----------------------------------------------------------------

R1_QUESTIONS: Dict[Role, str] = {
    Role.CEO: (
        "What is the single biggest strategic risk in this report? "
        "State your recommended direction in 2 sentences. "
        "End with VOTE and CONFIDENCE."
    ),
    Role.CTO: (
        "Is the technical scope realistic for our stage? "
        "Name exactly what must be CUT and what must be KEPT. "
        "End with VOTE and CONFIDENCE."
    ),
    Role.CFO: (
        "State the BURN RISK (runway + burn rate + risk level), "
        "UNIT ECONOMICS (LTV, CAC estimate, YES or NO it works), "
        "and REVENUE TARGET (exact number and deadline). "
        "End with VOTE and CONFIDENCE."
    ),
    Role.CMO: (
        "Name the FIRST CUSTOMER (exact segment), "
        "CHANNEL (exact platform), "
        "and MESSAGE (one sentence). "
        "End with VOTE and CONFIDENCE."
    ),
    Role.COO: (
        "Name the top 2 execution risks. "
        "For each: BLOCKER, OWNER (specific role), DEADLINE. "
        "End with VOTE and CONFIDENCE."
    ),
}


# ----------------------------------------------------------------
# STRUCTURED OUTPUT PARSERS
# Extract structured fields from free-text Round 1 responses.
# This replaces asking the LLM for JSON (which small models fail).
# ----------------------------------------------------------------

def _extract_vote(text: str) -> DecisionType:
    upper = text.upper()
    for v in ["APPROVE", "REJECT", "REVISE", "PRIORITIZE", "DELAY", "PIVOT"]:
        if f"VOTE: {v}" in upper or f"VOTE:{v}" in upper:
            return DecisionType(v)
    if "APPROVE" in upper and "REJECT" not in upper:
        return DecisionType.APPROVE
    if "REJECT" in upper:
        return DecisionType.REJECT
    return DecisionType.REVISE


def _extract_confidence(text: str) -> int:
    m = re.search(r"CONFIDENCE\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)
    if m:
        return max(1, min(10, int(m.group(1))))
    if any(w in text.lower() for w in ["strongly", "critical", "definitely"]):
        return 9
    return 7


def _first_sentence(text: str, max_chars: int = 250) -> str:
    for sep in [".", "!", "?"]:
        idx = text.find(sep)
        if 20 < idx < max_chars:
            return text[:idx + 1].strip()
    return text[:max_chars].strip()


def parse_round1(role: Role, text: str) -> Dict[str, Any]:
    """
    Extract structured fields from a Round 1 free-text response.
    Returns a clean dict for JSON output.
    Does NOT ask the LLM for JSON — extracts from what the model said.
    """
    result: Dict[str, Any] = {}
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    if role == Role.CEO:
        result["strategic_risk"] = lines[0][:300] if lines else ""
        result["direction"]      = lines[1][:300] if len(lines) > 1 else ""

    elif role == Role.CTO:
        cut_m  = re.search(r"CUT[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        keep_m = re.search(r"KEEP[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        result["verdict"] = _first_sentence(lines[0]) if lines else ""
        result["cut"]     = cut_m.group(1).strip()[:250]  if cut_m  else ""
        result["keep"]    = keep_m.group(1).strip()[:250] if keep_m else ""

    elif role == Role.CFO:
        burn_m = re.search(r"BURN\s*RISK[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        unit_m = re.search(r"UNIT\s*ECONOMICS[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        rev_m  = re.search(r"REVENUE\s*TARGET[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        result["burn_risk"]       = burn_m.group(1).strip()[:200] if burn_m else _first_sentence(lines[0]) if lines else ""
        result["unit_economics"]  = unit_m.group(1).strip()[:200] if unit_m else ""
        result["revenue_target"]  = rev_m.group(1).strip()[:200]  if rev_m  else ""

    elif role == Role.CMO:
        cust_m = re.search(r"FIRST\s*CUSTOMER[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        chan_m = re.search(r"CHANNEL[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        msg_m  = re.search(r"MESSAGE[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        result["first_customer"] = cust_m.group(1).strip()[:250] if cust_m else _first_sentence(lines[0]) if lines else ""
        result["channel"]        = chan_m.group(1).strip()[:200]  if chan_m else ""
        result["message"]        = msg_m.group(1).strip()[:200]   if msg_m  else ""

    elif role == Role.COO:
        b1_m = re.search(r"BLOCKER\s*1[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        b2_m = re.search(r"BLOCKER\s*2[:\-]?\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
        result["blocker_1"] = b1_m.group(1).strip()[:250] if b1_m else _first_sentence(lines[0]) if lines else ""
        result["blocker_2"] = b2_m.group(1).strip()[:250] if b2_m else (lines[1][:250] if len(lines) > 1 else "")

    result["vote"]       = _extract_vote(text).value
    result["confidence"] = _extract_confidence(text)
    return result


# ----------------------------------------------------------------
# BASE AGENT
# ----------------------------------------------------------------

BASE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are {role} — {title}.\n"
     "Personality: {voice}\n"
     "Goal: {goal}\n"
     "{priority_note}\n\n"
     "RULES:\n"
     "1. Be direct. Use natural human language.\n"
     "2. Use actual numbers from the data — no vague statements.\n"
     "3. Always end with exactly: VOTE: <decision>  and  CONFIDENCE: <1-10>\n"
     "4. Do NOT repeat prior settled decisions."
    ),
    ("human",
     "STARTUP: {startup_name} | STAGE: {startup_stage} | PHASE: {phase} | PRESSURE: {pressure}\n\n"
     "YOUR DATA:\n{report_slice}\n\n"
     "YOUR TASK:\n{task}\n\n"
     "PRIOR SETTLED DECISIONS (do not re-debate these):\n{prior_decisions}\n\n"
     "LAST 4 ROOM MESSAGES:\n{transcript}\n\n"
     "Respond now."
    )
])


class ExecutiveAgent:

    def __init__(self, role: Role):
        self.role        = role
        self.personality = PERSONALITIES[role]
        self.r1_question = R1_QUESTIONS[role]
        self.llm         = get_llm()
        self.chain       = BASE_PROMPT | self.llm

    def _build_inputs(
        self,
        state: BoardState,
        task: str,
        prior_decisions: str,
    ) -> Dict[str, str]:
        is_priority   = get_priority_agent(state.phase) == self.role
        priority_note = "★ YOU ARE THE PRIORITY AGENT for this phase. Be decisive and anchor the board." if is_priority else ""

        transcript = "\n".join([
            f"  {m.speaker.value}: {m.content[:120]}"
            for m in state.messages[-4:]
        ]) or "  (none yet)"

        return {
            "role":           self.role.value,
            "title":          self.personality["title"],
            "voice":          self.personality["voice"],
            "goal":           self.personality["goal"],
            "priority_note":  priority_note,
            "startup_name":   state.startup_name,
            "startup_stage":  state.startup_stage,
            "phase":          state.phase,
            "pressure":       detect_pressure(state.metrics).value,
            "report_slice":   compress_report(state.reports, self.role),
            "task":           task,
            "prior_decisions": prior_decisions or "None — first round.",
            "transcript":     transcript,
        }

    def think(
        self,
        state: BoardState,
        prior_decisions: str = "",
    ) -> str:
        """Round 1 diagnosis. Full response, parsed into structured JSON."""
        raw  = self.chain.invoke(self._build_inputs(state, self.r1_question, prior_decisions))
        text = str(getattr(raw, "content", raw)).strip()
        text = "\n".join(text.split("\n")[:15])  # max 15 lines for R1

        vote      = _extract_vote(text)
        conf      = _extract_confidence(text)
        sentiment = Sentiment.SUPPORT if vote in [DecisionType.APPROVE, DecisionType.PRIORITIZE] else Sentiment.OPPOSE

        add_message(state, new_message(self.role, state.round_no, text, sentiment))
        add_vote(state, Vote(self.role, vote, conf, text[:150]))

        # Parse and store structured output
        structured = parse_round1(self.role, text)
        state.round1_structured[self.role.value] = structured

        return text

    def debate_turn(
        self,
        state: BoardState,
        task: str,
        prior_decisions: str = "",
    ) -> str:
        """
        Debate exchange. Capped at 3 lines / 300 chars for speed.
        Does NOT add a vote — only Round 1 votes count.
        """
        raw  = self.chain.invoke(self._build_inputs(state, task, prior_decisions))
        text = str(getattr(raw, "content", raw)).strip()

        # Hard cap for speed
        lines = [l for l in text.split("\n") if l.strip()]
        text  = "\n".join(lines[:3])
        if len(text) > 300:
            text = text[:300] + "..."

        add_message(state, new_message(self.role, state.round_no, text, Sentiment.NEUTRAL))
        return text


# ----------------------------------------------------------------
# SPECIALIST SUBCLASSES
# ----------------------------------------------------------------

class CEOAgent(ExecutiveAgent):
    def __init__(self): super().__init__(Role.CEO)

class CTOAgent(ExecutiveAgent):
    def __init__(self): super().__init__(Role.CTO)

class CFOAgent(ExecutiveAgent):
    def __init__(self): super().__init__(Role.CFO)

class CMOAgent(ExecutiveAgent):
    def __init__(self): super().__init__(Role.CMO)

class COOAgent(ExecutiveAgent):
    def __init__(self): super().__init__(Role.COO)


def build_executive_team() -> Dict[Role, ExecutiveAgent]:
    return {
        Role.CEO: CEOAgent(),
        Role.CTO: CTOAgent(),
        Role.CFO: CFOAgent(),
        Role.CMO: CMOAgent(),
        Role.COO: COOAgent(),
    }