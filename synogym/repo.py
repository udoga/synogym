from abc import ABC, abstractmethod
from synogym.data_classes import Detail, Meaning, Quote

class Repo(ABC):
    @abstractmethod
    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        pass

    @abstractmethod
    def create_meaning(self, meaning: Meaning) -> Meaning:
        pass

    @abstractmethod
    def read_meaning(self, meaning_id: int | None) -> Meaning:
        pass

    @abstractmethod
    def create_detail(self, detail: Detail) -> Detail:
        pass

    @abstractmethod
    def read_detail(self, detail_id: int | None) -> Detail:
        pass

    @abstractmethod
    def list_quotes_by_query(self, query: str) -> list[Quote]:
        pass

    @abstractmethod
    def create_quote(self, quote: Quote) -> Quote:
        pass
