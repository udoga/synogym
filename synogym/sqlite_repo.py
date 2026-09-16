import json
import sqlite3
from sqlite3 import Row
from pathlib import Path
from synogym.data_classes import Detail, Example, Meaning, Quote
from synogym.repo import Repo

class SqliteRepo(Repo):
    LIST_MEANINGS_SQL = "SELECT * FROM meanings WHERE query = ? ORDER BY id"
    READ_MEANING_SQL = "SELECT * FROM meanings WHERE id = ?"
    READ_DETAIL_SQL = "SELECT * FROM meaning_details WHERE meaning_id = ?"
    LIST_EXAMPLES_SQL = "SELECT * FROM examples WHERE meaning_id = ? ORDER BY id"
    LIST_QUOTES_SQL = "SELECT * FROM quotes WHERE LOWER(text) LIKE ? ORDER BY id"
    INSERT_MEANING_SQL = "INSERT INTO meanings (query, definition, pos) VALUES (?, ?, ?)"
    INSERT_DETAIL_SQL = "INSERT INTO meaning_details (meaning_id, level, description, synonyms, history, formations) " \
                        "VALUES (?, ?, ?, ?, ?, ?)"
    INSERT_EXAMPLE_SQL = "INSERT INTO examples (meaning_id, sentence, replacements) VALUES (?, ?, ?)"
    INSERT_QUOTE_SQL = "INSERT INTO quotes (text, author, url) VALUES (?, ?, ?)"

    def __init__(self, database_path: str, schema_sql_path: str):
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.connection.row_factory = Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(Path(schema_sql_path).read_text())
        self.connection.commit()

    def __del__(self):
        if hasattr(self, "connection"):
            self.connection.close()

    def list_meanings_by_query(self, query: str) -> list[Meaning]:
        cursor = self.connection.execute(self.LIST_MEANINGS_SQL, (query,))
        return [self._get_meaning(row) for row in cursor.fetchall()]

    def create_meanings(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            meaning_values: tuple = (meaning.query, meaning.definition, meaning.pos)
            cursor = self.connection.execute(self.INSERT_MEANING_SQL, meaning_values)
            meaning.id = cursor.lastrowid
        self.connection.commit()
        return meanings

    def read_meaning(self, meaning_id: int) -> Meaning:
        cursor = self.connection.execute(self.READ_MEANING_SQL, (meaning_id,))
        row = cursor.fetchone()
        if not row: raise ValueError("Meaning not found")
        return self._get_meaning(row)

    def create_detail(self, d: Detail) -> Detail:
        self.read_meaning(d.id)
        detail_values = (d.id, d.level, d.description, json.dumps(d.synonyms), d.history, json.dumps(d.formations))
        self.connection.execute(self.INSERT_DETAIL_SQL, detail_values)
        for example in d.examples:
            self._create_example(d.id, example)
        self.connection.commit()
        return d

    def read_detail(self, detail_id: int) -> Detail:
        cursor = self.connection.execute(self.READ_DETAIL_SQL, (detail_id,))
        row = cursor.fetchone()
        if not row: raise ValueError("Detail not found")
        detail: Detail = self._get_detail(row)
        detail.examples = self._list_examples(row["meaning_id"])
        return detail

    def list_quotes_by_query(self, query: str) -> list[Quote]:
        cursor = self.connection.execute(self.LIST_QUOTES_SQL, (f"%{query.lower()}%",))
        return [self._get_quote(row) for row in cursor.fetchall()]

    def create_quotes(self, quotes: list[Quote]) -> list[Quote]:
        for quote in quotes:
            quote_values: tuple = (quote.text, quote.author, quote.url)
            cursor = self.connection.execute(self.INSERT_QUOTE_SQL, quote_values)
            quote.id = cursor.lastrowid
        self.connection.commit()
        return quotes

    def _create_example(self, detail_id: int | None, example: Example) -> Example:
        example_values: tuple = (detail_id, example.sentence, json.dumps(example.replacements))
        cursor = self.connection.execute(self.INSERT_EXAMPLE_SQL, example_values)
        example.id = cursor.lastrowid
        return example

    def _list_examples(self, detail_id: int) -> list[Example]:
        cursor = self.connection.execute(self.LIST_EXAMPLES_SQL, (detail_id,))
        return [self._get_example(row) for row in cursor.fetchall()]

    def _get_detail(self, row: Row) -> Detail:
        return Detail(id=row["meaning_id"], level=row["level"], description=row["description"],
                      synonyms=json.loads(row["synonyms"]), history=row["history"],
                      formations=json.loads(row["formations"]), examples=[])

    def _get_meaning(self, row: Row) -> Meaning:
        return Meaning(id=row["id"], query=row["query"], definition=row["definition"], pos=row["pos"])

    def _get_example(self, row: Row) -> Example:
        return Example(id=row["id"], sentence=row["sentence"], replacements=json.loads(row["replacements"]))

    def _get_quote(self, row: Row) -> Quote:
        return Quote(id=row["id"], text=row["text"], author=row["author"], url=row["url"])
