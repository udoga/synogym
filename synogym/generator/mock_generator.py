from typing import TypeVar
from synogym.generator import Generator

Input = TypeVar("Input")
Output = TypeVar("Output")

class MockGenerator(Generator[Input, Output]):
    def __init__(self, output: Output | None = None):
        self.output = output
        self.value: Input | None = None

    def generate(self, value: Input) -> Output:
        self.value = value
        return self.output
