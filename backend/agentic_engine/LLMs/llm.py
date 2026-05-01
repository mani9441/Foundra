import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL = os.getenv("LLM_MODEL", "")
TEMP = float(os.getenv("LLM_TEMPERATURE", "0.2"))


def require_env(key: str):
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} not found in environment variables")
    return value

def get_llm(PROVIDER=PROVIDER, MODEL=MODEL, TEMP=TEMP):
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
        require_env("GOOGLE_API_KEY")
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
    


    elif PROVIDER == "ollama_remote":

        from ..LLMs.RemoteOllamaLLM import RemoteOllama

        return RemoteOllama(
            model=MODEL or "phi3",
            temperature=TEMP,
            base_url="http://172.23.105.40:8000",
            verbose_stream=True
        )


    elif PROVIDER == "groq":
        from langchain_groq import ChatGroq
        require_env("GROQ_API_KEY")
        
        return ChatGroq(
            model=MODEL or "llama-3.1-8b-instant",
            temperature=TEMP,
            # Optional: custom endpoint if you're using a proxy
            # base_url="https://api.groq.com/openai/v1", 
            # api_key="your_api_key_here" # Or set GROQ_API_KEY env var
        )
    
    elif PROVIDER == "github":
        """
        GitHub Models via Azure OpenAI-compatible endpoint
        Supports fallback between multiple tokens
        """

        from langchain_openai import ChatOpenAI

        tokens = [
            os.getenv("MY_GITHUB_TOKEN_1"),
            os.getenv("MY_GITHUB_TOKEN_2"),
            os.getenv("MY_GITHUB_TOKEN_3"),
        ]

        # Remove empty ones
        tokens = [t for t in tokens if t]

        if not tokens:
            raise ValueError("No GitHub tokens found")

        last_error = None

        for token in tokens:
            try:
                llm = ChatOpenAI(
                    model=MODEL or "gpt-4o-mini",
                    temperature=TEMP,
                    api_key=token,
                    base_url="https://models.github.ai/inference"
                )

                # Test call (important)
                llm.invoke("ping")

                print("Using GitHub token:", token[:5], "...")
                return llm

            except Exception as e:
                print(f"[GitHub] Token failed: {token[:5]}... → {e}")
                last_error = e
                continue

        raise RuntimeError(f"All GitHub tokens failed: {last_error}")


    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")
