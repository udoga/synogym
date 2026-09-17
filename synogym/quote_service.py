from synogym.data_classes import Quote
from synogym.generator import Generator
from synogym.quote_repo import QuoteRepo

class QuoteService:
    def __init__(self, repo: QuoteRepo, quote_generator: Generator[str, list[Quote]]):
        self.repo = repo
        self.generator = quote_generator

    def list_by_query(self, query: str) -> list[Quote]:
        quotes = self.repo.list_by_query(query)
        return quotes if len(quotes) >= 10 else self.repo.create_all(self.generator.generate(query))
