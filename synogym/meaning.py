from dataclasses import dataclass

@dataclass
class Example:
    sentence: str
    replacements: list[str]

@dataclass
class Meaning:
    query: str
    definition: str
    part_of_speech: str
    level: str
    description: str
    synonyms: list[str]
    history: str
    related: list[str]

@dataclass
class FullMeaning(Meaning):
    examples: list[Example]
