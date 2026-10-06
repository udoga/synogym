from typing import Any
from openai import OpenAI
from synogym.generator.generator import Generator

class GptModel(Generator[str, str]):
    def __init__(self, model: str = "gpt-5", api_key: str = "", reasoning_effort: str = ""):
        self.model = model
        self.client = OpenAI(api_key=api_key)
        self.reasoning_effort = reasoning_effort

    def generate(self, prompt: str) -> str:
        arguments: dict[str, Any] = {"model": self.model, "input": prompt}
        if self.reasoning_effort:
            arguments["reasoning"] = {"effort": self.reasoning_effort}
        return self.client.responses.create(**arguments).output_text
