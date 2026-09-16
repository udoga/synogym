from typing import Any
from synogym.yaml_parser import YamlParser
from synogym.data_classes import Detail, Example

class DetailParser(YamlParser):
    def parse(self, text: str) -> Detail:
        return self.parse_detail(self.parse_field(self.parse_yaml(text), "detail", dict))

    def parse_detail(self, data: dict[str, Any]) -> Detail:
        return Detail(level=self.parse_field(data, "level", str),
                      description=self.parse_field(data, "description", str),
                      synonyms=self.parse_field(data, "synonyms", list),
                      history=self.parse_field(data, "history", str),
                      formations=self.parse_field(data, "formations", list),
                      examples=[self.parse_example(e) for e in self.parse_field(data, "examples", list)])

    def parse_example(self, data: dict[str, Any]) -> Example:
        return Example(sentence=self.parse_field(data, "sentence", str),
                       replacements=self.parse_field(data, "replacements", list))
