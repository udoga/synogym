from synogym.service.quote_service import QuoteService
from synogym.rest_server import RestServer

class QuoteController:
    def __init__(self, server: RestServer, service: QuoteService):
        server.add_route("/quotes/<query>", service.list_by_query)
