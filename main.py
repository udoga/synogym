from synogym.meaning_service import MeaningService
from synogym.memory_repo import MemoryRepo
from synogym.model_generator import ModelGenerator
from synogym.rest_service import RestService
from synogym.console import Console

if __name__ == "__main__":
    generator = ModelGenerator()
    repo = MemoryRepo()
    meaning_service = MeaningService(generator, repo)
    rest_service = RestService(meaning_service)
    console = Console(meaning_service)
    console.run()
