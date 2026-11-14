import random
from dataclasses import replace
from synogym.data_classes import Quote
from synogym.highlighter import Highlighter
from synogym.repo.interface import QuoteRepo

class QuoteService:
    def __init__(self, repo: QuoteRepo):
        self.repo = repo
        self.highlighter = Highlighter()
        self.quote_limit = 5
        self.quote_text_limit = 200

    def list_by_query(self, query: str) -> list[Quote]:
        quotes = self._filter(self.repo.list_by_query(query))
        quotes = [self._highlight(q, query) for q in quotes]
        return random.sample(quotes, min(len(quotes), self.quote_limit))

    def _highlight(self, quote: Quote, query: str) -> Quote:
        text: str = self.highlighter.highlight(quote.text, query)
        return replace(quote, text=text)

    def _filter(self, quotes: list[Quote]) -> list[Quote]:
        return [quote for quote in quotes if len(quote.text) < self.quote_text_limit]
