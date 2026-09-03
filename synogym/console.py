from pprint import pprint
from synogym.core_service import CoreService

class Console:
    def __init__(self, service: CoreService):
        self.service = service

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
            self.display(self.service.list_meanings(s[1]))
        elif len(s) == 2 and s[0] == "detail":
            self.display(self.service.read_meaning_with_detail(int(s[1])))
        else:
            print("Invalid command")

    def display(self, response: object):
        pprint(response, sort_dicts=False, width=120)
