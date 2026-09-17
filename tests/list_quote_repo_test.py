from unittest import TestCase
from synogym.data_classes import Quote
from synogym.list_quote_repo import ListQuoteRepo

class ListQuoteRepoTest(TestCase):
    def test_lists_quotes_by_query(self):
        repo = ListQuoteRepo()
        quote = repo.create_all([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        repo.create_all([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], repo.list_by_query("happy"))
