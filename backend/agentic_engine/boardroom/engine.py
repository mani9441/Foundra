from __future__ import annotations
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ..boardroom.discussion import boardroom_node
from ..boardroom.core import get_phase_config
from ..boardroom.report_mutator import mutate_report

@dataclass
class LoopResult:
    approved: bool
    iterations: int
    decision: str
    priority_agent: str
    refinement_orders: List[str]
    actionables: List[Dict[str, Any]]
    transcript: List[Dict[str, Any]]
    vote_summary: Dict[str, Any]
    agreement_matrix: Dict[str, Any]
    approval_score: float
    final_payload: Dict[str, Any]
    revised_report: Dict[str, Any]
    output_file: Optional[str] = None   # <-- added

def save_boardroom_output(output: Dict[str, Any], startup_name: str, phase: str) -> str:
    """Save boardroom output JSON to outputs/ folder."""
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{startup_name}_{phase}_{timestamp}.json"
    filepath = os.path.join("outputs", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return filepath

class BacklogManager:
    @staticmethod
    def extract(result: Dict[str, Any]) -> List[str]:
        orders = []
        # In new output, round2_challenges might not exist; fallback to votes
        challenges = result.get("round2_challenges", {})
        for key, val in challenges.items():
            if val and len(val) > 15:
                orders.append(val[:120])
                if len(orders) >= 2:
                    break
        if not orders:
            for v in result.get("votes", {}).values():
                if v.get("reason") and len(v["reason"]) > 10:
                    orders.append(v["reason"][:120])
                    if len(orders) >= 2:
                        break
        return orders[:3] or ["Refine based on board feedback", "Incorporate priority agent's concerns"]

def smart_operational_callback(report: Dict[str, Any], orders: List[str]) -> Dict[str, Any]:
    return mutate_report(report, orders)

def run_phase_gate(
    startup_name: str,
    startup_stage: str,
    phase: str,
    report: Dict[str, Any],
    metrics: Dict[str, Any],
    operational_callback: Optional[Callable] = None,
    max_iterations: int = 1,        # default to 1 cycle for speed
    debate_exchanges: int = 5,
) -> LoopResult:

    cfg = get_phase_config(phase)
    threshold = cfg["threshold"]
    priority = cfg["priority_agent"].value

    current_report = report
    settled_decisions = ""
    all_transcripts = []
    result = None
    output_file = None

    for i in range(1, max_iterations + 1):
        print(f"\n{'═'*55}")
        print(f"  CYCLE {i} of {max_iterations}  |  {cfg['label']}  |  Threshold: {threshold}")
        print(f"{'═'*55}")

        result = boardroom_node({
            "startup_name": startup_name,
            "startup_stage": startup_stage,
            "phase": phase,
            "reports": current_report,
            "metrics": metrics,
            "approval_threshold": threshold,
            "settled_decisions": settled_decisions,
            "max_exchanges": debate_exchanges,
        })

        # Save output after first call (for single cycle)
        if output_file is None:
            output_file = save_boardroom_output(result, startup_name, phase)
            print(f"\n  [SAVED] Boardroom JSON → {output_file}")

        # Extract info for loop decision
        session = result.get("session", {})
        score = session.get("score", 0.0)
        verdict = session.get("verdict", "")
        decision_type = session.get("decision_type", "?")
        approved = verdict in ["ACCEPTED", "ACCEPTED_WITH_CHANGES"]

        print(f"\n  Board verdict: {decision_type}  |  Score: {score:.2f} / {threshold}  |  {'✓ PASSED' if approved else '✗ NOT PASSED'}")

        if approved:
            return LoopResult(
                approved=True,
                iterations=i,
                decision=decision_type,
                priority_agent=priority,
                refinement_orders=[],
                actionables=result.get("board_resolution", {}).get("action_items", []),
                transcript=all_transcripts,
                vote_summary=result.get("votes", {}),
                agreement_matrix=result.get("agreement_matrix", {}),
                approval_score=score,
                final_payload=result,
                revised_report=current_report,
                output_file=output_file,
            )

        # Not approved: prepare for next cycle (if any)
        orders = BacklogManager.extract(result)
        print(f"\n  Critique for operational layer:")
        for o in orders:
            print(f"    → {o}")

        r1 = result.get("round1", {})
        # Build new settled facts from structured round1
        for role_val, structured in r1.items():
            if structured.get("direction"):
                settled_decisions += f"\nCEO: {structured['direction'][:150]}"
            elif structured.get("cut"):
                settled_decisions += f"\nCTO cut: {structured['cut'][:150]}"
            elif structured.get("revenue_target"):
                settled_decisions += f"\nCFO target: {structured['revenue_target'][:150]}"
            elif structured.get("first_customer"):
                settled_decisions += f"\nCMO: {structured['first_customer'][:150]}"
            elif structured.get("blocker_1"):
                settled_decisions += f"\nCOO blocker: {structured['blocker_1'][:150]}"

        callback = operational_callback or smart_operational_callback
        current_report = callback(current_report, orders)
        if "burn rate" in " ".join(orders).lower():
            metrics["runway_months"] = max(metrics.get("runway_months", 5) - 1, 2)

    # After max cycles, if not approved but score OK – force approve with conditions
    if result and (score >= threshold or approved):
        print(f"\n[SECRETARY] Max cycles reached, but acceptable score. Approving with conditions.")
        return LoopResult(
            approved=True,
            iterations=max_iterations,
            decision=decision_type,
            priority_agent=priority,
            refinement_orders=["Implement board feedback from the cycles"],
            actionables=result.get("board_resolution", {}).get("action_items", []),
            transcript=all_transcripts,
            vote_summary=result.get("votes", {}),
            agreement_matrix=result.get("agreement_matrix", {}),
            approval_score=score,
            final_payload=result,
            revised_report=current_report,
            output_file=output_file,
        )
    else:
        print(f"\n[SECRETARY] Max cycles reached and score insufficient. Board rejects.")
        return LoopResult(
            approved=False,
            iterations=max_iterations,
            decision="REJECT",
            priority_agent=priority,
            refinement_orders=["Restart phase with major changes"],
            actionables=[],
            transcript=all_transcripts,
            vote_summary=result.get("votes", {}) if result else {},
            agreement_matrix=result.get("agreement_matrix", {}) if result else {},
            approval_score=score,
            final_payload=result or {},
            revised_report=current_report,
            output_file=output_file,
        )