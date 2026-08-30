from importlib.resources import files
from pprint import pprint
from synogym.detail_parser import DetailParser
from synogym.gpt_model import GptModel
from synogym.meaning import Meaning, DetailedMeaning
from synogym.meaning_parser import MeaningParser
from synogym.prompter import Prompter

class Application:
    def __init__(self):
        self.model = GptModel(model="gpt-5", reasoning_effort="minimal")
        self.meaning_prompter = Prompter(self.model, self.read_file("meaning.txt"))
        self.detail_prompter = Prompter(self.model, self.read_file("detail.txt"))
        self.meaning_parser = MeaningParser()
        self.detail_parser = DetailParser()

    def run(self):
        command = self.get_command()
        while command != "quit":
            self.process(command)
            command = self.get_command()

    def get_command(self):
        command = ""
        while command == "":
            command = input("> ")
        return command

    def process(self, command):
        s = command.split()
        if len(s) == 2 and s[0] == "meaning":
            self.display(self.get_meanings(s[1]))
        elif len(s) >= 4 and s[0] == "detail":
            self.display(self.get_detail(Meaning(query=s[1], definition=" ".join(s[2:-1]), pos=s[-1])))
        else:
            print("Invalid command")

    def get_meanings(self, query: str) -> list[Meaning]:
        return self.meaning_parser.parse(self.meaning_prompter.respond({"query": query}), query)

    def get_detail(self, m: Meaning) -> DetailedMeaning:
        response = self.detail_prompter.respond({"query": m.query, "definition": m.definition, "pos": m.pos})
        return self.detail_parser.parse(response, m)

    def read_file(self, file_name: str) -> str:
        return files("synogym").joinpath("resources", file_name).read_text()

    def display(self, response: object):
        pprint(response, sort_dicts=False, width=120)


if __name__ == "__main__":
    Application().run()
