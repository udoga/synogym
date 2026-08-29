import os

from openai import OpenAI


class GptClient:
    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        self.model = model
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def respond(self, prompt: str) -> str:
        response = self.client.responses.create(model=self.model, input=prompt)
        return response.output_text
