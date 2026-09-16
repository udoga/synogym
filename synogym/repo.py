from abc import ABC, abstractmethod
from synogym.data_classes import Detail, Meaning, Quote

class Repo(ABC):
    @abstractmethod
    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        pass

    @abstractmethod
    def create_meanings(self, meanings: list[Meaning]) -> list[Meaning]:
        pass

    @abstractmethod
    def find_meaning(self, meaning_id: int) -> Meaning | None:
        pass

    @abstractmethod
    def create_detail(self, detail: Detail) -> Detail:
        pass

    @abstractmethod
    def find_detail(self, detail_id: int) -> Detail | None:
        pass

    @abstractmethod
    def list_quotes_by_query(self, query: str) -> list[Quote]:
        pass

    @abstractmethod
    def create_quotes(self, quotes: list[Quote]) -> list[Quote]:
        pass
