# ==========================================================
# FILE: backend/routes/boardroom.py
# FINAL BOARDROOM ROUTER
# Uses DB for ownership/storage
# Uses engine only for execution
# ==========================================================

import json
import traceback
from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from ..db.auth import get_current_user
from ..db.supabase import supabase

from backend.agentic_engine.boardroom.engine import run_phase_gate

router = APIRouter()


# ==========================================================
# HELPERS
# ==========================================================

def debug(msg):
    print(f"[BOARDROOM DEBUG] {msg}")


def get_project_or_404(project_id: str, user_id: str):
    result = (
        supabase.table("projects")
        .select("*")
        .eq("id", project_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")

    return result.data[0]


def get_latest_phase(project_id: str, phase: int):
    result = (
        supabase.table("phase_runs")
        .select("*")
        .eq("project_id", project_id)
        .eq("phase_number", phase)
        .eq("status", "completed")
        .order("retry_number", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def get_latest_boardroom(project_id: str, phase: int):
    result = (
        supabase.table("boardroom_runs")
        .select("*")
        .eq("project_id", project_id)
        .eq("phase_number", phase)
        .order("retry_number", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def get_next_retry(project_id: str, phase: int):
    latest = get_latest_boardroom(project_id, phase)

    if latest:
        return latest["retry_number"] + 1

    return 1


def create_processing_row(project_id, user_id, phase, retry_number, input_data):
    created = (
        supabase.table("boardroom_runs")
        .insert({
            "project_id": project_id,
            "user_id": user_id,
            "phase_number": phase,
            "retry_number": retry_number,
            "status": "processing",
            "input_data": input_data
        })
        .execute()
    )

    if not created.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create boardroom row"
        )

    return created.data[0]


def mark_completed(row_id, raw_output):
    updated = (
        supabase.table("boardroom_runs")
        .update({
            "status": "completed",
            "raw_output": raw_output,
            "api_output": raw_output
        })
        .eq("id", row_id)
        .execute()
    )

    return updated.data[0]


def mark_failed(row_id):
    (
        supabase.table("boardroom_runs")
        .update({
            "status": "failed"
        })
        .eq("id", row_id)
        .execute()
    )


# ==========================================================
# CORE EXECUTION
# ==========================================================

def execute_boardroom(project, phase_data, user_id, phase):
    project_id = project["id"]

    retry_number = get_next_retry(project_id, phase)

    row = create_processing_row(
        project_id=project_id,
        user_id=user_id,
        phase=phase,
        retry_number=retry_number,
        input_data=phase_data["raw_output"]
    )

    row_id = row["id"]

    try:
        debug("Calling run_phase_gate()")

        result = run_phase_gate(
            startup_name=project["name"],
            startup_stage=f"phase_{phase}",
            phase=str(phase),
            report=phase_data["raw_output"],
            metrics={
                "runway_months": 6,
                "team_size": 3,
                "confidence": 70
            }
        )

        raw_output = asdict(result)

        debug("Boardroom engine completed")

        return mark_completed(
            row_id=row_id,
            raw_output=raw_output
        )

    except Exception as e:
        debug(str(e))
        debug(traceback.format_exc())

        mark_failed(row_id)

        raise HTTPException(
            status_code=500,
            detail=f"Boardroom failed: {str(e)}"
        )


# ==========================================================
# RUN
# ==========================================================

@router.post("/api/project/{project_id}/phase/{phase}/boardroom/run")
async def run_boardroom(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    if phase < 1 or phase > 6:
        raise HTTPException(
            status_code=400,
            detail="Phase must be between 1 and 6"
        )

    project = get_project_or_404(project_id, user.id)

    phase_data = get_latest_phase(project_id, phase)

    if not phase_data:
        raise HTTPException(
            status_code=400,
            detail=f"Phase {phase} not completed yet"
        )

    latest = get_latest_boardroom(project_id, phase)

    if latest and latest["status"] == "processing":
        return latest

    if latest and latest["status"] == "completed":
        return latest

    return execute_boardroom(
        project=project,
        phase_data=phase_data,
        user_id=user.id,
        phase=phase
    )


# ==========================================================
# RETRY
# ==========================================================

@router.post("/api/project/{project_id}/phase/{phase}/boardroom/retry")
async def retry_boardroom(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    project = get_project_or_404(project_id, user.id)

    phase_data = get_latest_phase(project_id, phase)

    if not phase_data:
        raise HTTPException(
            status_code=400,
            detail=f"Phase {phase} not completed yet"
        )

    latest = get_latest_boardroom(project_id, phase)

    if latest and latest["status"] == "processing":
        raise HTTPException(
            status_code=409,
            detail="Boardroom already processing"
        )

    return execute_boardroom(
        project=project,
        phase_data=phase_data,
        user_id=user.id,
        phase=phase
    )


# ==========================================================
# GET LATEST
# ==========================================================

@router.get("/api/project/{project_id}/phase/{phase}/boardroom")
async def get_boardroom(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    latest = get_latest_boardroom(project_id, phase)

    if not latest:
        raise HTTPException(
            status_code=404,
            detail="Boardroom result not found"
        )

    return latest


# ==========================================================
# HISTORY
# ==========================================================

@router.get("/api/project/{project_id}/phase/{phase}/boardroom/history")
async def boardroom_history(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    result = (
        supabase.table("boardroom_runs")
        .select("*")
        .eq("project_id", project_id)
        .eq("phase_number", phase)
        .order("retry_number", desc=True)
        .execute()
    )

    return result.data