import os
from time import perf_counter
from typing import Any
from openai import OpenAI
from synogym.data_classes import LlmResponse
from synogym.generator.generator import Generator

class GptClient(Generator[str, LlmResponse]):
    def __init__(self, config: dict[str, str]):
        self.llm_name = config["llm_name"]
        self.client = OpenAI(api_key=config["openai_api_key"] or os.environ.get("OPENAI_API_KEY"))
        self.reasoning_effort = config["reasoning_effort"]

    def generate(self, prompt: str) -> LlmResponse:
        return self._stream_response(self._get_arguments(prompt))

    def _get_arguments(self, prompt: str) -> dict[str, Any]:
        arguments: dict[str, Any] = {"model": self.llm_name, "input": prompt}
        if self.reasoning_effort:
            arguments["reasoning"] = {"effort": self.reasoning_effort}
        return arguments

    def _stream_response(self, arguments: dict[str, Any]) -> LlmResponse:
        started_at = perf_counter()
        with self.client.responses.stream(**arguments) as stream:
            first_token_at = self._get_first_token_at(stream)
            response = stream.get_final_response()
        finished_at = perf_counter()
        return self._get_llm_response(response, started_at, first_token_at, finished_at)

    def _get_first_token_at(self, stream) -> float | None:
        for event in stream:
            if event.type == "response.output_text.delta":
                return perf_counter()
        return None

    def _get_llm_response(self, response, started_at, first_token_at, finished_at):
        return LlmResponse(text=response.output_text,
                           input_token_count=response.usage.input_tokens,
                           output_token_count=response.usage.output_tokens,
                           first_token_latency=(first_token_at - started_at),
                           generation_latency=(finished_at - first_token_at))
