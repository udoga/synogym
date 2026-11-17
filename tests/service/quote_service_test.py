from dataclasses import replace
from unittest import TestCase
from unittest.mock import patch
from synogym.data_classes import Quote
from synogym.repo.memory import MemoryQuoteRepo
from synogym.service import QuoteService
from synogym.usage_checker import UsageChecker

class FakeUsageChecker(UsageChecker):
    def __init__(self):
        super().__init__()
        self.inflections = None

    def create_inflections(self, query: str, pos: str) -> list[str]:
        return self.inflections if self.inflections else [query]

    def is_usage_example(self, text: str, inflections: list[str], pos: str) -> bool:
        return not "Wrong" in text

class QuoteServiceTest(TestCase):
    def setUp(self):
        self.repo = MemoryQuoteRepo()
        self.usage_checker = FakeUsageChecker()
        self.service = QuoteService(self.repo, self.usage_checker)
        self.sample_patch = patch("synogym.service.quote_service.random.sample", side_effect=lambda q, c: q[:c])
        self.sample = self.sample_patch.start()
        self.addCleanup(self.sample_patch.stop)

    def test_returns_quotes_from_repo(self):
        quotes = self.create_quotes("Be yourself", self.service.quote_limit)
        self.repo.create_all(quotes)
        self.assertEqual(self.highlight_quotes(quotes), self.service.list_by_query("yourself", "noun"))

    def test_uses_inflections_when_searching_quotes(self):
        self.usage_checker.inflections = ["experiences"]
        quote = Quote(text="Experiences shape us.", author="Oscar Wilde", url="quote")
        self.repo.create_all([quote])
        highlighted = replace(quote, text="<em>Experiences</em> shape us.")
        self.assertEqual([highlighted], self.service.list_by_query("experience", "noun"))

    def test_filters_quotes_by_usage(self):
        right = Quote(text="Be yourself", author="Oscar Wilde", url="right")
        wrong = Quote(text="Wrong yourself", author="Oscar Wilde", url="wrong")
        self.repo.create_all([right, wrong])
        self.assertEqual(self.highlight_quotes([right]), self.service.list_by_query("yourself", "noun"))

    def test_limits_number_of_quotes_from_repo_when_repo_has_more(self):
        quotes = self.create_quotes("Be yourself", self.service.quote_limit+1)
        self.repo.create_all(quotes)
        highlighted = self.highlight_quotes(quotes)
        self.assertEqual(highlighted[:self.service.quote_limit], self.service.list_by_query("yourself", "noun"))
        self.sample.assert_called_with(highlighted, self.service.quote_limit)

    def test_returns_quotes_under_200_characters(self):
        short_quote = Quote(text=f"Be yourself {'a' * 186}", author="Oscar Wilde", url="short")
        long_quote = Quote(text=f"Be yourself {'a' * 188}", author="Oscar Wilde", url="long")
        self.repo.create_all([short_quote, long_quote])
        self.assertEqual(self.highlight_quotes([short_quote]), self.service.list_by_query("yourself", "noun"))

    def test_highlights_query_in_quotes(self):
        self.usage_checker.inflections = ["told off"]
        quote = Quote(text="The teacher told off the students.", author="Oscar Wilde", url="quote")
        self.repo.create_all([quote])
        result = self.service.list_by_query("told off", "verb")
        self.assertEqual("The teacher <em>told off</em> the students.", result[0].text)

    def highlight_quotes(self, quotes: list[Quote]) -> list[Quote]:
        return [replace(q, text=q.text.replace("yourself", "<em>yourself</em>")) for q in quotes]

    def create_quotes(self, content: str, count: int) -> list[Quote]:
        return [Quote(text=f"{content} {number}", author="Oscar Wilde", url=f"https://example.com/{number}")
                for number in range(count)]
