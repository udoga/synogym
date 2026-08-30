from typing import Any
import yaml
from synogym.meaning import Meaning

class MeaningParser:
    def parse(self, text: str, query: str) -> list[Meaning]:
        data: Any = yaml.safe_load(text) or {}
        meanings: list[Any] = data.get("meanings", []) if isinstance(data, dict) else []
        return [meaning for item in meanings if (meaning := self.parse_meaning(item, query))]

    def parse_meaning(self, data: Any, query: str) -> Meaning | None:
        if not self.is_valid(data):
            return None
        return Meaning(query=query, definition=data["definition"], pos=data["pos"])

    def is_valid(self, data: Any) -> bool:
        return isinstance(data, dict) and isinstance(data.get("definition"), str) and isinstance(data.get("pos"), str)
