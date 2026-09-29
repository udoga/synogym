from collections.abc import Callable
import os
from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException

class RestServer:
    def __init__(self, port: int = 5000):
        self.port = port
        self.app = Flask(__name__, static_folder="web")
        self.app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
        self.app.json.sort_keys = False
        self.add_home_route()
        self.add_error_handlers()

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port)

    def add_route(self, rule: str, view_func: Callable[..., Response], methods: list[str] | None = None):
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def add_home_route(self):
        self.app.add_url_rule("/", view_func=self.render_home)

    def render_home(self) -> Response:
        return self.app.send_static_file("index.html")

    def add_error_handlers(self):
        self.app.register_error_handler(ValueError, self.handle_value_error)
        self.app.register_error_handler(HTTPException, self.handle_http_error)
        self.app.register_error_handler(Exception, self.handle_exception)

    def handle_value_error(self, error: ValueError) -> tuple[Response, int]:
        return self.create_error_response(404, error)

    def handle_http_error(self, error: HTTPException) -> tuple[Response, int]:
        return self.create_error_response(error.code or 500, error, error.description)

    def handle_exception(self, error: Exception) -> tuple[Response, int]:
        return self.create_error_response(500, error)

    def create_error_response(self, status: int, error: Exception, message: str | None = None) -> tuple[Response, int]:
        error_json = {"error": {"status": status, "type": type(error).__name__, "message": message or str(error)}}
        return jsonify(error_json), status
