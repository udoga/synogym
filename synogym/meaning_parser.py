from typing import Any
import yaml
from synogym.meaning import Example
from synogym.meaning import FullMeaning

class MeaningParser:
    def parse(self, text: str) -> list[FullMeaning]:
        data: dict[str, Any] = yaml.safe_load(text) or {}
        meanings: list[dict[str, Any]] = data.get("meanings", [])
        return [self.parse_meaning(meaning) for meaning in meanings]

    def parse_meaning(self, meaning: dict[str, Any]) -> FullMeaning:
        keys = ["query", "definition", "part_of_speech", "level", "description", "synonyms", "history", "related"]
        fields: dict[str, Any] = {key: meaning[key] for key in keys}
        examples: list[Example] = self.parse_examples(meaning)
        return FullMeaning(examples=examples, **fields)

    def parse_examples(self, meaning: dict[str, Any]) -> list[Example]:
        examples: list[dict[str, Any]] = meaning.get("examples", [])
        return [Example(sentence=example["sentence"], replacements=example["replacements"]) for example in examples]
