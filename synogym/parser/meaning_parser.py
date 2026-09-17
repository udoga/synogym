from typing import Any
from synogym.parser.yaml_parser import YamlParser
from synogym.data_classes import Meaning

class MeaningParser(YamlParser):
    def parse(self, text: str) -> list[Meaning]:
        return [self.parse_meaning(item) for item in self.parse_field(self.parse_yaml(text), "meanings", list)]

    def parse_meaning(self, data: Any) -> Meaning:
        self.check_type(data, dict, "Invalid meaning")
        return Meaning(query="",
                       definition=self.parse_field(data, "definition", str),
                       pos=self.parse_field(data, "pos", str))
