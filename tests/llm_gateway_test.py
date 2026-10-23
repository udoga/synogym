from unittest import TestCase
from synogym.data_classes import LlmCall, LlmResponse, LlmRequest
from synogym.generator.generator import Generator
from synogym.llm_gateway import LlmGateway
from synogym.repo.memory.memory_llm_call_repo import MemoryLlmCallRepo

class MockLlmClient(Generator[str, LlmResponse]):
    def generate(self, request: LlmRequest) -> LlmResponse:
        return LlmResponse(text="answer",
                           input_token_count=3,
                           output_token_count=4,
                           first_token_latency=0.1,
                           generation_latency=0.2)

class LlmGatewayTest(TestCase):
    def test_saves_llm_call_and_returns_model_response(self):
        config = {"llm_name": "gpt-5", "reasoning_effort": "minimal"}
        llm_client = MockLlmClient()
        repo = MemoryLlmCallRepo()
        generator = LlmGateway(config, llm_client, repo)
        self.assertEqual("answer", generator.generate(LlmRequest("prompt", "detail")))
        self.assertEqual([LlmCall(llm_name="gpt-5", reasoning_effort="minimal", operation="detail",
                                  input_token_count=3, output_token_count=4, first_token_latency=0.1,
                                  generation_latency=0.2)], repo.calls)
