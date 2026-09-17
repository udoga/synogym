from unittest import TestCase
from synogym.data_classes import Quote
from synogym.memory_repo import MemoryRepo
from synogym.mock_generator import MockGenerator
from synogym.quote_service import QuoteService

class QuoteServiceTest(TestCase):
    def setUp(self):
        self.repo = MemoryRepo()
        self.quote_fetcher = MockGenerator[str, list[Quote]]([])
        self.service = QuoteService(self.repo, self.quote_fetcher)

    def test_returns_quotes_from_repo_when_repo_has_ten(self):
        quotes = self.create_quotes("Be yourself", 10)
        self.repo.create_quotes(quotes)
        self.assertEqual(quotes, self.service.list_quotes_by_query("yourself"))

    def test_lists_generated_quotes_when_repo_has_one(self):
        self.repo.create_quotes(self.create_quotes("Be yourself", 1))
        self.quote_fetcher.output = self.create_quotes("Generated yourself", 10)
        self.assertEqual(self.quote_fetcher.output, self.service.list_quotes_by_query("yourself"))

    def test_lists_quotes_from_generator(self):
        self.quote_fetcher.output = [Quote(text="Be yourself", author="Oscar Wilde", url="https://example.com/quote")]
        self.assertEqual(self.quote_fetcher.output, self.service.list_quotes_by_query("yourself"))
        self.assertEqual(self.quote_fetcher.output, self.repo.list_quotes_by_query("yourself"))

    def create_quotes(self, content: str, count: int) -> list[Quote]:
        return [Quote(text=f"{content} {number}", author="Oscar Wilde", url=f"https://example.com/{number}")
                for number in range(count)]
