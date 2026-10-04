from unittest import TestCase, skip
from synogym.generator.quote_fetcher import QuoteFetcher

class QuoteFetcherTest(TestCase):
    def test_makes_search_url_for_word(self):
        url = QuoteFetcher()._make_url("word")
        self.assertEqual("https://www.brainyquote.com/search_results?q=word", url)

    def test_makes_search_url_for_multiple_words(self):
        url = QuoteFetcher()._make_url("good life")
        self.assertEqual("https://www.brainyquote.com/search_results?q=good+life", url)

    def test_parses_quote_results(self):
        html = ('<a href="/quotes/test_1" class="b-qt qt_123">Life is good.</a>'
                '<a class="bq-aut qa_123" href="/authors/test">Test Author</a>')
        quotes = QuoteFetcher()._parse_quotes(html)
        values = [(quote.text, quote.author, quote.url) for quote in quotes]
        self.assertEqual([("Life is good.", "Test Author", "https://www.brainyquote.com/quotes/test_1")], values)

    @skip("Requires external BrainyQuote access")
    def test_fetches_quotes_from_brainyquote(self):
        quotes = QuoteFetcher().generate("life")
        self.assertGreaterEqual(len(quotes), 5)
        self.assertTrue(quotes[0].text)
        self.assertTrue(quotes[0].author)
        self.assertTrue(quotes[0].url.startswith("https://www.brainyquote.com/"))
