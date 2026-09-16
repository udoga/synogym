from unittest import TestCase
from synogym.data_classes import Meaning, MeaningWithDetail, Quote
from synogym.rest_server import RestServer

class MockCoreService:
    def list_meanings(self, query: str) -> list[Meaning]:
        raise ValueError("Meaning not found")

    def read_meaning_with_detail(self, meaning_id: int) -> MeaningWithDetail:
        raise ValueError("Meaning not found")

    def list_quotes(self, query: str) -> list[Quote]:
        return [Quote(text="Be yourself", author="Oscar Wilde", url="https://example.com/quote")]

class RestServerTest(TestCase):
    def setUp(self):
        self.service = MockCoreService()
        self.client = RestServer(self.service).app.test_client()

    def test_returns_json_for_value_error(self):
        response = self.client.get("/meanings/happy")
        self.assertEqual(404, response.status_code)
        self.assertEqual({"error": {"status": 404, "type": "ValueError", "message": "Meaning not found"}},
                         response.get_json())

    def test_returns_quotes(self):
        response = self.client.get("/quotes/happy")
        expected = [{"text": "Be yourself", "author": "Oscar Wilde", "url": "https://example.com/quote"}]
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.get_json())
