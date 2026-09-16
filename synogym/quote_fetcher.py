from html import unescape
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import re
from synogym.data_classes import Quote
from synogym.generator import Generator

class QuoteFetcher(Generator[str, list[Quote]]):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
    }

    def generate(self, query: str) -> list[Quote]:
        return self.fetch(query)

    def fetch(self, query: str) -> list[Quote]:
        html = self._fetch_html(self._make_url(query))
        return self._parse_quotes(html)

    def _make_url(self, query: str) -> str:
        return f"https://www.brainyquote.com/topics/{self._make_slug(query)}-quotes"

    def _make_slug(self, query: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")

    def _fetch_html(self, url: str) -> str:
        with urlopen(Request(url, headers=self.HEADERS), timeout=10) as response:
            return response.read().decode("utf-8", "ignore")

    def _parse_quotes(self, html: str) -> list[Quote]:
        matches = re.findall(self._quote_pattern(), html, re.DOTALL)
        return [self._make_quote(path, text, author) for path, text, author in matches]

    def _quote_pattern(self) -> str:
        return (r'<a[^>]+href="([^"]+)"[^>]+class="[^"]*b-qt[^"]*"[^>]*>(.*?)</a>\s*'
                r'<a[^>]+class="[^"]*bq-aut[^"]*"[^>]*>(.*?)</a>')

    def _make_quote(self, path: str, text: str, author: str) -> Quote:
        return Quote(text=self._clean(text), author=self._clean(author), url=urljoin(self._base_url(), path))

    def _base_url(self) -> str:
        return "https://www.brainyquote.com"

    def _clean(self, html: str) -> str:
        text = re.sub(r"<[^>]+>", "", html)
        return unescape(text).strip()
