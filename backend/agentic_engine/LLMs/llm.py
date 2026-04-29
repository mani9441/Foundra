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
        Need:
        GITHUB_TOKEN=your_pat_token
        """

        from langchain_openai import ChatOpenAI

        github_token = os.getenv("GITHUB_TOKEN")

        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in .env")

        return ChatOpenAI(
            model=MODEL or "gpt-4o-mini",
            temperature=TEMP,
            api_key=github_token,
            base_url="https://models.github.ai/inference"
        )


    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")
