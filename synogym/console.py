from pprint import pprint
from synogym.meaning import Meaning
from synogym.api import Api

class Console:
    def __init__(self, api: Api):
        self.api = api

    def run(self):
        command = self.get_command()
        while command != "quit":
            self.process(command)
            command = self.get_command()

    def get_command(self) -> str:
        command = ""
        while command == "":
            command = input("> ")
        return command

    def process(self, command: str):
        s = command.split()
        if len(s) == 2 and s[0] == "meaning":
            self.display(self.api.get_meanings(s[1]))
        elif len(s) >= 4 and s[0] == "detail":
            self.display(self.api.get_detail(Meaning(query=s[1], definition=" ".join(s[2:-1]), pos=s[-1])))
        else:
            print("Invalid command")

    def display(self, response: object):
        pprint(response, sort_dicts=False, width=120)
