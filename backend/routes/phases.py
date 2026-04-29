# backend/routes/phases.py

import json
from fastapi import APIRouter, Depends, HTTPException
from ..db.auth import get_current_user
from ..db.supabase import supabase

# ===============================
# REAL PHASE ENGINE IMPORTS
# ===============================

from backend.agentic_engine.worker_agents.phase1_problem_discovery.graph import run_phase1
from backend.agentic_engine.bridge.discovery2api import generate_phase_discovery

from backend.agentic_engine.worker_agents.phase2_validation.run_phase2_from_phase1 import run_from_phase1_file
from backend.agentic_engine.bridge.validation2api import generate_phase_validation

from backend.agentic_engine.worker_agents.phase3_market_research.run_phase3_from_phase2 import run_from_phase2_file
from backend.agentic_engine.bridge.market2api import generate_phase_market

from backend.agentic_engine.worker_agents.phase4_business_model.run_phase4_from_phase3 import run_from_phase3_file
from backend.agentic_engine.bridge.business2api import generate_business_model

from backend.agentic_engine.worker_agents.phase5_product_strategy.run_phase5_from_phase4 import run_from_phase4_file
from backend.agentic_engine.bridge.mvp2api import generate_phase_mvp

from backend.agentic_engine.worker_agents.phase6_gtm.run_phase6_from_phase5 import run_from_phase5_file
from backend.agentic_engine.bridge.gtm2api import generate_phase_launch

router = APIRouter()


# ==========================================================
# HELPERS
# ==========================================================

import tempfile
import os

def dict_to_temp_json(data: dict):
    """
    Converts dict to temp JSON file and returns file path
    """
    temp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8"
    )

    json.dump(data, temp, indent=2)
    temp.close()

    return temp.name


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


def get_latest_phase(project_id: str, phase_number: int):
    result = (
        supabase.table("phase_runs")
        .select("*")
        .eq("project_id", project_id)
        .eq("phase_number", phase_number)
        .order("retry_number", desc=True)
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def get_next_retry(project_id: str, phase_number: int):
    latest = get_latest_phase(project_id, phase_number)

    if latest:
        return latest["retry_number"] + 1

    return 1


def save_phase_run(
    project_id: str,
    user_id: str,
    phase_number: int,
    retry_number: int,
    input_data,
    raw_output,
    api_output
):
    result = (
        supabase.table("phase_runs")
        .insert({
            "project_id": project_id,
            "user_id": user_id,
            "phase_number": phase_number,
            "retry_number": retry_number,
            "status": "completed",
            "input_data": input_data,
            "raw_output": raw_output,
            "api_output": api_output
        })
        .execute()
    )

    return result.data[0]


def update_project_progress(project_id: str, phase_number: int):
    percent = int((phase_number / 6) * 100)

    (
        supabase.table("projects")
        .update({
            "current_phase": phase_number,
            "completion_percent": percent
        })
        .eq("id", project_id)
        .execute()
    )


# ==========================================================
# CORE PHASE EXECUTION
# ==========================================================


def normalize_json_output(data):
    """
    Accepts dict / list / JSON string.
    Returns Python object.
    """

    if isinstance(data, (dict, list)):
        return data

    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {
                "raw_text": data
            }

    return {
        "raw_output": str(data)
    }


def execute_phase(project: dict, phase: int):
    """
    Executes real AI engines.
    Returns raw_output, api_output
    """

    if phase == 1:
        raw = run_phase1(project)
        api = normalize_json_output(generate_phase_discovery(raw))
        return raw, api

    previous = get_latest_phase(project["id"], phase - 1)

    if not previous:
        raise HTTPException(
            status_code=400,
            detail=f"Previous phase {phase - 1} not completed"
        )

    previous_data = previous["raw_output"]

    # Convert dict → temp file
    temp_file = dict_to_temp_json(previous_data)

    previous_data = temp_file

    if phase == 2:
        raw = run_from_phase1_file(previous_data)
        api = normalize_json_output(generate_phase_validation(raw))
        return raw, api

    if phase == 3:
        raw = run_from_phase2_file(previous_data)
        api = normalize_json_output(generate_phase_market(raw))
        return raw, api

    if phase == 4:
        raw = run_from_phase3_file(previous_data)
        api = normalize_json_output(generate_business_model(raw))
        return raw, api

    if phase == 5:
        raw = run_from_phase4_file(previous_data)
        api = normalize_json_output(generate_phase_mvp(raw))
        return raw, api

    if phase == 6:
        raw = run_from_phase5_file(previous_data)
        api = normalize_json_output(generate_phase_launch(raw))
        return raw, api

    raise HTTPException(status_code=400, detail="Invalid phase number")


# ==========================================================
# RUN PHASE
# ==========================================================

@router.post("/api/project/{project_id}/phase/{phase}/run")
async def run_phase_route(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    if phase < 1 or phase > 6:
        raise HTTPException(status_code=400, detail="Phase must be 1 to 6")

    project = get_project_or_404(project_id, user.id)

    retry = get_next_retry(project_id, phase)

    raw_output, api_output = execute_phase(project, phase)

    saved = save_phase_run(
        project_id=project_id,
        user_id=user.id,
        phase_number=phase,
        retry_number=retry,
        input_data=project,
        raw_output=raw_output,
        api_output=api_output
    )

    update_project_progress(project_id, phase)

    return saved


# ==========================================================
# RETRY PHASE
# ==========================================================

@router.post("/api/project/{project_id}/phase/{phase}/retry")
async def retry_phase(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    # --------------------------------------------
    # Validate phase range
    # --------------------------------------------
    if phase < 1 or phase > 6:
        raise HTTPException(
            status_code=400,
            detail="Phase must be between 1 and 6"
        )

    # --------------------------------------------
    # Ensure project belongs to user
    # --------------------------------------------
    project = get_project_or_404(project_id, user.id)

    # --------------------------------------------
    # Prevent duplicate parallel retries
    # --------------------------------------------
    existing = (
        supabase.table("phase_runs")
        .select("id")
        .eq("project_id", project_id)
        .eq("phase_number", phase)
        .eq("status", "processing")
        .limit(1)
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=409,
            detail="This phase is already processing."
        )

    # --------------------------------------------
    # New retry number
    # --------------------------------------------
    retry = get_next_retry(project_id, phase)

    # --------------------------------------------
    # Insert processing row first
    # --------------------------------------------
    created = (
        supabase.table("phase_runs")
        .insert({
            "project_id": project_id,
            "user_id": user.id,
            "phase_number": phase,
            "retry_number": retry,
            "status": "processing",
            "input_data": project,
        })
        .execute()
    )

    if not created.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create retry run."
        )

    row_id = created.data[0]["id"]

    try:
        # --------------------------------------------
        # Execute phase
        # --------------------------------------------
        raw_output, api_output = execute_phase(project, phase)

        # --------------------------------------------
        # Mark completed
        # --------------------------------------------
        updated = (
            supabase.table("phase_runs")
            .update({
                "status": "completed",
                "raw_output": raw_output,
                "api_output": api_output,
            })
            .eq("id", row_id)
            .execute()
        )

        update_project_progress(project_id, phase)

        return {
            "success": True,
            "message": "Retry completed successfully.",
            "run": updated.data[0]
        }

    except Exception as e:
        # --------------------------------------------
        # Mark failed
        # --------------------------------------------
        supabase.table("phase_runs").update({
            "status": "failed"
        }).eq("id", row_id).execute()

        raise HTTPException(
            status_code=500,
            detail=f"Retry failed: {str(e)}"
        )

# ==========================================================
# GET LATEST PHASE
# ==========================================================

@router.get("/api/project/{project_id}/phase/{phase}")
async def get_phase(
    project_id: str,
    phase: int,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    latest = get_latest_phase(project_id, phase)

    if not latest:
        raise HTTPException(status_code=404, detail="Phase not found")

    return latest


# ==========================================================
# GET ALL RUN HISTORY
# ==========================================================

@router.get("/api/project/{project_id}/history")
async def project_history(
    project_id: str,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    result = (
        supabase.table("phase_runs")
        .select("*")
        .eq("project_id", project_id)
        .order("phase_number")
        .order("retry_number")
        .execute()
    )

    return result.data