from pathlib import Path
from synogym.core_service import CoreService
from synogym.detail_generator import DetailGenerator
from synogym.meaning_generator import MeaningGenerator
from synogym.gpt_model import GptModel
from synogym.rest_server import RestServer
from synogym.console import Console
from synogym.sqlite_repo import SqliteRepo

if __name__ == "__main__":
    repo = SqliteRepo("synogym.sqlite", str(Path(__file__).resolve().parent / "sqlite-schema.sql"))
    model = GptModel(model="gpt-5", reasoning_effort="minimal")
    meaning_generator = MeaningGenerator(model)
    detail_generator = DetailGenerator(model)
    core_service = CoreService(repo, meaning_generator, detail_generator)
    rest_server = RestServer(core_service)
    console = Console(core_service)
    rest_server.run(port=8080)
