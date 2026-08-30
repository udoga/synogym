class Formatter:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def format(self, values: dict[str, str]) -> str:
        return self.prompt.format(**values)
