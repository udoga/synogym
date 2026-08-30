from dataclasses import asdict
from flask import Flask, Response, jsonify, request
from synogym.api import Api
from synogym.meaning import Meaning

class RestService:
    def __init__(self, api: Api):
        self.api = api
        self.app = Flask(__name__)
        self._add_routes()

    def run(self):
        self.app.run()

    def get_meanings(self, query: str) -> Response:
        meanings = self.api.get_meanings(query)
        return jsonify([asdict(meaning) for meaning in meanings])

    def get_detail(self) -> Response:
        detail = self.api.get_detail(self._create_meaning())
        return jsonify(asdict(detail))

    def _add_routes(self):
        self.app.add_url_rule("/meanings/<query>", view_func=self.get_meanings)
        self.app.add_url_rule("/detail", view_func=self.get_detail, methods=["POST"])

    def _create_meaning(self) -> Meaning:
        return Meaning(**request.get_json())
