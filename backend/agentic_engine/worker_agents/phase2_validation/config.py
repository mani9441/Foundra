# ============================================================
# File: phase2_validation/config.py
# ============================================================

import os
from dataclasses import dataclass


@dataclass
class Settings:
    APP_NAME: str = "Phase2 Idea Validation Engine"
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "ollama")   # ollama / openai
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    REDDIT_CLIENT_ID: str = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET: str = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "phase2-agent")

    MAX_SEARCH_RESULTS: int = 5
    MAX_COMPETITORS: int = 5
    MAX_RETRIES: int = 2


settings = Settings()