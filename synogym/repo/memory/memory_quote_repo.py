import re
from synogym.repo.interface import QuoteRepo
from synogym.data_classes import Quote

class MemoryQuoteRepo(QuoteRepo):
    def __init__(self):
        self.quotes: list[Quote] = []

    def list_by_inflections(self, inflections: list[str]) -> list[Quote]:
        return [quote for quote in self.quotes if self._has_inflection(quote, inflections)]

    def _has_inflection(self, quote: Quote, inflections: list[str]) -> bool:
        return any(self._has_word(quote, inflection) for inflection in inflections)

    def _has_word(self, quote: Quote, inflection: str) -> bool:
        word: str = re.escape(inflection)
        pattern: str = rf"(?<![A-Za-z0-9]){word}(?![A-Za-z0-9])"
        return re.search(pattern, quote.text, re.IGNORECASE) is not None

    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            quote.id = len(self.quotes) + 1
            self.quotes.append(quote)
        return quotes
