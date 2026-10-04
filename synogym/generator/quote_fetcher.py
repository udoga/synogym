from html import unescape
import re
from urllib.parse import urlencode, urljoin
from curl_cffi import requests
from synogym.data_classes import Quote
from synogym.generator.generator import Generator

class QuoteFetcher(Generator[str, list[Quote]]):
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    def generate(self, query: str) -> list[Quote]:
        return self.fetch(query)

    def fetch(self, query: str) -> list[Quote]:
        html = self._fetch_html(self._make_url(query))
        return self._parse_quotes(html)

    def _make_url(self, query: str) -> str:
        return f"{self._base_url()}/search_results?{urlencode({'q': query})}"

    def _fetch_html(self, url: str) -> str:
        response = requests.get(url, headers=self.HEADERS, impersonate="chrome", timeout=10)
        response.raise_for_status()
        return response.text

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
