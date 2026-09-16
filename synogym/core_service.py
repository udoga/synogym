from dataclasses import asdict
from synogym.generator import Generator
from synogym.data_classes import Detail, Meaning, MeaningWithDetail, Quote
from synogym.repo import Repo

class CoreService:
    def __init__(self,
                 repo: Repo,
                 meaning_generator: Generator[str, list[Meaning]],
                 detail_generator: Generator[Meaning, Detail],
                 quote_generator: Generator[str, list[Quote]]):
        self.repo = repo
        self.meaning_generator = meaning_generator
        self.detail_generator = detail_generator
        self.quote_generator = quote_generator

    def list_meanings(self, query: str) -> list[Meaning]:
        meanings = self.repo.list_meanings_by_query(query)
        if meanings:
            return meanings
        return [self.repo.create_meaning(meaning) for meaning in self.meaning_generator.generate(query)]

    def read_meaning_with_detail(self, meaning_id: int) -> MeaningWithDetail:
        meaning = self.repo.read_meaning(meaning_id)
        detail = self._read_or_create_detail(meaning)
        return MeaningWithDetail(**asdict(meaning), detail=detail)

    def list_quotes(self, query: str) -> list[Quote]:
        return self.quote_generator.generate(query)

    def _read_or_create_detail(self, meaning: Meaning) -> Detail:
        try:
            return self.repo.read_detail(meaning.id)
        except ValueError:
            return self._create_detail(meaning)

    def _create_detail(self, meaning: Meaning) -> Detail:
        detail = self.detail_generator.generate(meaning)
        detail.id = meaning.id
        return self.repo.create_detail(detail)
