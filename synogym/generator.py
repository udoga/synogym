from abc import ABC, abstractmethod
from synogym.meaning import Detail, Meaning

class Generator(ABC):
    @abstractmethod
    def generate_meanings(self, query: str) -> list[Meaning]:
        pass

    @abstractmethod
    def generate_detail(self, meaning: Meaning) -> Detail:
        pass
