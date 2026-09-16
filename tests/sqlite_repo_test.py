from pathlib import Path
from unittest import TestCase
from synogym.data_classes import Detail, Example, Meaning, Quote
from synogym.sqlite_repo import SqliteRepo

class SqliteRepoTest(TestCase):
    def setUp(self):
        self.schema_sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")

    def test_meaning_operations(self):
        repo = SqliteRepo(":memory:", self.schema_sql_path)
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        repo.create_meanings([Meaning(query="sad", definition="unhappy", pos="adjective")])
        self.assertEqual([meaning], repo.list_meanings_by_query("happy"))
        self.assertEqual(meaning, repo.read_meaning(meaning.id))

    def test_detail_operations(self):
        repo = SqliteRepo(":memory:", self.schema_sql_path)
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        self.assertEqual(detail, repo.create_detail(detail))
        self.assertEqual(detail, repo.read_detail(detail.id))

    def test_quote_operations(self):
        repo = SqliteRepo(":memory:", self.schema_sql_path)
        quote = repo.create_quotes([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        repo.create_quotes([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], repo.list_quotes_by_query("happy"))

    def create_detail(self, detail_id: int | None) -> Detail:
        example = Example(sentence="She is happy.", replacements=["glad", "cheerful"])
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=["glad"],
                      history="Old English.", formations=["happiness"], examples=[example])
