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

    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        meanings = self.repo.list_meanings_by_query(query)
        return meanings or self.repo.create_meanings(self.meaning_generator.generate(query))

    def read_meaning_with_detail(self, meaning_id: int) -> MeaningWithDetail:
        meaning = self.repo.find_meaning(meaning_id)
        if not meaning: raise ValueError("Meaning not found")
        detail = self.repo.find_detail(meaning_id) or self.repo.create_detail(self.detail_generator.generate(meaning))
        return MeaningWithDetail(**asdict(meaning), detail=detail)

    def list_quotes_by_query(self, query: str) -> list[Quote]:
        quotes = self.repo.list_quotes_by_query(query)
        return quotes if len(quotes) >= 10 else self.repo.create_quotes(self.quote_generator.generate(query))
