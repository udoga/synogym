from dataclasses import replace
from synogym.data_classes import ComparisonRequest, Detail, Example, Meaning
from synogym.generator import Generator
from synogym.highlighter import Highlighter
from synogym.repo.interface import MeaningRepo

class MeaningService:
    def __init__(self, repo: MeaningRepo,
                 meaning_generator: Generator[str, list[Meaning]],
                 detail_generator: Generator[Meaning, Detail],
                 example_generator: Generator[Meaning, list[Example]],
                 comparison_generator: Generator[ComparisonRequest, str]):
        self.repo = repo
        self.meaning_generator = meaning_generator
        self.detail_generator = detail_generator
        self.example_generator = example_generator
        self.comparison_generator = comparison_generator
        self.highlighter = Highlighter()

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
        examples = examples or self.repo.create_examples(meaning_id, self.example_generator.generate(meaning))
        return [self._highlight(e, meaning.query) for e in examples]

    def read_detail(self, meaning_id: int) -> Detail:
        meaning = self.read_meaning(meaning_id)
        detail = self.repo.find_detail(meaning_id)
        return detail or self.repo.create_detail(self.detail_generator.generate(meaning))

    def compare(self, meaning_id: int, selection: str, selection_type: str = "synonym") -> str:
        meaning = self.read_meaning(meaning_id)
        return self.comparison_generator.generate(ComparisonRequest(meaning, selection, selection_type))

    def _highlight(self, example: Example, query: str) -> Example:
        sentence: str = self.highlighter.highlight(example.sentence, query)
        return replace(example, sentence=sentence)
