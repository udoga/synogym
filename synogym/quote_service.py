from synogym.data_classes import Quote
from synogym.generator import Generator
from synogym.repo import Repo

class QuoteService:
    def __init__(self, repo: Repo, quote_generator: Generator[str, list[Quote]]):
        self.repo = repo
        self.quote_generator = quote_generator

    def list_quotes_by_query(self, query: str) -> list[Quote]:
        quotes = self.repo.list_quotes_by_query(query)
        return quotes if len(quotes) >= 10 else self.repo.create_quotes(self.quote_generator.generate(query))
