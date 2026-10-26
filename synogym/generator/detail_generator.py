from dataclasses import asdict
from synogym.generator import Generator
from synogym.parser import DetailParser
from synogym.data_classes import Detail, LlmRequest, Meaning

class DetailGenerator(Generator[Meaning, Detail]):
    PROMPT = """You are a dictionary API for English learners.
Given a word or phrase, its selected definition and pos; return only YAML in the structure below.

detail:
  level: A1 | A2 | B1 | B2 | C1 | C2
  description: around 3 learner-friendly sentences explaining this meaning
  synonyms: comma separated best synonyms, ideally 10, each 1-2 words
  history: a brief paragraph of why it has this name or where it came from
  formations: comma separated different words sharing the same root, ideally 10, each 1 word

Rules:
- ONLY content, no markdown, no additional text, no quotation marks.

Query: {query}
Definition: {definition}
Part of speech: {pos}
"""

    def __init__(self, generator: Generator[LlmRequest, str]):
        self.generator: Generator[LlmRequest, str] = generator
        self.parser = DetailParser()

    def generate(self, meaning: Meaning) -> Detail:
        prompt: str = self.PROMPT.format(**asdict(meaning))
        text: str = self.generator.generate(LlmRequest(prompt, "detail"))
        detail: Detail = self.parser.parse(text)
        detail.meaning_id = meaning.id
        return detail
