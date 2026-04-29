# ================================================================
# boardroom/discussion.py  |  FINAL (with board_summary)
# ================================================================

from __future__ import annotations

import time
from typing import Any, Dict, List, Tuple

from ..boardroom.core import (
    Role, BoardState, Sentiment, DecisionType,
    add_message, add_action, new_message,
    resolve_final_decision, approval_score, derive_verdict, is_approved,
    last_message, get_priority_agent, get_phase_config, get_next_phase,
    DebateExchange, DebateRecord,
)
from ..boardroom.matrix import (
    build_agreement_matrix, get_disagreements, get_priority_conflicts,
    matrix_to_dict, print_matrix,
)
from ..executive_agents.executives import build_executive_team

SPEAK_DELAY = 0.05

def _p(text: str, delay: float = SPEAK_DELAY):
    print(text, flush=True)
    if delay:
        time.sleep(delay)

def _section(title: str):
    _p(f"\n{'─'*60}\n  {title}\n{'─'*60}")

def _tag(role: Role, is_priority: bool = False) -> str:
    star = "★ " if is_priority else "  "
    return f"{star}[{role.value}]"

def print_header(state: BoardState):
    cfg      = get_phase_config(state.phase)
    priority = cfg["priority_agent"]
    _p(f"\n{'═'*60}")
    _p(f"  BOARDROOM  |  {state.startup_name} ({state.startup_stage})")
    _p(f"  Phase      : {cfg['label']}")
    _p(f"  Priority   : ★ {priority.value} (weight {cfg['weight_boost']}x)")
    _p(f"  Threshold  : {state.approval_threshold}/10")
    _p(f"  Runway     : {state.metrics.get('runway_months','?')} months  "
       f"| Competitor pressure: {state.metrics.get('competitor_pressure', False)}")
    _p(f"{'═'*60}")

def round_diagnosis(state: BoardState, team: Dict, prior_decisions: str = "") -> None:
    state.round_no = 1
    _section("ROUND 1  |  INDEPENDENT DIAGNOSIS")
    priority = get_priority_agent(state.phase)
    order    = [r for r in Role if r != priority] + [priority]
    for role in order:
        is_p  = (role == priority)
        label = _tag(role, is_p)
        _p(f"\n{label}", 0.3)
        team[role].think(state=state, prior_decisions=prior_decisions)
        msg = last_message(state, role)
        for line in msg.split("\n")[:10]:
            if line.strip():
                _p(f"    {line.strip()}")

def run_matrix(state: BoardState) -> List:
    _section("AGREEMENT MATRIX  |  Each exec reviews every other's position")
    cells = build_agreement_matrix(state)
    print_matrix(cells, state.phase)
    return cells

EXCHANGE_TYPES = ["CHALLENGE", "DEFENSE", "REBUTTAL", "COUNTER", "SYNTHESIS"]

EXCHANGE_PROMPTS = [
    lambda reviewer, target, reason, tar_msg: (
        f"You DISAGREED with {target.value}: {reason}\n"
        f"{target.value} said: {tar_msg[:250]}\n"
        f"Launch a specific, evidence-based challenge. Use numbers from the report. 2-3 sentences max."
    ),
    lambda reviewer, target, reason, rev_msg: (
        f"{reviewer.value} challenged you: {rev_msg[:250]}\n"
        f"Defend your position with specific data. 2-3 sentences."
    ),
    lambda reviewer, target, reason, tar_msg: (
        f"{target.value} defended: {tar_msg[:250]}\n"
        f"Attack the weakest part of their defense. Propose a concrete change. 2 sentences."
    ),
    lambda reviewer, target, reason, rev_msg: (
        f"{reviewer.value} rebutted: {rev_msg[:250]}\n"
        f"Final counter or accept a middle ground. 2 sentences."
    ),
    lambda reviewer, target, reason, _: (
        f"Based on this exchange, propose ONE specific actionable decision "
        f"that resolves the disagreement. 1-2 sentences."
    ),
]

SPEAKER_SEQUENCE = [
    lambda reviewer, target: reviewer,
    lambda reviewer, target: target,
    lambda reviewer, target: reviewer,
    lambda reviewer, target: target,
    lambda reviewer, target: reviewer,
]

def _run_single_debate(
    state: BoardState,
    team: Dict,
    debate_id: int,
    reviewer: Role,
    target: Role,
    reason: str,
    prior_decisions: str,
    max_exchanges: int = 5,
) -> DebateRecord:
    record = DebateRecord(
        id=debate_id,
        challenger=reviewer,
        defender=target,
        disagreement_reason=reason,
    )
    last_rev_msg = last_message(state, reviewer)
    last_tar_msg = last_message(state, target)
    for turn_idx in range(min(max_exchanges, 5)):
        turn_no      = turn_idx + 1
        exchange_type = EXCHANGE_TYPES[turn_idx]
        speaker       = SPEAKER_SEQUENCE[turn_idx](reviewer, target)
        prompt_fn     = EXCHANGE_PROMPTS[turn_idx]
        if turn_idx == 0:
            context_msg = last_tar_msg
        elif turn_idx % 2 == 1:
            context_msg = last_rev_msg
        else:
            context_msg = last_tar_msg
        task = prompt_fn(reviewer, target, reason, context_msg)
        _p(f"\n    Turn {turn_no} — {exchange_type} by {speaker.value}:", 0.2)
        team[speaker].debate_turn(state=state, task=task, prior_decisions=prior_decisions)
        content = last_message(state, speaker)
        if speaker == reviewer:
            last_rev_msg = content
        else:
            last_tar_msg = content
        exchange = DebateExchange(turn=turn_no, speaker=speaker, type=exchange_type, content=content)
        record.exchanges.append(exchange)
        _p(f"      {content[:350]}")
    return record

def round_debates(
    state: BoardState,
    team: Dict,
    cells: List,
    prior_decisions: str,
    max_exchanges: int = 5,
) -> None:
    state.round_no = 2
    _section(f"ROUND 2  |  TARGETED DEBATES  ({max_exchanges} exchanges each)")
    priority   = get_priority_agent(state.phase)
    conflicts  = get_priority_conflicts(cells, state.phase)
    all_disagree = get_disagreements(cells)
    queue: List[Tuple[Role, Role, str]] = []
    seen = set()
    for target, reason in conflicts:
        queue.append((priority, target, reason))
        seen.add((priority, target))
    for reviewer, target, reason in all_disagree:
        if (reviewer, target) not in seen:
            queue.append((reviewer, target, reason))
            seen.add((reviewer, target))
    if not queue:
        _p("  No disagreements found. Board is aligned.")
        return
    for idx, (reviewer, target, reason) in enumerate(queue):
        is_p = (reviewer == priority)
        star = "★ " if is_p else ""
        _p(f"\n  {star}Debate {idx+1}: [{reviewer.value}] vs [{target.value}]")
        _p(f"  Disagreement: {reason[:120]}")
        record = _run_single_debate(state, team, idx+1, reviewer, target, reason, prior_decisions, max_exchanges)
        state.debates.append(record)

def final_resolution(state: BoardState) -> None:
    _section("BOARD RESOLUTION")
    cfg      = get_phase_config(state.phase)
    priority = cfg["priority_agent"]
    decision = resolve_final_decision(state)
    score    = approval_score(state)
    verdict  = derive_verdict(state)
    verdict_labels = {
        "ACCEPTED":              "✓  ACCEPTED — Proceed to next phase",
        "ACCEPTED_WITH_CHANGES": "↺  ACCEPTED WITH CHANGES — Rework then proceed",
        "REJECTED":              "✗  REJECTED — Restart this phase",
        "PENDING":               "⏸  PENDING",
    }
    _p(f"\n  VERDICT   : {verdict_labels.get(verdict.value, verdict.value)}")
    _p(f"  DECISION  : {decision.value}")
    _p(f"  SCORE     : {score:.2f} / {state.approval_threshold}")
    _p("\n  VOTE BREAKDOWN:")
    for v in state.votes:
        star = "★" if v.role == priority else " "
        bar  = "█" * v.confidence + "░" * (10 - v.confidence)
        _p(f"    {star} {v.role.value:<5}  {v.vote.value:<12}  [{bar}]  {v.confidence}/10  w={v.weight}")
    add_action(state, "CEO Office", "Assign owners to board decisions", "48h", "HIGH")
    add_action(state, "Operational Layer", "Apply board feedback to phase deliverables", "Immediate", "HIGH")

def build_phase_handoff(state: BoardState) -> Dict[str, Any]:
    cfg        = get_phase_config(state.phase)
    next_phase = get_next_phase(state.phase)
    priority   = cfg["priority_agent"]
    verdict    = derive_verdict(state)
    settled_facts = []
    for role_val, structured in state.round1_structured.items():
        role = Role(role_val)
        if role == Role.CEO and structured.get("direction"):
            settled_facts.append(f"CEO direction: {structured['direction'][:150]}")
        elif role == Role.CTO and structured.get("cut"):
            settled_facts.append(f"CTO cut: {structured['cut'][:150]}")
        elif role == Role.CFO and structured.get("revenue_target"):
            settled_facts.append(f"CFO revenue target: {structured['revenue_target'][:150]}")
        elif role == Role.CMO and structured.get("first_customer"):
            settled_facts.append(f"CMO first customer: {structured['first_customer'][:150]}")
        elif role == Role.COO and structured.get("blocker_1"):
            settled_facts.append(f"COO blocker 1: {structured['blocker_1'][:150]}")
    open_issues = []
    for debate in state.debates:
        synth = next((e for e in debate.exchanges if e.type == "SYNTHESIS"), None)
        if synth:
            settled_facts.append(
                f"Resolved ({debate.challenger.value} vs {debate.defender.value}): {synth.content[:120]}"
            )
        else:
            open_issues.append(
                f"Unresolved: {debate.challenger.value} vs {debate.defender.value} — {debate.disagreement_reason[:100]}"
            )
    priority_structured = state.round1_structured.get(priority.value, {})
    directive = (
        priority_structured.get("direction", "")
        or priority_structured.get("first_customer", "")
        or priority_structured.get("strategic_risk", "")
        or "Proceed with board decisions."
    )
    return {
        "from_phase":       state.phase,
        "from_phase_label": cfg["label"],
        "to_phase":         next_phase,
        "verdict":          verdict.value,
        "score":            approval_score(state),
        "priority_agent":   priority.value,
        "settled_facts":    settled_facts[:6],
        "open_issues":      open_issues[:3],
        "board_directive":  directive[:300],
        "action_items": [
            {"owner": a.owner, "task": a.task, "deadline": a.deadline}
            for a in state.action_items
        ],
    }

def build_board_resolution(state: BoardState) -> Dict[str, Any]:
    cfg      = get_phase_config(state.phase)
    priority = cfg["priority_agent"]
    verdict  = derive_verdict(state)
    score    = approval_score(state)
    conditions = []
    for v in state.votes:
        if v.vote in [DecisionType.REVISE, DecisionType.REJECT]:
            if v.reason and len(v.reason) > 20:
                conditions.append(f"{v.role.value}: {v.reason[:150]}")
    key_decisions = []
    for debate in state.debates:
        synth = next((e for e in debate.exchanges if e.type == "SYNTHESIS"), None)
        if synth and synth.content:
            key_decisions.append(synth.content[:200])
    unresolved = []
    for debate in state.debates:
        synth = next((e for e in debate.exchanges if e.type == "SYNTHESIS"), None)
        if not synth:
            unresolved.append(f"{debate.challenger.value} vs {debate.defender.value}: {debate.disagreement_reason[:100]}")
    next_steps = [f"{a.owner}: {a.task} by {a.deadline}" for a in state.action_items]
    return {
        "verdict":         verdict.value,
        "decision_type":   state.final_decision.value if state.final_decision else "UNKNOWN",
        "score":           score,
        "threshold":       state.approval_threshold,
        "priority_agent":  priority.value,
        "approved":        is_approved(state),
        "conditions":      conditions[:4],
        "key_decisions":   key_decisions[:4],
        "unresolved":      unresolved[:3],
        "next_steps":      next_steps[:4],
        "action_items": [
            {"owner": a.owner, "task": a.task, "deadline": a.deadline, "priority": a.priority}
            for a in state.action_items
        ],
    }

def build_output(state: BoardState) -> Dict[str, Any]:
    cfg      = get_phase_config(state.phase)
    priority = cfg["priority_agent"]
    score    = approval_score(state)
    verdict  = derive_verdict(state)
    decision_type = state.final_decision.value if state.final_decision else "UNKNOWN"

    # Quick readable summary
    board_summary_lines = [
        f"Verdict: {verdict.value}",
        f"Score: {score:.2f} / {state.approval_threshold}",
        f"Decision: {decision_type}",
    ]
    board_summary = "\n".join(board_summary_lines)

    return {
        "session": {
            "startup_name":    state.startup_name,
            "startup_stage":   state.startup_stage,
            "phase":           state.phase,
            "phase_label":     cfg["label"],
            "priority_agent":  priority.value,
            "score":           score,
            "threshold":       state.approval_threshold,
            "verdict":         verdict.value,
            "decision_type":   decision_type,
            "timestamp":       state.created_at,
        },
        "round1": state.round1_structured,
        "agreement_matrix": matrix_to_dict(state.agreement_matrix),
        "debates": [
            {
                "id":                  d.id,
                "challenger":          d.challenger.value,
                "defender":            d.defender.value,
                "is_priority_debate":  d.challenger == priority,
                "disagreement_reason": d.disagreement_reason,
                "exchanges": [
                    {"turn": e.turn, "speaker": e.speaker.value, "type": e.type, "content": e.content}
                    for e in d.exchanges
                ],
            }
            for d in state.debates
        ],
        "votes": {
            v.role.value: {
                "vote":        v.vote.value,
                "confidence":  v.confidence,
                "weight":      v.weight,
                "is_priority": v.role == priority,
            }
            for v in state.votes
        },
        "board_resolution": build_board_resolution(state),
        "phase_handoff": build_phase_handoff(state),
        "board_summary": board_summary,   # <-- ADDED for easy frontend display
    }

def run_full_board_meeting(
    state: BoardState,
    prior_decisions: str = "",
    max_exchanges: int = 5,
) -> BoardState:
    team = build_executive_team()
    print_header(state)
    round_diagnosis(state, team, prior_decisions)
    cells = run_matrix(state)
    round_debates(state, team, cells, prior_decisions, max_exchanges)
    final_resolution(state)
    return state

def boardroom_node(payload: Dict[str, Any]) -> Dict[str, Any]:
    phase     = payload["phase"]
    cfg       = get_phase_config(phase)
    threshold = payload.get("approval_threshold", cfg["threshold"])
    state = BoardState(
        startup_name=payload["startup_name"],
        startup_stage=payload["startup_stage"],
        phase=phase,
        agenda=payload.get("agenda", f"Review {cfg['label']} submission"),
        reports=payload["reports"],
        metrics=payload.get("metrics", {}),
        approval_threshold=threshold,
        settled_decisions=payload.get("settled_decisions", ""),
    )
    run_full_board_meeting(
        state,
        prior_decisions=payload.get("settled_decisions", ""),
        max_exchanges=payload.get("max_exchanges", 5),
    )
    return build_output(state)