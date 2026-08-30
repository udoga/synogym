import sys
from dataclasses import asdict
from importlib.resources import files
from pprint import pprint
from synogym.gpt_model import GptModel
from synogym.meaning_parser import MeaningParser
from synogym.prompter import Prompter

def read_prompt() -> str:
    return files("synogym").joinpath("resources", "lookup.txt").read_text()

def read_query(arguments: list[str]) -> str:
    if len(arguments) < 2:
        raise SystemExit("usage: python main.py <word or phrase>")
    return " ".join(arguments[1:])

def main():
    query = read_query(sys.argv)
    model = GptModel(model="gpt-5", reasoning_effort="minimal")
    prompter = Prompter(model, read_prompt())
    response = prompter.respond(query)
    meanings = MeaningParser().parse(response, query)
    pprint([asdict(meaning) for meaning in meanings], sort_dicts=False)

if __name__ == "__main__":
    main()
