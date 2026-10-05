from pathlib import Path
from unittest import TestCase
from synogym.repo.db.sql_quote_repo import SqlQuoteRepo
from synogym.db_connector import DbConnector
from synogym.data_classes import Quote

class SqlMeaningRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "schema-sqlite.sql")
        self.connection = DbConnector().connect({"type": "sqlite", "uri": ":memory:", "sql_paths": [self.sql_path]})
        self.repo = SqlQuoteRepo(self.connection)

    def test_quote_operations(self):
        quote = self.repo.create_all([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        self.repo.create_all([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], self.repo.list_by_query("happy"))

    def test_create_all_ignores_duplicate_quotes(self):
        quote = Quote(text="Be happy.", author="Unknown", url="https://example.com")
        duplicate = Quote(text="Be happy.", author="Unknown", url="https://example.com")
        self.repo.create_all([quote])
        self.repo.create_all([duplicate])
        self.assertEqual([quote], self.repo.list_by_query("happy"))
