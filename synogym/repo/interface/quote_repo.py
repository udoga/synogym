from abc import ABC, abstractmethod
from synogym.data_classes import Quote

class QuoteRepo(ABC):
    @abstractmethod
    def list_by_query(self, query: str) -> list[Quote]:
        pass

    @abstractmethod
    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        pass
