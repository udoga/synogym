from dataclasses import asdict
from synogym.data_classes import Detail, Meaning, MeaningWithDetail
from synogym.generator import Generator
from synogym.meaning_repo import MeaningRepo

class MeaningService:
    def __init__(self, repo: MeaningRepo,
                 meaning_generator: Generator[str, list[Meaning]],
                 detail_generator: Generator[Meaning, Detail]):
        self.repo = repo
        self.meaning_generator = meaning_generator
        self.detail_generator = detail_generator

    def list_by_query(self, query: str) -> list[Meaning]:
        meanings = self.repo.list_by_query(query)
        return meanings or self.repo.create_all(self.meaning_generator.generate(query))

    def read_meaning_with_detail(self, meaning_id: int) -> MeaningWithDetail:
        meaning = self.repo.find(meaning_id)
        if not meaning: raise ValueError("Meaning not found")
        detail = self.repo.find_detail(meaning_id) or self.repo.create_detail(self.detail_generator.generate(meaning))
        return MeaningWithDetail(**asdict(meaning), detail=detail)
