from unittest import TestCase
from synogym.prompter import Prompter

class FakeResponder:
    def __init__(self):
        self.prompt = ""

    def respond(self, prompt: str) -> str:
        self.prompt = prompt
        return "result"

class PrompterTest(TestCase):
    def test_prompter_formats_values(self):
        responder = FakeResponder()
        prompter = Prompter(responder, "Query: {query}, POS: {pos}")
        result = prompter.respond({"query": "happy", "pos": "adjective"})
        self.assertEqual("Query: happy, POS: adjective", responder.prompt)
        self.assertEqual("result", result)
