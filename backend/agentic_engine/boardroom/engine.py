# ===============================================================
# FILE: boardroom/engine.py
# LIVE BOARDROOM ENGINE (FINAL)
#
# Features:
# - accepts messy phase outputs
# - launches real-time executive room
# - redo loop with live meetings
# - board secretary compromise
# - terminal friendly output
#
# Depends:
#   boardroom/core.py
#   boardroom/discussion.py
# ===============================================================

from __future__ import annotations

from typing import Dict, Any, List, Callable
from dataclasses import dataclass

from ..boardroom.discussion import boardroom_node


# ===============================================================
# PHASE CONFIG
# ===============================================================

PHASE_LABELS = {
    "validation": "Problem & Idea Validation",
    "market": "Market Research",
    "business_model": "Business Model Design",
    "product": "Product Strategy",
    "gtm": "Go-To-Market Strategy"
}


# ===============================================================
# RESULT MODEL
# ===============================================================

@dataclass
class LoopResult:
    approved: bool
    iterations: int
    decision: str
    refinement_orders: List[str]
    actionables: List[Dict[str, Any]]
    transcript: List[str]
    final_payload: Dict[str, Any]


# ===============================================================
# BOARD SECRETARY
# ===============================================================

class BoardSecretary:

    def force_resolution(self):

        print("\n[BOARD SECRETARY] "
              "Three review cycles reached.")
        print("[BOARD SECRETARY] "
              "Forcing pragmatic compromise.\n")

        return {
            "decision": "FORCED_COMPROMISE",
            "orders": [
                "Ship reduced-scope version now",
                "Track real user metrics",
                "Re-open board review next week"
            ]
        }


# ===============================================================
# BACKLOG MANAGER
# ===============================================================

class BacklogManager:

    @staticmethod
    def extract(payload: Dict[str, Any]):

        redo = payload.get("redo_brief", [])

        if redo:
            return redo

        return [
            "Improve strategic clarity",
            "Fix weak assumptions",
            "Return stronger version"
        ]


# ===============================================================
# ENGINE
# ===============================================================

class BoardroomEngine:

    def __init__(self):
        self.secretary = BoardSecretary()
        self.backlog = BacklogManager()

    # -----------------------------------------------------------

    def run_once(
        self,
        startup_name: str,
        startup_stage: str,
        phase: str,
        report: Dict[str, Any],
        metrics: Dict[str, Any]
    ):

        payload = {
            "startup_name": startup_name,
            "startup_stage": startup_stage,
            "phase": phase,
            "agenda": (
                f"Review "
                f"{PHASE_LABELS.get(phase, phase)} "
                f"submission"
            ),
            "reports": report,
            "metrics": metrics
        }

        return boardroom_node(payload)

    # -----------------------------------------------------------

    def should_approve(
        self,
        output: Dict[str, Any]
    ) -> bool:
        """
        Realistic temporary logic:
        If transcript contains strong resolution.
        """

        text = " ".join(
            output.get("transcript", [])
        ).lower()

        signals = [
            "move forward",
            "proceed",
            "launch",
            "approved",
            "we move"
        ]

        return any(s in text for s in signals)

    # -----------------------------------------------------------

    def run_loop(
        self,
        startup_name: str,
        startup_stage: str,
        phase: str,
        initial_report: Dict[str, Any],
        metrics: Dict[str, Any],
        operational_callback: Callable[
            [Dict[str, Any], List[str]],
            Dict[str, Any]
        ],
        max_iterations: int = 3
    ):

        current = initial_report

        for i in range(1, max_iterations + 1):

            print("\n" + "=" * 70)
            print(f"BOARD REVIEW CYCLE {i}")
            print("=" * 70)

            result = self.run_once(
                startup_name=startup_name,
                startup_stage=startup_stage,
                phase=phase,
                report=current,
                metrics=metrics
            )

            approved = self.should_approve(result)

            if approved:

                print("\n[BOARD] Consensus reached.")
                print("[BOARD] Proceeding.\n")

                return LoopResult(
                    approved=True,
                    iterations=i,
                    decision="PROCEED",
                    refinement_orders=[],
                    actionables=result["actionables"],
                    transcript=result["transcript"],
                    final_payload=result
                )

            # redo route
            redo_orders = self.backlog.extract(
                result
            )

            print("\n[BOARD] Revision required.")
            print("[BOARD] Sending notes "
                  "to operational layer.\n")

            current = operational_callback(
                current,
                redo_orders
            )

        # =======================================================
        # CIRCUIT BREAKER
        # =======================================================

        forced = self.secretary.force_resolution()

        return LoopResult(
            approved=True,
            iterations=max_iterations,
            decision=forced["decision"],
            refinement_orders=forced["orders"],
            actionables=[
                {
                    "owner": "Board Secretary",
                    "task": x,
                    "deadline": "Immediate"
                }
                for x in forced["orders"]
            ],
            transcript=[],
            final_payload=forced
        )


# ===============================================================
# DEFAULT CALLBACK
# ===============================================================

def dummy_operational_callback(
    report: Dict[str, Any],
    orders: List[str]
):

    print("[OPERATIONAL LAYER] "
          "Applying board feedback...")

    improved = dict(report)
    improved["board_feedback"] = orders

    return improved


# ===============================================================
# PUBLIC ENTRY
# ===============================================================

def run_phase_gate(
    startup_name: str,
    startup_stage: str,
    phase: str,
    report: Dict[str, Any],
    metrics: Dict[str, Any],
    operational_callback=None
):

    engine = BoardroomEngine()

    return engine.run_loop(
        startup_name=startup_name,
        startup_stage=startup_stage,
        phase=phase,
        initial_report=report,
        metrics=metrics,
        operational_callback=(
            operational_callback
            or dummy_operational_callback
        )
    )