from synogym.generator import Generator
from synogym.meaning import Detail, Meaning

class MockGenerator(Generator):
    def __init__(self):
        self.meanings: list[Meaning] = []
        self.details: list[Detail] = []

    def generate_meanings(self, query: str) -> list[Meaning]:
        return [meaning for meaning in self.meanings if meaning.query == query]

    def generate_detail(self, meaning: Meaning) -> Detail:
        for detail in self.details:
            if detail.id == meaning.id:
                return detail
        raise ValueError("Detail not found")
