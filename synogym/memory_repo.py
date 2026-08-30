from dataclasses import asdict
from synogym.meaning import Detail
from synogym.meaning import Meaning
from synogym.meaning import MeaningWithDetail

class MemoryRepo:
    def __init__(self):
        self.meanings: list[Meaning] = []
        self.details: list[Detail] = []

    def save_meaning(self, meaning: Meaning) -> Meaning:
        self.meanings.append(meaning)
        meaning.id = len(self.meanings)
        return meaning

    def save_meanings(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            self.save_meaning(meaning)
        return meanings

    def find_meanings(self, query: str) -> list[Meaning]:
        return [meaning for meaning in self.meanings if meaning.query == query]

    def find_meaning_with_detail(self, meaning_id: int | None) -> MeaningWithDetail:
        meaning = self._get_meaning(meaning_id)
        detail = self._get_detail(meaning_id)
        return MeaningWithDetail(**asdict(meaning), detail=detail)

    def save_detail(self, detail: Detail) -> MeaningWithDetail:
        meaning = self._get_meaning(detail.id)
        if any(d.id == detail.id for d in self.details):
            raise ValueError("Detail already exists")
        self.details.append(detail)
        return MeaningWithDetail(**asdict(meaning), detail=detail)

    def _get_meaning(self, meaning_id: int | None) -> Meaning:
        for meaning in self.meanings:
            if meaning.id == meaning_id:
                return meaning
        raise ValueError("Meaning not found")

    def _get_detail(self, detail_id: int | None) -> Detail:
        for detail in self.details:
            if detail.id == detail_id:
                return detail
        raise ValueError("Detail not found")
