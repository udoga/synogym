from synogym.repo.meaning_repo import MeaningRepo
from synogym.data_classes import Detail, Meaning

class ListMeaningRepo(MeaningRepo):
    def __init__(self):
        self.meanings: list[Meaning] = []
        self.details: list[Detail] = []

    def list_by_query(self, query: str) -> list[Meaning]:
        return [meaning for meaning in self.meanings if meaning.query == query]

    def create_all(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            meaning.id = len(self.meanings) + 1
            self.meanings.append(meaning)
        return meanings

    def find(self, meaning_id: int) -> Meaning | None:
        return next((meaning for meaning in self.meanings if meaning.id == meaning_id), None)

    def create_detail(self, detail: Detail) -> Detail:
        self.details.append(detail)
        return detail

    def find_detail(self, meaning_id: int) -> Detail | None:
        return next((detail for detail in self.details if detail.meaning_id == meaning_id), None)
