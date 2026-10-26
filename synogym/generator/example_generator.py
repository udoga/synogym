from dataclasses import asdict
from synogym.generator import Generator
from synogym.parser import ExampleParser
from synogym.data_classes import Example, LlmRequest, Meaning

class ExampleGenerator(Generator[Meaning, list[Example]]):
    PROMPT = """You are a dictionary API for English learners.
Given a word or phrase, its selected definition and pos; return only YAML in the structure below.

examples:
  - sentence: A clear and common usage example.
    replacements: comma separated best alternatives for the word in this context

Rules:
- 3 versatile examples.
- 2 replacements each with 1 or 2 words.
- ONLY content, no markdown, no additional text, no quotation marks.

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
