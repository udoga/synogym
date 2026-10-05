import json
from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import Detail, Example, Meaning
from synogym.repo.meaning_repo import MeaningRepo

class SqlMeaningRepo(MeaningRepo):
    LIST_MEANINGS_SQL = "SELECT * FROM meanings WHERE query = :query ORDER BY id"
    READ_MEANING_SQL = "SELECT * FROM meanings WHERE id = :id"
    READ_DETAIL_SQL = "SELECT * FROM meaning_details WHERE meaning_id = :meaning_id"
    LIST_EXAMPLES_SQL = "SELECT * FROM examples WHERE meaning_id = :meaning_id ORDER BY id"
    INSERT_MEANING_SQL = """
        INSERT INTO meanings (query, definition, pos)
        VALUES (:query, :definition, :pos)
        RETURNING id
    """
    INSERT_DETAIL_SQL = """
        INSERT INTO meaning_details (meaning_id, level, description, synonyms, history, formations)
        VALUES (:meaning_id, :level, :description, :synonyms, :history, :formations)
    """
    INSERT_EXAMPLE_SQL = """
        INSERT INTO examples (meaning_id, sentence, replacements)
        VALUES (:meaning_id, :sentence, :replacements)
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def list_by_query(self, query: str) -> list[Meaning]:
        rows = self.connection.execute(text(self.LIST_MEANINGS_SQL), {"query": query}).mappings().all()
        return [self._get_meaning(row) for row in rows]

    def create_all(self, meanings: list[Meaning]) -> list[Meaning]:
        for meaning in meanings:
            meaning.id = self.connection.execute(text(self.INSERT_MEANING_SQL), self._get_values(meaning)).scalar_one()
        self.connection.commit()
        return meanings

    def find(self, meaning_id: int) -> Meaning | None:
        row = self._fetch_one(self.READ_MEANING_SQL, {"id": meaning_id})
        return self._get_meaning(row) if row else None

    def create_detail(self, detail: Detail) -> Detail:
        self.connection.execute(text(self.INSERT_DETAIL_SQL), self._get_detail_values(detail))
        for example in detail.examples:
            self._create_example(detail.meaning_id, example)
        self.connection.commit()
        return detail

    def find_detail(self, detail_id: int) -> Detail | None:
        row = self._fetch_one(self.READ_DETAIL_SQL, {"meaning_id": detail_id})
        if not row:
            return None
        detail: Detail = self._get_detail(row)
        detail.examples = self._list_examples(row["meaning_id"])
        return detail

    def _create_example(self, detail_id: int | None, example: Example) -> Example:
        self.connection.execute(text(self.INSERT_EXAMPLE_SQL), self._get_example_values(detail_id, example))
        example.meaning_id = detail_id
        return example

    def _list_examples(self, detail_id: int) -> list[Example]:
        rows = self.connection.execute(text(self.LIST_EXAMPLES_SQL), {"meaning_id": detail_id}).mappings().all()
        return [self._get_example(row) for row in rows]

    def _fetch_one(self, sql: str, values: dict) -> RowMapping | None:
        return self.connection.execute(text(sql), values).mappings().fetchone()

    def _get_values(self, meaning: Meaning) -> dict[str, str]:
        return {"query": meaning.query, "definition": meaning.definition, "pos": meaning.pos}

    def _get_detail_values(self, detail: Detail) -> dict[str, int | str | None]:
        return {"meaning_id": detail.meaning_id, "level": detail.level, "description": detail.description,
                "synonyms": json.dumps(detail.synonyms), "history": detail.history,
                "formations": json.dumps(detail.formations)}

    def _get_example_values(self, detail_id: int | None, example: Example) -> dict[str, int | str | None]:
        return {"meaning_id": detail_id, "sentence": example.sentence,
                "replacements": json.dumps(example.replacements)}

    def _get_detail(self, row: RowMapping) -> Detail:
        return Detail(meaning_id=row["meaning_id"], level=row["level"], description=row["description"],
                      synonyms=json.loads(row["synonyms"]), history=row["history"],
                      formations=json.loads(row["formations"]), examples=[])

    def _get_meaning(self, row: RowMapping) -> Meaning:
        return Meaning(id=row["id"], query=row["query"], definition=row["definition"], pos=row["pos"])

    def _get_example(self, row: RowMapping) -> Example:
        return Example(meaning_id=row["meaning_id"], sentence=row["sentence"],
                       replacements=json.loads(row["replacements"]))
