from pathlib import Path
from unittest import TestCase
from synogym.meaning import Detail, Example, Meaning
from synogym.sqlite_repo import SqliteRepo

class SqliteRepoTest(TestCase):
    def setUp(self):
        self.schema_sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")

    def test_meaning_operations(self):
        repo = SqliteRepo(":memory:", self.schema_sql_path)
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        repo.create_meaning(Meaning(query="sad", definition="unhappy", pos="adjective"))
        self.assertEqual([meaning], repo.list_meanings_by_query("happy"))
        self.assertEqual(meaning, repo.read_meaning(meaning.id))

    def test_detail_operations(self):
        repo = SqliteRepo(":memory:", self.schema_sql_path)
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        self.assertEqual(detail, repo.create_detail(detail))
        self.assertEqual(detail, repo.read_detail(detail.id))

    def create_detail(self, detail_id: int | None) -> Detail:
        example = Example(sentence="She is happy.", replacements=["glad", "cheerful"])
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=["glad"],
                      history="Old English.", formations=["happiness"], examples=[example])
