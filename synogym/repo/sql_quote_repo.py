import sqlite3
from sqlite3 import Row
from synogym.data_classes import Quote
from synogym.repo.quote_repo import QuoteRepo

class SqlQuoteRepo(QuoteRepo):
    LIST_QUOTES_SQL = "SELECT * FROM quotes WHERE LOWER(text) LIKE ? ORDER BY id"
    INSERT_QUOTE_SQL = "INSERT INTO quotes (text, author, url) VALUES (?, ?, ?)"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Quote]:
        cursor = self.connection.execute(self.LIST_QUOTES_SQL, (f"%{query.lower()}%",))
        return [self._get_quote(row) for row in cursor.fetchall()]

    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            values: tuple = (quote.text, quote.author, quote.url)
            cursor = self.connection.execute(self.INSERT_QUOTE_SQL, values)
            quote.id = cursor.lastrowid
        self.connection.commit()
        return quotes

    def _get_quote(self, row: Row) -> Quote:
        return Quote(id=row["id"], text=row["text"], author=row["author"], url=row["url"])
