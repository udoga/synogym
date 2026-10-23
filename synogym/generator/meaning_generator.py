from dataclasses import replace
from synogym.generator import Generator
from synogym.data_classes import Meaning, LlmRequest
from synogym.parser import MeaningParser

class MeaningGenerator(Generator[str, list[Meaning]]):
    PROMPT = """You are a dictionary API for English learners.
Given a queried English word or phrase, return a YAML in the structure below.

meanings:
- definition: Very short and concise, ideally 3-6 words.
  pos: noun | verb | adjective | adverb | preposition | conjunction | interjection | determiner | article

Rules:
- Only YAML, no markdown or additional text, no quotation marks.
- If the query is meaningless in English, or if there is a typo, return meanings: []

Query: {query}
"""

    def __init__(self, generator: Generator[LlmRequest, str]):
        self.generator: Generator[LlmRequest, str] = generator
        self.parser = MeaningParser()

    def generate(self, query: str) -> list[Meaning]:
        prompt: str = self.PROMPT.format(query=query)
        response: str = self.generator.generate(LlmRequest(prompt, "meanings"))
        meanings: list[Meaning] = self.parser.parse(response)
        return [replace(meaning, query=query) for meaning in meanings]
