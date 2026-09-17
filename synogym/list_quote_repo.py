from synogym.quote_repo import QuoteRepo
from synogym.data_classes import Quote

class ListQuoteRepo(QuoteRepo):
    def __init__(self):
        self.quotes: list[Quote] = []

    def list_by_query(self, query: str) -> list[Quote]:
        return [quote for quote in self.quotes if query.lower() in quote.text.lower()]

    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            quote.id = len(self.quotes) + 1
            self.quotes.append(quote)
        return quotes
