import json
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Detail, Example, Meaning
from synogym.repo.interface import MeaningRepo

class SqlMeaningRepo(MeaningRepo):
    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Meaning]:
        sql = "SELECT * FROM meanings WHERE query = :query ORDER BY id"
        rows = self.connection.execute(text(sql), {"query": query}).mappings().all()
        return [self._get_meaning(row) for row in rows]

    def create_all(self, meanings: list[Meaning]) -> list[Meaning]:
        sql = """INSERT INTO meanings (query, definition, pos)
                 VALUES (:query, :definition, :pos) RETURNING id"""
        for meaning in meanings:
            meaning.id = self.connection.execute(text(sql), self._get_values(meaning)).scalar_one()
        self.connection.commit()
        return meanings

    def find(self, meaning_id: int) -> Meaning | None:
        sql = "SELECT * FROM meanings WHERE id = :id"
        row = self.connection.execute(text(sql), {"id": meaning_id}).mappings().fetchone()
        return self._get_meaning(row) if row else None

    def create_detail(self, detail: Detail) -> Detail:
        sql = """INSERT INTO meaning_details (meaning_id, level, description, synonyms, history, formations)
                 VALUES (:meaning_id, :level, :description, :synonyms, :history, :formations)"""
        self.connection.execute(text(sql), self._get_detail_values(detail))
        self.connection.commit()
        return detail

    def find_detail(self, meaning_id: int) -> Detail | None:
        sql = "SELECT * FROM meaning_details WHERE meaning_id = :meaning_id"
        row = self.connection.execute(text(sql), {"meaning_id": meaning_id}).mappings().fetchone()
        return self._get_detail(row) if row else None

    def create_examples(self, meaning_id: int, examples: list[Example]) -> list[Example]:
        for example in examples:
            self._create_example(meaning_id, example)
        self.connection.commit()
        return examples

    def list_examples(self, meaning_id: int) -> list[Example]:
        sql = "SELECT * FROM examples WHERE meaning_id = :meaning_id ORDER BY id"
        rows = self.connection.execute(text(sql), {"meaning_id": meaning_id}).mappings().all()
        return [self._get_example(row) for row in rows]

    def _create_example(self, meaning_id: int | None, example: Example) -> Example:
        sql = """INSERT INTO examples (meaning_id, sentence, replacements)
                 VALUES (:meaning_id, :sentence, :replacements)"""
        self.connection.execute(text(sql), self._get_example_values(meaning_id, example))
        example.meaning_id = meaning_id
        return example

    def _get_values(self, meaning: Meaning) -> dict[str, str]:
        return {"query": meaning.query, "definition": meaning.definition, "pos": meaning.pos}

    def _get_detail_values(self, detail: Detail) -> dict[str, int | str | None]:
        return {"meaning_id": detail.meaning_id,
                "level": detail.level,
                "description": detail.description,
                "synonyms": json.dumps(detail.synonyms),
                "history": detail.history,
                "formations": json.dumps(detail.formations)}

    def _get_example_values(self, meaning_id: int | None, example: Example) -> dict[str, int | str | None]:
        return {"meaning_id": meaning_id,
                "sentence": example.sentence,
                "replacements": json.dumps(example.replacements)}

    def _get_detail(self, row: RowMapping) -> Detail:
        return Detail(meaning_id=row["meaning_id"],
                      level=row["level"],
                      description=row["description"],
                      synonyms=json.loads(row["synonyms"]),
                      history=row["history"],
                      formations=json.loads(row["formations"]))

    def _get_meaning(self, row: RowMapping) -> Meaning:
        return Meaning(id=row["id"], query=row["query"], definition=row["definition"], pos=row["pos"])

    def _get_example(self, row: RowMapping) -> Example:
        return Example(meaning_id=row["meaning_id"],
                       sentence=row["sentence"],
                       replacements=json.loads(row["replacements"]))
