from synogym.service.meaning_service import MeaningService
from synogym.rest_server import RestServer

class MeaningController:
    def __init__(self, server: RestServer, service: MeaningService):
        server.add_route("/meanings/<query>", service.list_by_query)
        server.add_route("/meanings/<int:meaning_id>", service.read_meaning_with_detail)
