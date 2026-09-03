from dataclasses import asdict, replace
from synogym.generator import Generator
from synogym.detail_parser import DetailParser
from synogym.gpt_model import GptModel
from synogym.meaning import Detail, Meaning
from synogym.meaning_parser import MeaningParser

class ModelGenerator(Generator):
    MEANING_PROMPT = """You are a dictionary API for English learners.
Given a queried English word or phrase, return a YAML in the structure below.

meanings:
- definition: Very short and concise, ideally 3-6 words.
  pos: noun | verb | adjective | adverb | preposition | conjunction | interjection | determiner | article

Rules:
- Only YAML, no markdown or additional text, no quotation marks.
- If the query is meaningless in English, or if there is a typo, return meanings: []

Query: {query}
"""

    DETAIL_PROMPT = """You are a dictionary API for English learners.
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

    def __init__(self):
        self.model = GptModel(model="gpt-5", reasoning_effort="minimal")
        self.meaning_parser = MeaningParser()
        self.detail_parser = DetailParser()

    def generate_meanings(self, query: str) -> list[Meaning]:
        prompt: str = self.MEANING_PROMPT.format(query=query)
        response: str = self.model.respond(prompt)
        meanings: list[Meaning] = self.meaning_parser.parse(response)
        return [replace(meaning, query=query) for meaning in meanings]

    def generate_detail(self, meaning: Meaning) -> Detail:
        prompt: str = self.DETAIL_PROMPT.format(**asdict(meaning))
        response: str = self.model.respond(prompt)
        detail: Detail = self.detail_parser.parse(response)
        return detail
