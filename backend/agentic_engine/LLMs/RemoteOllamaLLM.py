# ==========================================================
# CLIENT CODE (LangChain Remote Streaming Ollama)
# save as remote_ollama.py
# ==========================================================

import json
import requests

from typing import Any, List, Optional, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult


class RemoteOllama(BaseChatModel):

    model: str = "phi3"
    base_url: str = "http://localhost:8000"
    temperature: float = 0.0
    timeout: int = 300
    verbose_stream: bool = False

    # ------------------------------------------------

    def _endpoint(self):
        return self.base_url.rstrip("/") + "/generate"

    # ------------------------------------------------

    def _messages_to_prompt(
        self,
        messages: List[BaseMessage]
    ) -> str:

        parts = []

        for msg in messages:

            if isinstance(msg, SystemMessage):
                parts.append(f"System: {msg.content}")

            elif isinstance(msg, HumanMessage):
                parts.append(f"User: {msg.content}")

            else:
                parts.append(f"Assistant: {msg.content}")

        parts.append("Assistant:")

        return "\n".join(parts)

    # ------------------------------------------------

    def _request(self, prompt: str) -> str:

        response = requests.post(
            self._endpoint(),
            json={
                "prompt": prompt,
                "model": self.model,
                "temperature": self.temperature
            },
            stream=True,
            timeout=(20, None)   # connect timeout, no read timeout
        )

        response.raise_for_status()

        full_text = ""

        for line in response.iter_lines(decode_unicode=True):

            if not line:
                continue

            try:
                data = json.loads(line)

                token = data.get("response", "")

                if token:
                    full_text += token

                    if self.verbose_stream:
                        print(token, end="", flush=True)

            except:
                continue

        if self.verbose_stream:
            print()

        return full_text.strip()
    # ------------------------------------------------

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> ChatResult:

        prompt = self._messages_to_prompt(messages)

        text = self._request(prompt)

        if stop:
            for token in stop:
                if token in text:
                    text = text.split(token)[0]

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=text)
                )
            ]
        )

    # ------------------------------------------------

    def invoke(
        self,
        input: Union[str, List[BaseMessage]],
        config=None,
        **kwargs
    ):
        return super().invoke(
            input,
            config=config,
            **kwargs
        )

    @property
    def _llm_type(self):
        return "remote_ollama"