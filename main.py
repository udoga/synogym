import yaml
from pathlib import Path
from synogym.sqlite_connector import SqliteConnector
from synogym.generator.detail_generator import DetailGenerator
from synogym.generator.meaning_generator import MeaningGenerator
from synogym.generator.quote_fetcher import QuoteFetcher
from synogym.gpt_model import GptModel
from synogym.controller.bookmark_controller import BookmarkController
from synogym.controller.meaning_controller import MeaningController
from synogym.controller.quote_controller import QuoteController
from synogym.controller.user_controller import UserController
from synogym.repo.sql_bookmark_repo import SqlBookmarkRepo
from synogym.repo.sql_meaning_repo import SqlMeaningRepo
from synogym.repo.sql_quote_repo import SqlQuoteRepo
from synogym.repo.sql_user_repo import SqlUserRepo
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService
from synogym.service.meaning_service import MeaningService
from synogym.service.quote_service import QuoteService
from synogym.service.user_service import UserService

if __name__ == "__main__":
    config: dict = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    model = GptModel(model="gpt-5", reasoning_effort="minimal")
    meaning_generator = MeaningGenerator(model)
    detail_generator = DetailGenerator(model)
    quote_fetcher = QuoteFetcher()

    connection = SqliteConnector().connect("synogym.sqlite", ["sqlite-schema.sql", "sqlite-data.sql"])
    bookmark_repo = SqlBookmarkRepo(connection)
    meaning_repo = SqlMeaningRepo(connection)
    quote_repo = SqlQuoteRepo(connection)
    user_repo = SqlUserRepo(connection)

    bookmark_service = BookmarkService(bookmark_repo)
    meaning_service = MeaningService(meaning_repo, meaning_generator, detail_generator)
    quote_service = QuoteService(quote_repo, quote_fetcher)
    user_service = UserService(user_repo)

    rest_server = RestServer(8080, config["flask_secret_key"])
    bookmark_controller = BookmarkController(rest_server, bookmark_service)
    meaning_controller = MeaningController(rest_server, meaning_service)
    quote_controller = QuoteController(rest_server, quote_service)
    user_controller = UserController(rest_server, user_service, config["google_client_id"])
    rest_server.run()
