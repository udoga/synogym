from dataclasses import asdict
from flask import Response, jsonify, request, session
from google.auth.transport import requests
from google.oauth2 import id_token
from synogym.data_classes import User
from synogym.rest_server import RestServer
from synogym.service.user_service import UserService

class UserController:
    def __init__(self, server: RestServer, service: UserService, google_client_id: str):
        self.service = service
        self.google_client_id = google_client_id
        self._add_routes(server)

    def _add_routes(self, server: RestServer):
        server.add_route("/auth/config", self.read_auth_config)
        server.add_route("/auth/google", self.sign_in_with_google, methods=["POST"])
        server.add_route("/auth/sign-in", self.sign_in, methods=["POST"])
        server.add_route("/auth/sign-up", self.sign_up, methods=["POST"])
        server.add_route("/auth/me", self.read_current_user)
        server.add_route("/auth/logout", self.logout, methods=["POST"])

    def read_auth_config(self) -> Response:
        return jsonify({"google_client_id": self.google_client_id})

    def sign_in_with_google(self) -> Response:
        data = request.get_json() or {}
        payload = self._verify_google_credential(data["credential"])
        google_user = User(payload["email"], payload.get("given_name", ""), payload.get("family_name", ""))
        user = self.service.find_or_create_user(google_user)
        session["user_id"] = user.id
        return jsonify({"user": asdict(user)})

    def sign_in(self) -> Response:
        data = request.get_json() or {}
        user = self.service.sign_in(data.get("email", ""), data.get("password", ""))
        session["user_id"] = user.id
        return jsonify({"user": asdict(user)})

    def sign_up(self) -> Response:
        data = request.get_json() or {}
        user = self.service.sign_up(data.get("email", ""), data.get("password", ""))
        session["user_id"] = user.id
        return jsonify({"user": asdict(user)})

    def _verify_google_credential(self, credential: str) -> dict:
        assert self.google_client_id, "Google client ID is not configured"
        payload = id_token.verify_oauth2_token(credential, requests.Request(), self.google_client_id)
        assert payload.get("email_verified"), "Google email is not verified"
        return payload

    def read_current_user(self) -> Response:
        user_id = session.get("user_id")
        user = self.service.find_user(user_id) if user_id else None
        return jsonify({"user": asdict(user) if user else None})

    def logout(self) -> Response:
        session.clear()
        return jsonify({"user": None})
