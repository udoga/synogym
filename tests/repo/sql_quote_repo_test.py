from unittest import TestCase
from synogym.repo.sqlalchemy.sql_quote_repo import SqlQuoteRepo
from synogym.db_connector import DbConnector
from synogym.data_classes import Quote

class SqlMeaningRepoTest(TestCase):
    def setUp(self):
        self.connection = DbConnector().connect_test()
        self.repo = SqlQuoteRepo(self.connection)

    def test_creates_and_lists(self):
        quote = self.repo.create_all([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        self.repo.create_all([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], self.repo.list_by_query("happy"))

    def test_ignores_duplicates_when_creates_all(self):
        quote = Quote(text="Be happy.", author="Unknown", url="https://example.com")
        duplicate = Quote(text="Be happy.", author="Unknown", url="https://example.com")
        self.repo.create_all([quote])
        self.repo.create_all([duplicate])
        self.assertEqual([quote], self.repo.list_by_query("happy"))

    def test_list_by_query_matches_whole_words_only(self):
        quote = self.repo.create_all([Quote(text="A cat sleeps.", author="Unknown", url="https://example.com/cat")])[0]
        self.repo.create_all([Quote(text="A catch is different.", author="Unknown", url="https://example.com/catch")])
        self.assertEqual([quote], self.repo.list_by_query("cat"))
