import re
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Quote
from synogym.repo.quote_repo import QuoteRepo

class SqlQuoteRepo(QuoteRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Quote]:
        sql = "SELECT * FROM quotes WHERE LOWER(text) LIKE :query ORDER BY id"
        rows = self.connection.execute(text(sql), {"query": f"%{query.lower()}%"}).mappings().all()
        quotes = [self._get_quote(row) for row in rows]
        return [quote for quote in quotes if self._has_query_word(quote, query)]

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

    def _has_query_word(self, quote: Quote, query: str) -> bool:
        query_word = re.escape(query)
        pattern = rf"(?<![A-Za-z0-9]){query_word}(?![A-Za-z0-9])"
        return re.search(pattern, quote.text, re.IGNORECASE) is not None
