from typing import Any
from synogym.parser import YamlParser
from synogym.data_classes import Example

class ExampleParser(YamlParser):
    def parse(self, text: str) -> list[Example]:
        return [self.parse_example(e) for e in self.parse_field(self.parse_yaml(text), "examples", list)]

    def parse_example(self, data: dict[str, Any]) -> Example:
        return Example(sentence=self.parse_field(data, "sentence", str),
                       replacements=self.parse_comma_separated_list(data, "replacements"))
