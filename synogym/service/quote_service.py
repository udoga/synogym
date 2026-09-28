from synogym.data_classes import Quote
from synogym.generator.generator import Generator
from synogym.repo.quote_repo import QuoteRepo

class QuoteService:
    def __init__(self, repo: QuoteRepo, quote_generator: Generator[str, list[Quote]]):
        self.repo = repo
        self.generator = quote_generator
        self.quote_limit = 10

    def list_by_query(self, query: str) -> list[Quote]:
        quotes = self.repo.list_by_query(query)
        if len(quotes) < self.quote_limit:
            quotes = self.repo.create_all(self.generator.generate(query))
        return quotes[:self.quote_limit]
