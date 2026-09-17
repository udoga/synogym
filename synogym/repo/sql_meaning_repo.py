import json
import sqlite3
from sqlite3 import Row
from synogym.data_classes import Detail, Example, Meaning
from synogym.repo.meaning_repo import MeaningRepo

class SqlMeaningRepo(MeaningRepo):
    LIST_MEANINGS_SQL = "SELECT * FROM meanings WHERE query = ? ORDER BY id"
    READ_MEANING_SQL = "SELECT * FROM meanings WHERE id = ?"
    READ_DETAIL_SQL = "SELECT * FROM meaning_details WHERE meaning_id = ?"
    LIST_EXAMPLES_SQL = "SELECT * FROM examples WHERE meaning_id = ? ORDER BY id"
    INSERT_MEANING_SQL = "INSERT INTO meanings (query, definition, pos) VALUES (?, ?, ?)"
    INSERT_DETAIL_SQL = "INSERT INTO meaning_details (meaning_id, level, description, synonyms, history, formations) " \
                        "VALUES (?, ?, ?, ?, ?, ?)"
    INSERT_EXAMPLE_SQL = "INSERT INTO examples (meaning_id, sentence, replacements) VALUES (?, ?, ?)"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Meaning]:
        cursor = self.connection.execute(self.LIST_MEANINGS_SQL, (query,))
        return [self._get_meaning(row) for row in cursor.fetchall()]

    def create_all(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            values: tuple = (meaning.query, meaning.definition, meaning.pos)
            cursor = self.connection.execute(self.INSERT_MEANING_SQL, values)
            meaning.id = cursor.lastrowid
        self.connection.commit()
        return meanings

    def find(self, meaning_id: int) -> Meaning | None:
        cursor = self.connection.execute(self.READ_MEANING_SQL, (meaning_id,))
        row = cursor.fetchone()
        return self._get_meaning(row) if row else None

    def create_detail(self, d: Detail) -> Detail:
        values = (d.meaning_id, d.level, d.description, json.dumps(d.synonyms), d.history, json.dumps(d.formations))
        self.connection.execute(self.INSERT_DETAIL_SQL, values)
        for example in d.examples:
            self._create_example(d.meaning_id, example)
        self.connection.commit()
        return d

    def find_detail(self, detail_id: int) -> Detail | None:
        cursor = self.connection.execute(self.READ_DETAIL_SQL, (detail_id,))
        row = cursor.fetchone()
        if not row: return None
        detail: Detail = self._get_detail(row)
        detail.examples = self._list_examples(row["meaning_id"])
        return detail

    def _create_example(self, detail_id: int | None, example: Example) -> Example:
        values: tuple = (detail_id, example.sentence, json.dumps(example.replacements))
        cursor = self.connection.execute(self.INSERT_EXAMPLE_SQL, values)
        example.meaning_id = cursor.lastrowid
        return example

    def _list_examples(self, detail_id: int) -> list[Example]:
        cursor = self.connection.execute(self.LIST_EXAMPLES_SQL, (detail_id,))
        return [self._get_example(row) for row in cursor.fetchall()]

    def _get_detail(self, row: Row) -> Detail:
        return Detail(meaning_id=row["meaning_id"], level=row["level"], description=row["description"],
                      synonyms=json.loads(row["synonyms"]), history=row["history"],
                      formations=json.loads(row["formations"]), examples=[])

    def _get_meaning(self, row: Row) -> Meaning:
        return Meaning(id=row["id"], query=row["query"], definition=row["definition"], pos=row["pos"])

    def _get_example(self, row: Row) -> Example:
        return Example(meaning_id=row["id"], sentence=row["sentence"], replacements=json.loads(row["replacements"]))
