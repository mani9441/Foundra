import os
import requests
import warnings
from typing import Optional, List
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from langchain_core.language_models.llms import LLM
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

class LocalOllamaLLM(BaseChatModel):
    """
    LLM class for interacting with a local Ollama instance via HTTP API.
    """
    # Ensure these are correct for your Ollama server
    endpoint: str = os.getenv("LOCAL_OLLAMA_API_ENDPOINT", "http://localhost:11434/api/generate")
    model: str = os.getenv("LOCAL_OLLAMA_MODEL_NAME", "gemma2:2b") # Make sure this model is downloaded!

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "num_ctx": 2048 # <--- ENSURE THIS IS PRESENT AND CORRECT
        }
        #print(f"Sending payload to Ollama: {payload}") # Debugging print
        #print(f"Ollama endpoint: {self.endpoint}")     # Debugging print

        try:
            # Increase timeout just to see if it's a very slow first response
            response = requests.post(self.endpoint, json=payload, timeout=30) # Increased timeout
            response.raise_for_status()

            data = response.json()
            generated_text = data.get("response")

            if not generated_text:
                print(f"Ollama response missing 'response' field. Full data: {data}")
                raise ValueError("No 'response' field found in Ollama response.")

            return generated_text

        except requests.RequestException as e:
            # IMPORTANT: Re-raise the original RequestException so tenacity can catch it.
            # If tenacity isn't catching it, it's not seeing this specific exception type.
            print(f"[LocalOllamaLLM] Connection error (will retry if applicable): {e}")
            raise e # <-- Re-raise the exact exception type tenacity expects
        except Exception as e:
            print(f"[LocalOllamaLLM] Unexpected error: {e}")
            raise ValueError(f"[LocalOllamaLLM] Unexpected error: {e}")

    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> ChatResult:
        prompt = "\n".join([str(msg.content) for msg in messages])
        response_text = self._call(prompt, stop)
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=response_text))]
        )

    @property
    def _llm_type(self) -> str:
        return "local_ollama"
