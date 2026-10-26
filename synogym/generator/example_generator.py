from dataclasses import asdict
from synogym.generator import Generator
from synogym.parser import ExampleParser
from synogym.data_classes import Example, LlmRequest, Meaning

class ExampleGenerator(Generator[Meaning, list[Example]]):
    PROMPT = """You are a dictionary API for English learners.
Given a word or phrase, its definition and its pos; return a YAML in the structure below.

examples:
  - sentence: a clear and common usage example
    replacements: 2 best alternatives for the word in this context, each 1-2 words

Rules:
- Exactly 3 versatile examples.
- Only YAML, no markdown, no additional text, no quotation marks.

Query: {query}
Definition: {definition}
Part of speech: {pos}
"""

    def __init__(self, generator: Generator[LlmRequest, str]):
        self.generator: Generator[LlmRequest, str] = generator
        self.parser = ExampleParser()

    def generate(self, meaning: Meaning) -> list[Example]:
        prompt: str = self.PROMPT.format(**asdict(meaning))
        text: str = self.generator.generate(LlmRequest(prompt, "examples"))
        examples: list[Example] = self.parser.parse(text)
        for example in examples:
            example.meaning_id = meaning.id
        return examples
