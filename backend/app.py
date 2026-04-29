# backend/app.py

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routes.health import router as health_router
from .routes.projects import router as projects_router
from .routes.phases import router as phases_router


# Define the lifespan logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic goes here
    print("Foundra Backend Started")
    
    yield  # The app runs while this is suspended
    
    # Shutdown logic goes here
    print("Foundra Backend Stopped")

# ==================================================
# APP INIT
# ==================================================

app = FastAPI(
    title="Foundra Backend",
    version="1.0.0",
    description="AI Startup Operating System Backend",
    lifespan=lifespan  # Add this line
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "*"   # replace with frontend domain in prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# GLOBAL ERROR HANDLER
# ==================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "error": str(exc)
        }
    )


# ==================================================
# ROOT
# ==================================================

@app.get("/")
async def root():
    return {
        "name": "Foundra Backend",
        "version": "3.0.0",
        "status": "running"
    }


# ==================================================
# ROUTES
# ==================================================

app.include_router(health_router)
app.include_router(projects_router)
app.include_router(phases_router)


# ==================================================
# STARTUP EVENT
# ==================================================

@app.on_event("startup")
async def startup_event():
    print("Foundra Backend Started")


# ==================================================
# SHUTDOWN EVENT
# ==================================================

@app.on_event("shutdown")
async def shutdown_event():
    print("Foundra Backend Stopped")


# ==================================================
# RUN LOCAL
# uvicorn app:app --reload
# ==================================================