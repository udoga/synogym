from dataclasses import asdict
from flask import Response, jsonify
from synogym.meaning_service import MeaningService
from synogym.rest_server import RestServer

class MeaningController:
    def __init__(self, s: RestServer, service: MeaningService):
        self.service = service
        s.add_route("/meanings/<query>", self.list_meanings_by_query)
        s.add_route("/meanings/<int:meaning_id>", self.read_meaning_with_detail)

    def list_meanings_by_query(self, query: str) -> Response:
        meanings = self.service.list_by_query(query)
        return jsonify([asdict(meaning) for meaning in meanings])

    def read_meaning_with_detail(self, meaning_id: int) -> Response:
        detail = self.service.read_meaning_with_detail(meaning_id)
        return jsonify(asdict(detail))
