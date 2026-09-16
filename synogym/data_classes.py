from dataclasses import dataclass, field

@dataclass
class Example:
    id: int | None = field(default=None, kw_only=True)
    sentence: str
    replacements: list[str]

@dataclass
class Meaning:
    id: int | None = field(default=None, kw_only=True)
    query: str
    definition: str
    pos: str

@dataclass
class Detail:
    id: int | None = field(default=None, kw_only=True)
    level: str
    description: str
    synonyms: list[str]
    history: str
    formations: list[str]
    examples: list[Example]

@dataclass
class MeaningWithDetail(Meaning):
    detail: Detail
