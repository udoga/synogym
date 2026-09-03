from pathlib import Path
from synogym.core_service import CoreService
from synogym.model_generator import ModelGenerator
from synogym.rest_server import RestServer
from synogym.console import Console
from synogym.sqlite_repo import SqliteRepo

if __name__ == "__main__":
    generator = ModelGenerator()
    schema_sql_path = str(Path(__file__).resolve().parent / "sqlite-schema.sql")
    repo = SqliteRepo("synogym.sqlite", schema_sql_path)
    core_service = CoreService(generator, repo)
    rest_server = RestServer(core_service)
    console = Console(core_service)
    rest_server.run(port=8080)
