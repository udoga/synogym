from unittest import TestCase
from synogym.controller.user_controller import UserController
from synogym.repo.list_user_repo import ListUserRepo
from synogym.rest_server import RestServer
from synogym.service.user_service import UserService

class UserControllerTest(TestCase):
    def setUp(self):
        self.repo = ListUserRepo()
        self.rest_server = RestServer()
        self.service = UserService(self.repo)
        self.controller = UserController(self.rest_server, self.service, "google-client-id")
        self.controller._verify_google_credential = self.verify_google_credential
        self.client = self.rest_server.app.test_client()

    def verify_google_credential(self, credential: str) -> dict:
        self.credential = credential
        return {"email": "ada@example.com", "given_name": "Ada", "family_name": "Lovelace"}

    def test_returns_google_client_id(self):
        response = self.client.get("/auth/config")
        self.assertEqual({"google_client_id": "google-client-id"}, response.get_json())

    def test_signs_in_google_user(self):
        response = self.client.post("/auth/google", json={"credential": "google-token"})
        expected = {"user": {"id": 1, "email": "ada@example.com", "first_name": "Ada", "last_name": "Lovelace"}}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.get_json())
        self.assertEqual("google-token", self.credential)

    def test_returns_current_user(self):
        self.client.post("/auth/google", json={"credential": "google-token"})
        response = self.client.get("/auth/me")
        expected = {"user": {"id": 1, "email": "ada@example.com", "first_name": "Ada", "last_name": "Lovelace"}}
        self.assertEqual(expected, response.get_json())

    def test_logs_out_user(self):
        self.client.post("/auth/google", json={"credential": "google-token"})
        response = self.client.post("/auth/logout", json={})
        self.assertEqual({"user": None}, response.get_json())
        self.assertEqual({"user": None}, self.client.get("/auth/me").get_json())

    def test_reuses_existing_google_user(self):
        self.client.post("/auth/google", json={"credential": "google-token"})
        self.client.post("/auth/google", json={"credential": "google-token"})
        self.assertEqual(1, len(self.repo.users))
