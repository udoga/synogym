from typing import TypeVar
from synogym.generator.generator import Generator

Input = TypeVar("Input")
Output = TypeVar("Output")

class MockGenerator(Generator[Input, Output]):
    def __init__(self, output: Output | None = None):
        self.output = output

    def generate(self, value: Input) -> Output:
        return self.output
