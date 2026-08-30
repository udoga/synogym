from dataclasses import asdict
from importlib.resources import files
from synogym.generator import Generator
from synogym.detail_parser import DetailParser
from synogym.formatter import Formatter
from synogym.gpt_model import GptModel
from synogym.meaning import Detail, Meaning
from synogym.meaning_parser import MeaningParser

class ModelGenerator(Generator):
    def __init__(self):
        self.model = GptModel(model="gpt-5", reasoning_effort="minimal")
        self.meaning_formatter = Formatter(self._read_file("meaning.txt"))
        self.detail_formatter = Formatter(self._read_file("detail.txt"))
        self.meaning_parser = MeaningParser()
        self.detail_parser = DetailParser()

    def generate_meanings(self, query: str) -> list[Meaning]:
        prompt = self.meaning_formatter.format({"query": query})
        response = self.model.respond(prompt)
        return self.meaning_parser.parse(response, query)

    def generate_detail(self, meaning: Meaning) -> Detail:
        prompt = self.detail_formatter.format(asdict(meaning))
        response = self.model.respond(prompt)
        return self.detail_parser.parse(response)

    def _read_file(self, file_name: str) -> str:
        return files("synogym").joinpath("resources", file_name).read_text()
