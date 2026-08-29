from unittest import TestCase
from synogym.prompter import Prompter

class FakeResponder:
    def __init__(self):
        self.prompt = ""

    def respond(self, prompt: str) -> str:
        self.prompt = prompt
        return "result"

class PrompterTest(TestCase):
    def test_prompter_inserts_query(self):
        responder = FakeResponder()
        prompter = Prompter(responder, "Query: {query}")
        result = prompter.respond("happy")
        self.assertEqual("Query: happy", responder.prompt)
        self.assertEqual("result", result)
