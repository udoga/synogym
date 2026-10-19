from flask import request, session
from synogym.data_classes import Bookmark, ExampleWithBookmark, MeaningWithBookmark
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService

class BookmarkController:
    def __init__(self, server: RestServer, service: BookmarkService):
        self.service = service
        server.add_route("/bookmarks", self.list_by, methods=["GET"])
        server.add_route("/bookmarks/meanings", self.list_meanings_with_bookmark, methods=["GET"])
        server.add_route("/bookmarks/examples", self.list_examples_with_bookmark, methods=["GET"])
        server.add_route("/bookmarks", self.create, methods=["POST"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.update, methods=["PUT"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.delete, methods=["DELETE"])

    def list_by(self) -> list[Bookmark]:
        return self.service.list_by(self._get_user_id(), self._get_int_arg("meaning_id"))

    def list_meanings_with_bookmark(self) -> list[MeaningWithBookmark]:
        return self.service.list_meanings_with_bookmark(self._get_user_id())

    def list_examples_with_bookmark(self) -> list[ExampleWithBookmark]:
        return self.service.list_examples_with_bookmark(self._get_user_id())

    def create(self) -> Bookmark:
        data = request.get_json() or {}
        return self.service.create(self._get_user_id(), data["meaning_id"])

    def update(self, bookmark_id: int) -> Bookmark:
        data = request.get_json() or {}
        return self.service.update(self._get_user_id(), bookmark_id, data.get("note", ""), data.get("tags", ""))

    def delete(self, bookmark_id: int):
        self.service.delete(self._get_user_id(), bookmark_id)

    def _get_int_arg(self, key) -> int | None:
        return int(request.args[key]) if key in request.args else None

    def _get_user_id(self) -> int:
        return int(session["user_id"])
