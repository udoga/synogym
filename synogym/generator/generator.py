from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")

class Generator(ABC, Generic[Input, Output]):
    @abstractmethod
    def generate(self, value: Input) -> Output:
        pass
