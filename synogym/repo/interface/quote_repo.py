from abc import ABC, abstractmethod
from synogym.data_classes import Quote

class QuoteRepo(ABC):
    @abstractmethod
    def list_by_inflections(self, inflections: list[str]) -> list[Quote]:
        pass

    @abstractmethod
    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        pass
