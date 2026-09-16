from dataclasses import asdict
from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException
from synogym.core_service import CoreService

class RestServer:
    def __init__(self, core_service: CoreService):
        self.core_service = core_service
        self.app = Flask(__name__)
        self.app.json.sort_keys = False
        self._add_error_handlers()
        self._add_routes()

    def run(self, port: int = 5000):
        self.app.run(port=port)

    def get_meanings(self, query: str) -> Response:
        meanings = self.core_service.list_meanings_by_query(query)
        return jsonify([asdict(meaning) for meaning in meanings])

    def get_detail(self, meaning_id: int) -> Response:
        detail = self.core_service.read_meaning_with_detail(meaning_id)
        return jsonify(asdict(detail))

    def get_quotes(self, query: str) -> Response:
        quotes = self.core_service.list_quotes_by_query(query)
        return jsonify([asdict(quote) for quote in quotes])

    def _add_error_handlers(self):
        self.app.register_error_handler(ValueError, self._handle_value_error)
        self.app.register_error_handler(HTTPException, self._handle_http_error)
        self.app.register_error_handler(Exception, self._handle_exception)

    def _handle_value_error(self, error: ValueError) -> tuple[Response, int]:
        return self._create_error_response(404, error)

    def _handle_http_error(self, error: HTTPException) -> tuple[Response, int]:
        return self._create_error_response(error.code or 500, error, error.description)

    def _handle_exception(self, error: Exception) -> tuple[Response, int]:
        return self._create_error_response(500, error)

    def _create_error_response(
        self, status: int, error: Exception, message: str | None = None
    ) -> tuple[Response, int]:
        error_json = {"error": {"status": status, "type": type(error).__name__, "message": message or str(error)}}
        return jsonify(error_json), status

    def _add_routes(self):
        self.app.add_url_rule("/meanings/<query>", view_func=self.get_meanings)
        self.app.add_url_rule("/meanings/<int:meaning_id>", view_func=self.get_detail)
        self.app.add_url_rule("/quotes/<query>", view_func=self.get_quotes)
