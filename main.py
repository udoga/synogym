from sqlite_connector import SqliteConnector
from synogym.detail_generator import DetailGenerator
from synogym.gpt_model import GptModel
from synogym.meaning_controller import MeaningController
from synogym.meaning_generator import MeaningGenerator
from synogym.meaning_service import MeaningService
from synogym.quote_controller import QuoteController
from synogym.quote_fetcher import QuoteFetcher
from synogym.quote_service import QuoteService
from synogym.rest_server import RestServer
from synogym.sql_meaning_repo import SqlMeaningRepo
from synogym.sql_quote_repo import SqlQuoteRepo

if __name__ == "__main__":
    model = GptModel(model="gpt-5", reasoning_effort="minimal")
    meaning_generator = MeaningGenerator(model)
    detail_generator = DetailGenerator(model)
    quote_fetcher = QuoteFetcher()

    connection = SqliteConnector().connect("synogym.sqlite", "sqlite-schema.sql")
    meaning_repo = SqlMeaningRepo(connection)
    quote_repo = SqlQuoteRepo(connection)

    meaning_service = MeaningService(meaning_repo, meaning_generator, detail_generator)
    quote_service = QuoteService(quote_repo, quote_fetcher)

    rest_server = RestServer(port=8080)
    meaning_controller = MeaningController(rest_server, meaning_service)
    quote_controller = QuoteController(rest_server, quote_service)
    rest_server.run()
