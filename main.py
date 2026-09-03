from pathlib import Path
from synogym.meaning_service import MeaningService
from synogym.model_generator import ModelGenerator
from synogym.rest_service import RestService
from synogym.console import Console
from synogym.sqlite_repo import SqliteRepo

if __name__ == "__main__":
    generator = ModelGenerator()
    schema_sql_path = str(Path(__file__).resolve().parent / "sqlite-schema.sql")
    repo = SqliteRepo("synogym.sqlite", schema_sql_path)
    meaning_service = MeaningService(generator, repo)
    rest_service = RestService(meaning_service)
    console = Console(meaning_service)
    rest_service.run()
