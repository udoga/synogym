import re
from sqlalchemy import text, Sequence
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Quote
from synogym.repo.interface import QuoteRepo

class SqlQuoteRepo(QuoteRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by_inflections(self, inflections: list[str]) -> list[Quote]:
        if not inflections: return []
        conditions: list[str] = [f"LOWER(text) LIKE :inflection_{i}" for i in range(len(inflections))]
        parameters: dict[str, str] = {f"inflection_{i}": f"%{s.lower()}%" for i, s in enumerate(inflections)}
        sql = f"SELECT * FROM quotes WHERE {' OR '.join(conditions)} ORDER BY id"
        rows: Sequence[RowMapping] = self.connection.execute(text(sql), parameters).mappings().all()
        quotes: list[Quote] = [self._get_quote(row) for row in rows]
        return [quote for quote in quotes if self._has_one_of(quote, inflections)]

    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            self._create(quote)
        self.connection.commit()
        return quotes

    def _create(self, quote: Quote) -> Quote:
        sql = """INSERT INTO quotes (text, author, url)
                 VALUES (:text, :author, :url)
                 ON CONFLICT (text, author, url) DO UPDATE SET text = excluded.text RETURNING id"""
        quote.id = self.connection.execute(text(sql), self._get_values(quote)).scalar_one()
        return quote

    def _get_values(self, quote: Quote) -> dict[str, str]:
        return {"text": quote.text, "author": quote.author, "url": quote.url}

    def _get_quote(self, row: RowMapping) -> Quote:
        return Quote(id=row["id"], text=row["text"], author=row["author"], url=row["url"])

    def _has_one_of(self, quote: Quote, inflections: list[str]) -> bool:
        return any(self._has_word(quote, inflection) for inflection in inflections)

    def _has_word(self, quote: Quote, word: str) -> bool:
        word: str = re.escape(word)
        pattern: str = rf"(?<![A-Za-z0-9]){word}(?![A-Za-z0-9])"
        return re.search(pattern, quote.text, re.IGNORECASE) is not None
