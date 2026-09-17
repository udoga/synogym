from collections.abc import Callable
from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException

class RestServer:
    def __init__(self, port: int = 5000):
        self.port = port
        self.app = Flask(__name__)
        self.app.json.sort_keys = False
        self.add_error_handlers()

    def run(self):
        self.app.run(port=self.port)

    def add_route(self, rule: str, view_func: Callable[..., Response]):
        self.app.add_url_rule(rule, view_func=view_func)

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
