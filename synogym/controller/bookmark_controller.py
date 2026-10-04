from dataclasses import asdict
from flask import Response, jsonify, request, session
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService

class BookmarkController:
    def __init__(self, server: RestServer, service: BookmarkService):
        self.service = service
        server.add_route("/bookmarks", self.create, methods=["POST"])
        server.add_route("/bookmarks", self.get, methods=["GET"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.update, methods=["PUT"])
        server.add_route("/bookmarks/<int:bookmark_id>", self.delete, methods=["DELETE"])

    def create(self) -> Response:
        data = request.get_json() or {}
        bookmark = self.service.create(self._get_user_id(), data["meaning_id"])
        return jsonify(asdict(bookmark))

    def get(self) -> Response:
        if "meaning_id" in request.args: return self.find_by_meaning()
        return self.list_with_meanings()

    def list_with_meanings(self) -> Response:
        bookmarks = self.service.list_with_meanings(self._get_user_id())
        return jsonify([asdict(bookmark) for bookmark in bookmarks])

    def find_by_meaning(self) -> Response:
        meaning_id = int(request.args["meaning_id"])
        bookmark = self.service.find_by_meaning(self._get_user_id(), meaning_id)
        return jsonify(asdict(bookmark) if bookmark else {"bookmark": None})

    def update(self, bookmark_id: int) -> Response:
        data = request.get_json() or {}
        bookmark = self.service.update(self._get_user_id(), bookmark_id, data.get("note", ""), data.get("tags", ""))
        return jsonify(asdict(bookmark))

    def delete(self, bookmark_id: int) -> Response:
        self.service.delete(self._get_user_id(), bookmark_id)
        return jsonify({"bookmark": None})

    def _get_user_id(self) -> int:
        return int(session["user_id"])
