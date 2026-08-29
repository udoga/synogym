from typing import Protocol

class Responder(Protocol):
    def respond(self, prompt: str) -> str:
        ...
