import random
from synogym.data_classes import Quote
from synogym.generator import Generator
from synogym.repo.interface import QuoteRepo

class QuoteService:
    def __init__(self, repo: QuoteRepo, quote_generator: Generator[str, list[Quote]] | None):
        self.repo = repo
        self.generator = quote_generator
        self.quote_limit = 5
        self.quote_text_limit = 200

    def list_by_query(self, query: str) -> list[Quote]:
        quotes = self._filter(self.repo.list_by_query(query))
        if len(quotes) < self.quote_limit and self.generator is not None:
            quotes = self._filter(self.repo.create_all(self.generator.generate(query)))
        return random.sample(quotes, min(len(quotes), self.quote_limit))

    def _filter(self, quotes: list[Quote]) -> list[Quote]:
        return [quote for quote in quotes if len(quote.text) < self.quote_text_limit]
