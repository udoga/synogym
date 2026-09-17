from dataclasses import dataclass, field

@dataclass
class User:
    id: int | None = field(default=None, kw_only=True)
    email: str
    first_name: str
    last_name: str

@dataclass
class Meaning:
    id: int | None = field(default=None, kw_only=True)
    query: str
    definition: str
    pos: str

@dataclass
class Example:
    meaning_id: int | None = field(default=None, kw_only=True)
    sentence: str
    replacements: list[str]

@dataclass
class Detail:
    meaning_id: int | None = field(default=None, kw_only=True)
    level: str
    description: str
    synonyms: list[str]
    history: str
    formations: list[str]
    examples: list[Example]

@dataclass
class Quote:
    id: int | None = field(default=None, kw_only=True)
    text: str
    author: str
    url: str

@dataclass
class MeaningWithDetail(Meaning):
    detail: Detail
