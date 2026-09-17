from dataclasses import asdict
from flask import Response, jsonify
from synogym.quote_service import QuoteService
from synogym.rest_server import RestServer

class QuoteController:
    def __init__(self, server: RestServer, service: QuoteService):
        self.service = service
        server.add_route("/quotes/<query>", self.list_quotes_by_query)

    def list_quotes_by_query(self, query: str) -> Response:
        quotes = self.service.list_quotes_by_query(query)
        return jsonify([asdict(quote) for quote in quotes])
