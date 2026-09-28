from unittest import TestCase
from synogym.generator.quote_fetcher import QuoteFetcher

class QuoteFetcherTest(TestCase):
    def test_fetches_quotes_from_brainyquote(self):
        quotes = QuoteFetcher().generate("life")
        self.assertGreaterEqual(len(quotes), 5)
        self.assertTrue(quotes[0].text)
        self.assertTrue(quotes[0].author)
        self.assertTrue(quotes[0].url.startswith("https://www.brainyquote.com/"))
