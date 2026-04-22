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


warnings.filterwarnings("ignore")
load_dotenv()

class RemoteOllamaLLM(BaseChatModel):
    """
    Custom LLM class to interface with a remote Ollama server
    exposed via a REST API (e.g., Flask).

    Reads configuration from environment variables:
    - OLLAMA_API_ENDPOINT
    - OLLAMA_MODEL_NAME
    """

    endpoint: str = os.getenv("OLLAMA_API_ENDPOINT", "http://localhost:8000/generate")
    model: str = os.getenv("OLLAMA_MODEL_NAME", "gemma2:2b")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(requests.RequestException)
    )
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Sends the prompt to the remote Ollama server and retrieves the response.
        """
        payload = {
            "prompt": prompt,
            "model": self.model
        }
        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            generated_text = data.get("generated_text")
            if not generated_text:
                raise ValueError("Response missing 'generated_text' field.")
            return generated_text

        except requests.RequestException as e:
            raise ValueError(f"[RemoteOllamaLLM] Connection error: {e}")
        except Exception as e:
            raise ValueError(f"[RemoteOllamaLLM] Unexpected error: {e}")

    def __call__(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Make the instance callable, forwarding to _call.
        """
        return self._call(prompt, stop)
    
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None) -> ChatResult:
        prompt = "\n".join([str(msg.content) for msg in messages])  # <-- fix here
        response_text = self._call(prompt, stop)  # your original call method
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=response_text))]
        )



    @property
    def _llm_type(self) -> str:
        return "remote_ollama"
