import yaml
import os
from pathlib import Path
from synogym.db_connector import DbConnector
from synogym.rest_server import RestServer
from synogym.generator import DetailGenerator, ExampleGenerator, MeaningGenerator
from synogym.client import BrainyClient, GptClient
from synogym.repo.sqlalchemy import SqlBookmarkRepo, SqlMeaningRepo, SqlQuoteRepo, SqlUserRepo
from synogym.service import BookmarkService, MeaningService, QuoteService, UserService
from synogym.controller import BookmarkController, MeaningController, QuoteController, UserController

def setup() -> RestServer:
    config_path = Path(os.environ.get("SYNOGYM_CONFIG_PATH", "config.yaml"))
    config: dict = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    connection = DbConnector().connect(config["database"])
    bookmark_repo = SqlBookmarkRepo(connection)
    meaning_repo = SqlMeaningRepo(connection)
    quote_repo = SqlQuoteRepo(connection)
    user_repo = SqlUserRepo(connection)

    gpt_client = GptClient(config["llm"])
    meaning_generator = MeaningGenerator(gpt_client)
    detail_generator = DetailGenerator(gpt_client)
    example_generator = ExampleGenerator(gpt_client)
    brainy_client = BrainyClient() if config["brainy_quotes_enabled"] else None

    bookmark_service = BookmarkService(bookmark_repo)
    meaning_service = MeaningService(meaning_repo, meaning_generator, detail_generator, example_generator)
    quote_service = QuoteService(quote_repo, brainy_client)
    user_service = UserService(user_repo)

    rest_server = RestServer(config["server"])
    BookmarkController(rest_server, bookmark_service)
    MeaningController(rest_server, meaning_service)
    QuoteController(rest_server, quote_service)
    UserController(rest_server, user_service, config["google_client_id"])
    return rest_server

if __name__ == "__main__":
    setup().run()
else: # gunicorn
    app = setup().app
