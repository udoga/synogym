from dataclasses import asdict
from flask import Response, jsonify, request
from synogym.rest_server import RestServer
from synogym.service.user_service import UserService

class UserController:
    def __init__(self, server: RestServer, service: UserService):
        self.service = service
        server.add_route("/users", self.create_user, methods=["POST"])

    def create_user(self) -> tuple[Response, int]:
        data = request.get_json() or {}
        user = self.service.create_user(data["email"], data["first_name"], data["last_name"])
        return jsonify(asdict(user)), 201
