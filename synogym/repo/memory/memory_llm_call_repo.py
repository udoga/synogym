from synogym.repo.interface import LlmCallRepo
from synogym.data_classes import LlmCall

class MemoryLlmCallRepo(LlmCallRepo):
    def __init__(self):
        self.calls: list[LlmCall] = []

    def create(self, call: LlmCall) -> LlmCall:
        self.calls.append(call)
        return call
