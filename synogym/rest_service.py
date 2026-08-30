from dataclasses import asdict
from flask import Flask, Response, jsonify
from synogym.meaning_service import MeaningService

class RestService:
    def __init__(self, meaning_service: MeaningService):
        self.meaning_service = meaning_service
        self.app = Flask(__name__)
        self.app.json.sort_keys = False
        self._add_routes()

    def run(self):
        self.app.run()

    def get_meanings(self, query: str) -> Response:
        meanings = self.meaning_service.list_meanings(query)
        return jsonify([asdict(meaning) for meaning in meanings])

    def get_detail(self, meaning_id: int) -> Response:
        detail = self.meaning_service.read_meaning_with_detail(meaning_id)
        return jsonify(asdict(detail))

    def _add_routes(self):
        self.app.add_url_rule("/meanings/<query>", view_func=self.get_meanings)
        self.app.add_url_rule("/detail/<int:meaning_id>", view_func=self.get_detail)
