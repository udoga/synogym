from unittest import TestCase
from unittest.mock import patch
from synogym.data_classes import Quote
from synogym.repo.memory import MemoryQuoteRepo
from synogym.generator import MockGenerator
from synogym.service import QuoteService

class QuoteServiceTest(TestCase):
    def setUp(self):
        self.repo = MemoryQuoteRepo()
        self.brainy_client = MockGenerator[str, list[Quote]]([])
        self.service = QuoteService(self.repo, self.brainy_client)
        self.sample_patch = patch("synogym.service.quote_service.random.sample", side_effect=lambda q, c: q[:c])
        self.sample = self.sample_patch.start()
        self.addCleanup(self.sample_patch.stop)

    def test_fetches_and_saves_quotes_when_repo_is_empty(self):
        self.brainy_client.output = [Quote(text="Be yourself", author="Oscar Wilde", url="https://example.com/quote")]
        self.assertEqual(self.brainy_client.output, self.service.list_by_query("yourself"))
        self.assertEqual(self.brainy_client.output, self.repo.list_by_query("yourself"))

    def test_fetches_and_saves_quotes_when_repo_has_four(self):
        self.repo.create_all(self.create_quotes("Be yourself", 4))
        self.brainy_client.output = self.create_quotes("Generated yourself", 5)
        self.assertEqual(self.brainy_client.output, self.service.list_by_query("yourself"))
        self.assertEqual(9, len(self.repo.quotes))

    def test_returns_quotes_from_repo_when_repo_has_five(self):
        quotes = self.create_quotes("Be yourself", 5)
        self.repo.create_all(quotes)
        self.assertEqual(quotes, self.service.list_by_query("yourself"))

    def test_returns_five_random_quotes_from_repo_when_repo_has_more(self):
        quotes = self.create_quotes("Be yourself", 6)
        self.repo.create_all(quotes)
        self.assertEqual(quotes[:5], self.service.list_by_query("yourself"))
        self.sample.assert_called_with(quotes, 5)

    def test_returns_five_quotes_from_fetcher_when_fetcher_has_more(self):
        self.brainy_client.output = self.create_quotes("Generated yourself", 6)
        self.assertEqual(self.brainy_client.output[:5], self.service.list_by_query("yourself"))

    def test_returns_repo_quotes_when_quote_generator_is_none(self):
        service = QuoteService(self.repo, None)
        quotes = self.create_quotes("Be yourself", 2)
        self.repo.create_all(quotes)
        self.assertEqual(quotes, service.list_by_query("yourself"))

    def test_returns_quotes_under_200_characters(self):
        short_quote = Quote(text=f"Be yourself {'a' * 186}", author="Oscar Wilde", url="short")
        long_quote = Quote(text=f"Be yourself {'a' * 188}", author="Oscar Wilde", url="long")
        service = QuoteService(self.repo, None)
        self.repo.create_all([short_quote, long_quote])
        self.assertEqual([short_quote], service.list_by_query("yourself"))

    def create_quotes(self, content: str, count: int) -> list[Quote]:
        return [Quote(text=f"{content} {number}", author="Oscar Wilde", url=f"https://example.com/{number}")
                for number in range(count)]
