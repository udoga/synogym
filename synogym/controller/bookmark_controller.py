from flask import request, session
from synogym.data_classes import Bookmark, BookmarkWithMeaning
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService

class BookmarkController:
    def __init__(self, server: RestServer, service: BookmarkService):
        self.service = service
        server.add_route("/bookmarks", self.create, methods=["POST"])
        server.add_route("/bookmarks", self.list_by, methods=["GET"])
        server.add_route("/bookmarks/with-meaning", self.list_with_meaning, methods=["GET"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.update, methods=["PUT"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.delete, methods=["DELETE"])

    def create(self) -> Bookmark:
        data = request.get_json() or {}
        return self.service.create(self._get_user_id(), data["meaning_id"])

    def list_by(self) -> list[Bookmark]:
        if not "meaning_id" in request.args: raise ValueError("Missing meaning id")
        return self.service.list_by_user_and_meaning(self._get_user_id(), int(request.args["meaning_id"]))

    def list_with_meaning(self) -> list[BookmarkWithMeaning]:
        return self.service.list_with_meanings(self._get_user_id())

    def update(self, bookmark_id: int) -> Bookmark:
        data = request.get_json() or {}
        return self.service.update(self._get_user_id(), bookmark_id, data.get("note", ""), data.get("tags", ""))

    def delete(self, bookmark_id: int):
        self.service.delete(self._get_user_id(), bookmark_id)

    def _get_user_id(self) -> int:
        return int(session["user_id"])
