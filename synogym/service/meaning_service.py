from synogym.data_classes import Detail, Example, Meaning
from synogym.generator import Generator
from synogym.repo.interface import MeaningRepo

class MeaningService:
    def __init__(self, repo: MeaningRepo,
                 meaning_generator: Generator[str, list[Meaning]],
                 detail_generator: Generator[Meaning, Detail],
                 example_generator: Generator[Meaning, list[Example]]):
        self.repo = repo
        self.meaning_generator = meaning_generator
        self.detail_generator = detail_generator
        self.example_generator = example_generator

    def list_by_query(self, query: str) -> list[Meaning]:
        meanings = self.repo.list_by_query(query)
        return meanings or self.repo.create_all(self.meaning_generator.generate(query))

    def read_meaning(self, meaning_id: int) -> Meaning:
        meaning = self.repo.find(meaning_id)
        if not meaning: raise ValueError("Meaning not found")
        return meaning

    def list_examples(self, meaning_id: int) -> list[Example]:
        meaning = self.read_meaning(meaning_id)
        examples = self.repo.list_examples(meaning_id)
        return examples or self.repo.create_examples(meaning_id, self.example_generator.generate(meaning))

    def read_detail(self, meaning_id: int) -> Detail:
        meaning = self.read_meaning(meaning_id)
        detail = self.repo.find_detail(meaning_id)
        return detail or self.repo.create_detail(self.detail_generator.generate(meaning))
