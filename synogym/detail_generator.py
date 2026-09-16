from dataclasses import asdict
from synogym.generator import Generator
from synogym.detail_parser import DetailParser
from synogym.data_classes import Detail, Meaning

class DetailGenerator(Generator[Meaning, Detail]):
    PROMPT = """You are a dictionary API for English learners.
Given a word or phrase, its part of speech, and its selected definition, return only YAML in the structure below.

detail:
  level: A1 | A2 | B1 | B2 | C1 | C2
  description: 2-3 learner-friendly sentences explaining this meaning
  synonyms: best synonym list, up to 10, each 1-2 words
  examples: exactly 3 versatile examples
    - sentence: a clear and common usage example
      replacements: 2 best alternatives for the word in this context, each 1-2 words
  history: a brief paragraph of why it has this name or where it came from, Unknown if uncertain
  formations: words with the same root and similar meaning, up to 10, e.g. competitor, competence

Rules:
- Only YAML, no markdown, no additional text, no quotation marks.

Query: {query}
Definition: {definition}
Part of speech: {pos}
"""

    def __init__(self, model: Generator[str, str]):
        self.model = model
        self.parser = DetailParser()

    def generate(self, meaning: Meaning) -> Detail:
        prompt: str = self.PROMPT.format(**asdict(meaning))
        response: str = self.model.generate(prompt)
        detail: Detail = self.parser.parse(response)
        detail.meaning_id = meaning.id
        return detail
