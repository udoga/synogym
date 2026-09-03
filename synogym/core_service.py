from dataclasses import asdict
from synogym.generator import Generator
from synogym.meaning import Detail, Meaning, MeaningWithDetail
from synogym.repo import Repo

class CoreService:
    def __init__(self, generator: Generator, repo: Repo):
        self.generator = generator
        self.repo = repo

    def list_meanings(self, query: str) -> list[Meaning]:
        meanings = self.repo.list_meanings_by_query(query)
        if meanings:
            return meanings
        return [self.repo.create_meaning(meaning) for meaning in self.generator.generate_meanings(query)]

    def read_meaning_with_detail(self, meaning_id: int) -> MeaningWithDetail:
        meaning = self.repo.read_meaning(meaning_id)
        detail = self._read_or_create_detail(meaning)
        return MeaningWithDetail(**asdict(meaning), detail=detail)

    def _read_or_create_detail(self, meaning: Meaning) -> Detail:
        try:
            return self.repo.read_detail(meaning.id)
        except ValueError:
            return self._create_detail(meaning)

    def _create_detail(self, meaning: Meaning) -> Detail:
        detail = self.generator.generate_detail(meaning)
        detail.id = meaning.id
        return self.repo.create_detail(detail)
