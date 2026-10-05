from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Quote
from synogym.repo.quote_repo import QuoteRepo

class SqlQuoteRepo(QuoteRepo):
    LIST_QUOTES_SQL = "SELECT * FROM quotes WHERE LOWER(text) LIKE :query ORDER BY id"
    INSERT_QUOTE_SQL = """
        INSERT INTO quotes (text, author, url)
        VALUES (:text, :author, :url)
        RETURNING id
    """
    FIND_QUOTE_SQL = "SELECT * FROM quotes WHERE text = :text AND author = :author AND url = :url"

    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Quote]:
        rows = self.connection.execute(text(self.LIST_QUOTES_SQL), {"query": f"%{query.lower()}%"}).mappings().all()
        return [self._get_quote(row) for row in rows]

    def create_all(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            self._create(quote)
        self.connection.commit()
        return quotes

    def _create(self, quote: Quote) -> Quote:
        values = self._get_values(quote)
        existing_quote = self._find(values)
        quote.id = existing_quote.id if existing_quote else self._insert(values)
        return quote

    def _insert(self, values: dict[str, str]) -> int:
        return self.connection.execute(text(self.INSERT_QUOTE_SQL), values).scalar_one()

    def _find(self, values: dict[str, str]) -> Quote | None:
        row = self.connection.execute(text(self.FIND_QUOTE_SQL), values).mappings().fetchone()
        return self._get_quote(row) if row else None

    def _get_values(self, quote: Quote) -> dict[str, str]:
        return {"text": quote.text, "author": quote.author, "url": quote.url}

    def _get_quote(self, row: RowMapping) -> Quote:
        return Quote(id=row["id"], text=row["text"], author=row["author"], url=row["url"])
