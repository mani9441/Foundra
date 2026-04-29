from fastapi import APIRouter

router = APIRouter()

@router.get("/api/health")
async def health():
    return {
        "status": "running",
        "service": "Foundra Backend V2"
    }