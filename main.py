from synogym.meaning_service import MeaningService
from synogym.mock_repo import MockRepo
from synogym.model_generator import ModelGenerator
from synogym.rest_service import RestService

if __name__ == "__main__":
    generator = ModelGenerator()
    repo = MockRepo()
    meaning_service = MeaningService(generator, repo)
    rest_service = RestService(meaning_service)
    rest_service.run()
