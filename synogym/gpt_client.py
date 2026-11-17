import os
from typing import Any
from synogym.data_classes import LlmRequest
from synogym.generator import Generator
from langfuse import Langfuse

class GptClient(Generator[LlmRequest, str]):
    def __init__(self, config: dict[str, Any]):
        self.llm_name = config["llm_name"]
        self.reasoning_effort = config["reasoning_effort"]
        self.langfuse: Langfuse | None = self._create_langfuse(config["langfuse"])
        self.client: Any = self._create_client(config)

    def generate(self, request: LlmRequest) -> str:
        return self._stream(self._create_arguments(request))

    def _create_langfuse(self, config: dict[str, Any]) -> Langfuse | None:
        if not bool(config.get("enabled")): return None
        return Langfuse(public_key=config.get("public_key") or None,
                        secret_key=config.get("secret_key") or None,
                        base_url=config.get("base_url") or None,
                        environment=config.get("environment") or None)

    def _create_client(self, config: dict[str, Any]) -> Any:
        if self.langfuse:
            from langfuse.openai import OpenAI
        else:
            from openai import OpenAI
        return OpenAI(api_key=config["openai_api_key"] or os.environ.get("OPENAI_API_KEY"))

    def _create_arguments(self, request: LlmRequest) -> dict[str, Any]:
        arguments: dict[str, Any] = {"model": self.llm_name, "input": request.text}
        if self.langfuse:
            arguments["name"] = request.name
        if self.reasoning_effort:
            arguments["reasoning"] = {"effort": self.reasoning_effort}
        return arguments

    def _stream(self, arguments: dict[str, Any]) -> str:
        output: list[str] = []
        with self.client.responses.create(stream=True, **arguments) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    output.append(event.delta)
        return "".join(output)
