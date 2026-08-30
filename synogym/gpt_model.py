import os
from typing import Any
from openai import OpenAI

class GptModel:
    def __init__(self, model: str = "gpt-5", api_key: str = "", reasoning_effort: str = ""):
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def respond(self, prompt: str) -> str:
        arguments: dict[str, Any] = {"model": self.model, "input": prompt}
        if self.reasoning_effort:
            arguments["reasoning"] = {"effort": self.reasoning_effort}
        return self.client.responses.create(**arguments).output_text
