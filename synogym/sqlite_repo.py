import json
import sqlite3
from sqlite3 import Row
from pathlib import Path
from synogym.meaning import Detail, Example, Meaning
from synogym.repo import Repo

class SqliteRepo(Repo):
    LIST_MEANINGS_SQL = "SELECT * FROM meanings WHERE query = ? ORDER BY id"
    READ_MEANING_SQL = "SELECT * FROM meanings WHERE id = ?"
    READ_DETAIL_SQL = "SELECT * FROM detailed_meanings WHERE meaning_id = ?"
    LIST_EXAMPLES_SQL = "SELECT * FROM examples WHERE meaning_id = ? ORDER BY id"
    INSERT_MEANING_SQL = "INSERT INTO meanings (query, definition, pos) VALUES (?, ?, ?)"
    INSERT_DETAIL_SQL = "INSERT INTO detailed_meanings (meaning_id, level, description, synonyms, history, formations) " \
                        "VALUES (?, ?, ?, ?, ?, ?)"
    INSERT_EXAMPLE_SQL = "INSERT INTO examples (meaning_id, sentence, replacements) VALUES (?, ?, ?)"

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

    def create_meaning(self, meaning: Meaning) -> Meaning:
        meaning_values: tuple = (meaning.query, meaning.definition, meaning.pos)
        cursor = self.connection.execute(self.INSERT_MEANING_SQL, meaning_values)
        self.connection.commit()
        meaning.id = cursor.lastrowid
        return meaning

    def read_meaning(self, meaning_id: int | None) -> Meaning:
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

    def read_detail(self, detail_id: int | None) -> Detail:
        cursor = self.connection.execute(self.READ_DETAIL_SQL, (detail_id,))
        row = cursor.fetchone()
        if not row: raise ValueError("Detail not found")
        detail: Detail = self._get_detail(row)
        detail.examples = self._list_examples(row["meaning_id"])
        return detail

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
