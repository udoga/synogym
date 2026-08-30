from synogym.responder import Responder

class Prompter:
    def __init__(self, model: Responder, prompt: str):
        self.model = model
        self.prompt = prompt

    def respond(self, values: dict[str, str]) -> str:
        prompt = self.prompt.format(**values)
        return self.model.respond(prompt)
