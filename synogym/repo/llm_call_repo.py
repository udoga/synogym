from abc import ABC, abstractmethod
from synogym.data_classes import LlmCall

class LlmCallRepo(ABC):
    @abstractmethod
    def create(self, call: LlmCall) -> LlmCall:
        pass
