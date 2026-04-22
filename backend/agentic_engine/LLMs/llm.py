import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL = os.getenv("LLM_MODEL", "")
TEMP = float(os.getenv("LLM_TEMPERATURE", "0.2"))


def get_llm():
    """
    Universal LLM loader
    """

    # if PROVIDER == "openai":
    #     from langchain_openai import ChatOpenAI 
    #     return ChatOpenAI(
    #         model=MODEL or "gpt-4o-mini",
    #         temperature=TEMP
    #     )

    # elif PROVIDER == "anthropic":
    #     from langchain_anthropic import ChatAnthropic 
    #     return ChatAnthropic(
    #         model=MODEL or "claude-3-5-sonnet-latest",
    #         temperature=TEMP
    #    )

    if PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI 
        return ChatGoogleGenerativeAI(
            model=MODEL or "gemini-1.5-pro",
            temperature=TEMP
        )

    elif PROVIDER == "ollama":
        print("Using Ollama...")
        
        from langchain_ollama import ChatOllama 
        
        return ChatOllama(
            model=MODEL or "llama3",
            temperature=TEMP,
            base_url="http://127.0.0.1:11434" # Change this as needed
        )

    # elif PROVIDER == "groq":
    #     from langchain_openai import ChatOpenAI 
    #     return ChatOpenAI(
    #         base_url="https://api.groq.com/openai/v1",
    #         api_key=os.getenv("GROQ_API_KEY"),
    #         model=MODEL or "llama-3.3-70b-versatile",
    #         temperature=TEMP
    #     )

    elif PROVIDER == "groq":
        from langchain_groq import ChatGroq
        
        return ChatGroq(
            model=MODEL or "llama-3.1-8b-instant",
            temperature=TEMP,
            # Optional: custom endpoint if you're using a proxy
            # base_url="https://api.groq.com/openai/v1", 
            # api_key="your_api_key_here" # Or set GROQ_API_KEY env var
        )

    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")
