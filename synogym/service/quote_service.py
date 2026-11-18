import random
from dataclasses import replace
from synogym.data_classes import Quote
from synogym.highlighter import Highlighter
from synogym.repo.interface import QuoteRepo
from synogym.usage_checker import UsageChecker

class QuoteService:
    def __init__(self, repo: QuoteRepo, usage_checker: UsageChecker):
        self.repo = repo
        self.usage_checker = usage_checker
        self.highlighter = Highlighter()
        self.quote_limit = 10
        self.max_length = 300

    def list_by_query(self, query: str, pos: str) -> list[Quote]:
        inflections: list[str] = self.usage_checker.get_inflections(query, pos)
        quotes: list[Quote] = self.repo.list_by_inflections(inflections)
        filtered_quotes: list[Quote] = [q for q in quotes if self._passes_filter(q, inflections, pos)]
        highlighted_quotes = [self._highlight(q, query) for q in filtered_quotes]
        quote_count = min(len(highlighted_quotes), self.quote_limit)
        return random.sample(highlighted_quotes, quote_count)

    def _passes_filter(self, q: Quote, inflections: list[str], pos: str) -> bool:
        return len(q.text) < self.max_length and self.usage_checker.is_usage_example(q.text, inflections, pos)

    def _highlight(self, quote: Quote, query: str) -> Quote:
        text: str = self.highlighter.highlight(quote.text, query)
        return replace(quote, text=text)
