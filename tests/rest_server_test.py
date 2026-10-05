from unittest import TestCase
from synogym.data_classes import Meaning
from synogym.rest_server import RestServer

class MockController:
    def __init__(self, rest_server: RestServer):
        self.meanings: list[Meaning] = [Meaning(query="happy", definition="feeling joy", pos="adjective")]
        rest_server.add_route("/meanings/<query>", self.get_meanings)

    def get_meanings(self, query: str) -> list[Meaning]:
        if query == "happy":
            return self.meanings
        raise ValueError("Meaning not found")

class RestServerTest(TestCase):
    def setUp(self):
        self.rest_server = RestServer({})
        self.controller = MockController(self.rest_server)
        self.client = self.rest_server.app.test_client()

    def test_returns_json_for_value_error(self):
        response = self.client.get("/meanings/asd")
        expected = {"error": {"status": 404, "type": "ValueError", "message": "Meaning not found"}}
        self.assertEqual(404, response.status_code)
        self.assertEqual(expected, response.get_json())

    def test_returns_meanings(self):
        response = self.client.get("/meanings/happy")
        expected = {"data": [{"id": None, "query": "happy", "definition": "feeling joy", "pos": "adjective"}]}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.get_json())

    def test_rejects_guest_requests(self):
        rest_server = RestServer({"check_login": True})
        MockController(rest_server)
        response = rest_server.app.test_client().get("/meanings/happy")
        expected = {"error": {"status": 401, "type": "Unauthorized", "message": "Sign in required"}}
        self.assertEqual(401, response.status_code)
        self.assertEqual(expected, response.get_json())
