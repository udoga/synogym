from unittest import TestCase
from synogym.controller.bookmark_controller import BookmarkController
from synogym.repo.list_bookmark_repo import ListBookmarkRepo
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService

class BookmarkControllerTest(TestCase):
    def setUp(self):
        self.repo = ListBookmarkRepo()
        self.rest_server = RestServer(check_login=False)
        self.service = BookmarkService(self.repo)
        self.controller = BookmarkController(self.rest_server, self.service)
        self.client = self.rest_server.app.test_client()
        with self.client.session_transaction() as session:
            session["user_id"] = 1

    def test_saves_bookmark(self):
        response = self.client.post("/bookmarks", json={"meaning_id": 2})
        expected = {"id": 1, "user_id": 1, "meaning_id": 2, "note": "", "tags": ""}
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.get_json())

    def test_reads_bookmark_by_meaning(self):
        self.client.post("/bookmarks", json={"meaning_id": 2})
        response = self.client.get("/bookmarks?meaning_id=2")
        expected = {"id": 1, "user_id": 1, "meaning_id": 2, "note": "", "tags": ""}
        self.assertEqual(expected, response.get_json())

    def test_returns_null_for_unsaved_meaning(self):
        response = self.client.get("/bookmarks?meaning_id=2")
        self.assertEqual({"bookmark": None}, response.get_json())

    def test_updates_bookmark(self):
        self.client.post("/bookmarks", json={"meaning_id": 2})
        response = self.client.put("/bookmarks/1", json={"note": "note", "tags": "tag"})
        expected = {"id": 1, "user_id": 1, "meaning_id": 2, "note": "note", "tags": "tag"}
        self.assertEqual(expected, response.get_json())

    def test_deletes_bookmark(self):
        self.client.post("/bookmarks", json={"meaning_id": 2})
        response = self.client.delete("/bookmarks/1")
        self.assertEqual({"bookmark": None}, response.get_json())
        self.assertEqual({"bookmark": None}, self.client.get("/bookmarks?meaning_id=2").get_json())
