from unittest import TestCase
from synogym.data_classes import Quote
from synogym.repo.list.list_quote_repo import ListQuoteRepo
from synogym.generator.mock_generator import MockGenerator
from synogym.service.quote_service import QuoteService

class QuoteServiceTest(TestCase):
    def setUp(self):
        self.repo = ListQuoteRepo()
        self.brainy_client = MockGenerator[str, list[Quote]]([])
        self.service = QuoteService(self.repo, self.brainy_client)

    def test_fetches_and_saves_quotes_when_repo_is_empty(self):
        self.brainy_client.output = [Quote(text="Be yourself", author="Oscar Wilde", url="https://example.com/quote")]
        self.assertEqual(self.brainy_client.output, self.service.list_by_query("yourself"))
        self.assertEqual(self.brainy_client.output, self.repo.list_by_query("yourself"))

    def test_fetches_and_saves_quotes_when_repo_has_nine(self):
        self.repo.create_all(self.create_quotes("Be yourself", 9))
        self.brainy_client.output = self.create_quotes("Generated yourself", 10)
        self.assertEqual(self.brainy_client.output, self.service.list_by_query("yourself"))
        self.assertEqual(19, len(self.repo.quotes))

    def test_returns_quotes_from_repo_when_repo_has_ten(self):
        quotes = self.create_quotes("Be yourself", 10)
        self.repo.create_all(quotes)
        self.assertEqual(quotes, self.service.list_by_query("yourself"))

    def test_returns_ten_quotes_from_repo_when_repo_has_more(self):
        quotes = self.create_quotes("Be yourself", 11)
        self.repo.create_all(quotes)
        self.assertEqual(quotes[:10], self.service.list_by_query("yourself"))

    def test_returns_ten_quotes_from_fetcher_when_fetcher_has_more(self):
        self.brainy_client.output = self.create_quotes("Generated yourself", 11)
        self.assertEqual(self.brainy_client.output[:10], self.service.list_by_query("yourself"))

    def create_quotes(self, content: str, count: int) -> list[Quote]:
        return [Quote(text=f"{content} {number}", author="Oscar Wilde", url=f"https://example.com/{number}")
                for number in range(count)]
