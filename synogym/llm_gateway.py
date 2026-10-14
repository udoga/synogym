from synogym.data_classes import LlmCall, LlmResponse, LlmRequest
from synogym.generator.generator import Generator
from synogym.repo.llm_call_repo import LlmCallRepo

class LlmGateway(Generator[LlmRequest, str]):
    def __init__(self, config: dict[str, str], llm_client: Generator[str, LlmResponse], repo: LlmCallRepo):
        self.config: dict[str, str] = config
        self.llm_client: Generator[str, LlmResponse] = llm_client
        self.repo: LlmCallRepo = repo

    def generate(self, request: LlmRequest) -> str:
        response: LlmResponse = self.llm_client.generate(request.text)
        self.repo.create(self._create_llm_call(request, response))
        return response.text

    def _create_llm_call(self, request, response):
        return LlmCall(llm_name=self.config["llm_name"],
                       reasoning_effort=self.config["reasoning_effort"],
                       operation=request.operation,
                       input_token_count=response.input_token_count,
                       output_token_count=response.output_token_count,
                       first_token_latency=response.first_token_latency,
                       generation_latency=response.generation_latency)
