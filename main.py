from importlib.resources import files
from synogym.gpt_model import GptModel
from synogym.prompter import Prompter

model = GptModel()
prompt = files("synogym").joinpath("resources", "prompt.txt").read_text()
prompter = Prompter(model, prompt)
result = prompter.respond("happy")
print(result)
