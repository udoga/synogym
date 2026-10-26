from abc import ABC, abstractmethod
from synogym.data_classes import Detail, Example, Meaning

class MeaningRepo(ABC):
    @abstractmethod
    def list_by_query(self, query: str) -> list[Meaning]:
        pass

    @abstractmethod
    def create_all(self, meanings: list[Meaning]) -> list[Meaning]:
        pass

    @abstractmethod
    def find(self, meaning_id: int) -> Meaning | None:
        pass

    @abstractmethod
    def create_detail(self, detail: Detail) -> Detail:
        pass

    @abstractmethod
    def find_detail(self, meaning_id: int) -> Detail | None:
        pass

    @abstractmethod
    def create_examples(self, meaning_id: int, examples: list[Example]) -> list[Example]:
        pass

    @abstractmethod
    def list_examples(self, meaning_id: int) -> list[Example]:
        pass
