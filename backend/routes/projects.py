# backend/routes/projects.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..db.auth import get_current_user
from ..db.supabase import supabase

router = APIRouter()


# ==================================================
# REQUEST MODELS
# ==================================================

class CreateProjectRequest(BaseModel):
    name: str
    idea: Optional[str] = None
    industry: Optional[str] = None
    target_market: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    name: Optional[str] = None
    idea: Optional[str] = None
    industry: Optional[str] = None
    target_market: Optional[str] = None
    status: Optional[str] = None


# ==================================================
# HELPERS
# ==================================================

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


# ==================================================
# CREATE PROJECT
# ==================================================

@router.post("/api/projects/create")
async def create_project(
    data: CreateProjectRequest,
    user=Depends(get_current_user)
):
    result = (
        supabase.table("projects")
        .insert({
            "user_id": user.id,
            "name": data.name,
            "idea": data.idea,
            "industry": data.industry,
            "target_market": data.target_market,
            "status": "active",
            "current_phase": 0,
            "completion_percent": 0
        })
        .execute()
    )

    return result.data[0]


# ==================================================
# LIST PROJECTS
# ==================================================

@router.get("/api/projects")
async def list_projects(
    user=Depends(get_current_user)
):
    result = (
        supabase.table("projects")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .execute()
    )

    return result.data


# ==================================================
# GET SINGLE PROJECT
# ==================================================

@router.get("/api/project/{project_id}")
async def get_project(
    project_id: str,
    user=Depends(get_current_user)
):
    return get_project_or_404(project_id, user.id)


# ==================================================
# UPDATE PROJECT
# ==================================================

@router.put("/api/project/{project_id}")
async def update_project(
    project_id: str,
    data: UpdateProjectRequest,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    payload = {}

    if data.name is not None:
        payload["name"] = data.name

    if data.idea is not None:
        payload["idea"] = data.idea

    if data.industry is not None:
        payload["industry"] = data.industry

    if data.target_market is not None:
        payload["target_market"] = data.target_market

    if data.status is not None:
        payload["status"] = data.status

    result = (
        supabase.table("projects")
        .update(payload)
        .eq("id", project_id)
        .eq("user_id", user.id)
        .execute()
    )

    return result.data[0]


# ==================================================
# DELETE PROJECT
# ==================================================

@router.delete("/api/project/{project_id}")
async def delete_project(
    project_id: str,
    user=Depends(get_current_user)
):
    get_project_or_404(project_id, user.id)

    (
        supabase.table("projects")
        .delete()
        .eq("id", project_id)
        .eq("user_id", user.id)
        .execute()
    )

    return {"success": True}


# ==================================================
# PROJECT DASHBOARD SUMMARY
# ==================================================

@router.get("/api/project/{project_id}/summary")
async def project_summary(
    project_id: str,
    user=Depends(get_current_user)
):
    project = get_project_or_404(project_id, user.id)

    runs = (
        supabase.table("phase_runs")
        .select("phase_number,retry_number")
        .eq("project_id", project_id)
        .execute()
    )

    total_runs = len(runs.data)

    completed_phases = len(
        set([row["phase_number"] for row in runs.data])
    )

    return {
        "project": project,
        "total_runs": total_runs,
        "completed_phases": completed_phases,
        "completion_percent": project["completion_percent"]
    }



# ==================================================
# INTIATE PHASE 1
# ==================================================

@router.post("/api/projects/{project_id}/initialize-phase-1")
async def initialize_phase_1(
    project_id: str,
    data: CreateProjectRequest,
    user=Depends(get_current_user)
):
    # 1. Verify project ownership [cite: 87]
    get_project_or_404(project_id, user.id)

    try:
        # 2. Execute AI Engine (Phase 1) [cite: 95]
        # Uses the strategic context from the second form
        from .phases import execute_phase, save_phase_run, update_project_progress
        
        raw_out, api_out = execute_phase(data.dict(), 1)
        
        # 3. Save findings to phase_runs [cite: 94]
        save_phase_run(
            project_id=project_id,
            user_id=user.id,
            phase_number=1,
            retry_number=0,
            input_data=data.dict(),
            raw_output=raw_out,
            api_output=api_out
        )

        # 4. Advance progress to Phase 1 [cite: 95]
        update_project_progress(project_id, 1)

        return {"status": "success", "project_id": project_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")