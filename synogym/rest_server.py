from collections.abc import Callable
from dataclasses import asdict, is_dataclass
from functools import partial
from flask import Flask, Response, jsonify, request, session
from werkzeug.exceptions import HTTPException, Unauthorized

class RestServer:
    def __init__(self, port: int = 5000, flask_secret_key: str = "dev-secret-key", check_login: bool = True):
        self.port = port
        self.check_login = check_login
        self.app = Flask(__name__, static_folder="web")
        self.app.secret_key = flask_secret_key
        self.app.json.sort_keys = False
        self.public_paths = {"/", "/auth/config", "/auth/google", "/auth/sign-in", "/auth/sign-up"}
        self.add_home_route()
        self.add_request_hooks()
        self.add_error_handlers()

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port)

    def add_route(self, rule: str, view_func: Callable[..., object], methods: list[str] | None = None):
        endpoint = f"{rule}:{','.join(methods or ['GET'])}"
        wrapped_view_func = partial(self._to_json_response, view_func)
        self.app.add_url_rule(rule, endpoint=endpoint, view_func=wrapped_view_func, methods=methods)

    def _to_json_response(self, view_func: Callable[..., object], *args: object, **kwargs: object) -> Response:
        result = view_func(*args, **kwargs)
        return result if isinstance(result, Response) else jsonify({"data": self._to_dict(result)})

    def _to_dict(self, value: object) -> object:
        if is_dataclass(value): return asdict(value)
        if isinstance(value, list): return [self._to_dict(item) for item in value]
        if isinstance(value, dict): return {key: self._to_dict(item) for key, item in value.items()}
        return value

    def add_home_route(self):
        self.app.add_url_rule("/", view_func=self.render_home)

    def add_request_hooks(self):
        if self.check_login:
            self.app.before_request(self.check_signed_in)

    def check_signed_in(self) -> Response | None:
        if self._is_public_request() or session.get("user_id"):
            return None
        raise Unauthorized("Sign in required")

    def _is_public_request(self) -> bool:
        return request.path in self.public_paths or request.endpoint == "static"

    def render_home(self) -> Response:
        response = self.app.send_static_file("index.html")
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        return response

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
