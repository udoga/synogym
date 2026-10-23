import yaml
import os
from pathlib import Path
from synogym.db_connector import DbConnector
from synogym.generator.detail_generator import DetailGenerator
from synogym.llm_gateway import LlmGateway
from synogym.generator.meaning_generator import MeaningGenerator
from synogym.client.brainy_client import BrainyClient
from synogym.client.gpt_client import GptClient
from synogym.controller.bookmark_controller import BookmarkController
from synogym.controller.meaning_controller import MeaningController
from synogym.controller.quote_controller import QuoteController
from synogym.controller.user_controller import UserController
from synogym.repo.sqlalchemy.sql_bookmark_repo import SqlBookmarkRepo
from synogym.repo.sqlalchemy.sql_llm_call_repo import SqlLlmCallRepo
from synogym.repo.sqlalchemy.sql_meaning_repo import SqlMeaningRepo
from synogym.repo.sqlalchemy.sql_quote_repo import SqlQuoteRepo
from synogym.repo.sqlalchemy.sql_user_repo import SqlUserRepo
from synogym.rest_server import RestServer
from synogym.service.bookmark_service import BookmarkService
from synogym.service.meaning_service import MeaningService
from synogym.service.quote_service import QuoteService
from synogym.service.user_service import UserService

def setup() -> RestServer:
    config_path = Path(os.environ.get("SYNOGYM_CONFIG_PATH", "config.yaml"))
    config: dict = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    connection = DbConnector().connect(config["database"])
    bookmark_repo = SqlBookmarkRepo(connection)
    meaning_repo = SqlMeaningRepo(connection)
    quote_repo = SqlQuoteRepo(connection)
    user_repo = SqlUserRepo(connection)
    llm_call_repo = SqlLlmCallRepo(connection)

    gpt_client = GptClient(config["llm"])
    llm_gateway = LlmGateway(config["llm"], gpt_client, llm_call_repo)
    meaning_generator = MeaningGenerator(llm_gateway)
    detail_generator = DetailGenerator(llm_gateway)
    brainy_client = BrainyClient() if config["brainy_quotes_enabled"] else None

    bookmark_service = BookmarkService(bookmark_repo)
    meaning_service = MeaningService(meaning_repo, meaning_generator, detail_generator)
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
