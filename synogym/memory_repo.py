from synogym.repo import Repo
from synogym.data_classes import Detail, Meaning

class MemoryRepo(Repo):
    def __init__(self):
        self.meanings: list[Meaning] = []
        self.details: list[Detail] = []

    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        return [meaning for meaning in self.meanings if meaning.query == query]

    def create_meaning(self, meaning: Meaning) -> Meaning:
        self.meanings.append(meaning)
        meaning.id = len(self.meanings)
        return meaning

    def read_meaning(self, meaning_id: int | None) -> Meaning:
        for meaning in self.meanings:
            if meaning.id == meaning_id:
                return meaning
        raise ValueError("Meaning not found")

    def create_detail(self, detail: Detail) -> Detail:
        self.read_meaning(detail.id)
        if any(d.id == detail.id for d in self.details):
            raise ValueError("Detail already exists")
        self.details.append(detail)
        return detail

    def read_detail(self, detail_id: int | None) -> Detail:
        for detail in self.details:
            if detail.id == detail_id:
                return detail
        raise ValueError("Detail not found")
