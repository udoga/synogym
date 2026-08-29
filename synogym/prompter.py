from synogym.responder import Responder

class Prompter(Responder):
    def __init__(self, model: Responder, prompt: str):
        self.model = model
        self.prompt = prompt

    def respond(self, query: str) -> str:
        prompt = self.prompt.replace("{query}", query)
        return self.model.respond(prompt)
