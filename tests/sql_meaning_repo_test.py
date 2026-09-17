from pathlib import Path
from unittest import TestCase
from synogym.sqlite_connector import SqliteConnector
from synogym.data_classes import Detail, Example, Meaning
from synogym.repo.sql_meaning_repo import SqlMeaningRepo

class SqlMeaningRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")
        self.connection = SqliteConnector().connect(":memory:", self.sql_path)
        self.repo = SqlMeaningRepo(self.connection)

    def test_meaning_operations(self):
        meaning = self.repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        self.repo.create_all([Meaning(query="sad", definition="unhappy", pos="adjective")])
        self.assertEqual([meaning], self.repo.list_by_query("happy"))
        self.assertEqual(meaning, self.repo.find(meaning.id))

    def test_detail_operations(self):
        meaning = self.repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        self.assertEqual(detail, self.repo.create_detail(detail))
        self.assertEqual(detail, self.repo.find_detail(detail.meaning_id))
        self.assertIsNone(self.repo.find_detail(123))

    def create_detail(self, detail_id: int | None) -> Detail:
        example = Example(sentence="She is happy.", replacements=["glad", "cheerful"])
        return Detail(meaning_id=detail_id, level="A1", description="Feeling joy.", synonyms=["glad"],
                      history="Old English.", formations=["happiness"], examples=[example])
