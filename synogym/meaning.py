from dataclasses import dataclass

@dataclass
class Example:
    sentence: str
    replacements: list[str]

@dataclass
class Meaning:
    query: str
    definition: str
    pos: str

@dataclass
class DetailedMeaning(Meaning):
    level: str
    description: str
    synonyms: list[str]
    history: str
    related: list[str]

@dataclass
class FullMeaning(DetailedMeaning):
    examples: list[Example]
