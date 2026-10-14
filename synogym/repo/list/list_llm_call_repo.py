from synogym.repo.llm_call_repo import LlmCallRepo
from synogym.data_classes import Quote, LlmCall

class ListLlmCallRepo(LlmCallRepo):
    def __init__(self):
        self.calls: list[LlmCall] = []

    def create(self, call: LlmCall) -> LlmCall:
        self.calls.append(call)
        return call
