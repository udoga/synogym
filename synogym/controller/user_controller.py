from dataclasses import asdict
from flask import Response, jsonify, request, session
from synogym.google_token_verifier import GoogleTokenVerifier
from synogym.rest_server import RestServer
from synogym.service.user_service import UserService

class UserController:
    def __init__(self, server: RestServer, service: UserService, verifier: GoogleTokenVerifier | None = None):
        self.service = service
        self.verifier = verifier or GoogleTokenVerifier()
        self._add_routes(server)

    def _add_routes(self, server: RestServer):
        server.add_route("/users", self.create_user, methods=["POST"])
        server.add_route("/auth/config", self.read_auth_config)
        server.add_route("/auth/google", self.sign_in_with_google, methods=["POST"])
        server.add_route("/auth/me", self.read_current_user)
        server.add_route("/auth/logout", self.logout, methods=["POST"])

    def create_user(self) -> tuple[Response, int]:
        data = request.get_json() or {}
        user = self.service.create_user(data["email"], data["first_name"], data["last_name"])
        return jsonify(asdict(user)), 201

    def read_auth_config(self) -> Response:
        return jsonify({"google_client_id": self.verifier.client_id})

    def sign_in_with_google(self) -> Response:
        data = request.get_json() or {}
        google_user = self.verifier.verify(data["credential"])
        user = self.service.find_or_create_user(google_user.email, google_user.first_name, google_user.last_name)
        session["user_id"] = user.id
        return jsonify({"user": asdict(user)})

    def read_current_user(self) -> Response:
        user_id = session.get("user_id")
        user = self.service.find_user(user_id) if user_id else None
        return jsonify({"user": asdict(user) if user else None})

    def logout(self) -> Response:
        session.clear()
        return jsonify({"user": None})
