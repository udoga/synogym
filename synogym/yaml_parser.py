from typing import Any
import yaml

class YamlParser:
    def parse_yaml(self, text: str):
        data: Any = yaml.safe_load(text)
        self.check_type(data, dict, "Invalid data")
        return data

    def parse_field(self, data: dict, field: str, cls):
        assert field in data, "Missing " + field
        self.check_type(data[field], cls, "Invalid " + field)
        return data[field]

    def check_type(self, data: Any, cls, message: str):
        if not isinstance(data, cls):
            raise TypeError(message)
