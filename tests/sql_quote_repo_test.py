from pathlib import Path
from unittest import TestCase
from synogym.repo.sql_quote_repo import SqlQuoteRepo
from synogym.sqlite_connector import SqliteConnector
from synogym.data_classes import Quote

class SqlMeaningRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")
        self.connection = SqliteConnector().connect(":memory:", self.sql_path)
        self.repo = SqlQuoteRepo(self.connection)

    def test_quote_operations(self):
        quote = self.repo.create_all([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        self.repo.create_all([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], self.repo.list_by_query("happy"))
