from synogym.repo import Repo
from synogym.data_classes import Detail, Meaning, Quote

class MemoryRepo(Repo):
    def __init__(self):
        self.meanings: list[Meaning] = []
        self.details: list[Detail] = []
        self.quotes: list[Quote] = []

    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        return [meaning for meaning in self.meanings if meaning.query == query]

    def create_meanings(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            meaning.id = len(self.meanings) + 1
            self.meanings.append(meaning)
        return meanings

    def find_meaning(self, meaning_id: int) -> Meaning | None:
        for meaning in self.meanings:
            if meaning.id == meaning_id:
                return meaning
        return None

    def create_detail(self, detail: Detail) -> Detail:
        if not self.find_meaning(detail.meaning_id):
            raise ValueError("Meaning not found")
        if any(d.meaning_id == detail.meaning_id for d in self.details):
            raise ValueError("Detail already exists")
        self.details.append(detail)
        return detail

    def find_detail(self, detail_id: int) -> Detail | None:
        for detail in self.details:
            if detail.meaning_id == detail_id:
                return detail
        return None

    def list_quotes_by_query(self, query: str) -> list[Quote]:
        return [quote for quote in self.quotes if query.lower() in quote.text.lower()]

    def create_quotes(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            quote.id = len(self.quotes) + 1
            self.quotes.append(quote)
        return quotes
