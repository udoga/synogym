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
class MeaningWithDetail(Meaning):
    detail: Detail

@dataclass
class Bookmark:
    id: int | None = field(default=None, kw_only=True)
    user_id: int
    meaning_id: int
    note: str
    tags: str

@dataclass
class BookmarkWithMeaning(Bookmark):
    meaning: Meaning

@dataclass
class Quote:
    id: int | None = field(default=None, kw_only=True)
    text: str
    author: str
    url: str

@dataclass
class LlmRequest:
    text: str
    operation: str

@dataclass
class LlmResponse:
    text: str
    input_token_count: int
    output_token_count: int
    first_token_latency: float
    generation_latency: float

@dataclass
class LlmCall:
    id: int | None = field(default=None, kw_only=True)
    llm_name: str
    reasoning_effort: str
    operation: str
    input_token_count: int
    output_token_count: int
    first_token_latency: float
    generation_latency: float
