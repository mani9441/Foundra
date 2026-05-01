import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
TEMP = float(os.getenv("LLM_TEMPERATURE", "0.2"))

### API KEYS ###
google_api_key = os.getenv("MY_GOOGLE_KEY1")
groq_api_key = os.getenv("MY_GROQ_KEY1")
github_api_key = os.getenv("MY_GITHUB_TOKEN1")

def get_llm(PROVIDER=PROVIDER, MODEL=MODEL, TEMP=TEMP):
    """
    Universal LLM loader (env-only, hardcoded keys)
    """

    # GOOGLE
    if PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        
        if not google_api_key:
            raise ValueError("MY_GOOGLE_KEY not set")

        return ChatGoogleGenerativeAI(
            model=MODEL or "gemini-1.5-pro",
            temperature=TEMP,
            google_api_key=google_api_key   
        )

    # GROQ
    elif PROVIDER == "groq":
        from langchain_groq import ChatGroq

        if not groq_api_key:
            raise ValueError("MY_GROQ_KEY not set")

        return ChatGroq(
            model=MODEL or "llama-3.1-8b-instant",
            temperature=TEMP,
            api_key=groq_api_key   
        )

    # GITHUB
    elif PROVIDER == "github":
        from langchain_openai import ChatOpenAI

        if not github_api_key:
            raise ValueError("MY_GITHUB_TOKEN not set")

        return ChatOpenAI(
            model=MODEL or "gpt-4o-mini",
            temperature=TEMP,
            api_key=github_api_key,
            base_url="https://models.github.ai/inference"
        )

    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")