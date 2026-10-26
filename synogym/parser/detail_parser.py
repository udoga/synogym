from typing import Any
from synogym.parser import YamlParser
from synogym.data_classes import Detail

class DetailParser(YamlParser):
    def parse(self, text: str) -> Detail:
        return self.parse_detail(self.parse_field(self.parse_yaml(text), "detail", dict))

    def parse_detail(self, data: dict[str, Any]) -> Detail:
        return Detail(level=self.parse_field(data, "level", str),
                      description=self.parse_field(data, "description", str),
                      synonyms=self.parse_comma_separated_list(data, "synonyms"),
                      history=self.parse_field(data, "history", str),
                      formations=self.parse_comma_separated_list(data, "formations"))
