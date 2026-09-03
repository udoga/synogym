from typing import Any
import yaml
from synogym.meaning import Detail
from synogym.meaning import Example

class DetailParser:
    def parse(self, text: str) -> Detail:
        data: Any = yaml.safe_load(text) or {}
        detail: dict[str, Any] = data.get("detail", {})
        examples = self.parse_examples(detail)
        return Detail(examples=examples, **self.parse_fields(detail))

    def parse_fields(self, detail: dict[str, Any]) -> dict[str, Any]:
        keys = ["level", "description", "synonyms", "history", "formations"]
        return {key: detail[key] for key in keys}

    def parse_examples(self, detail: dict[str, Any]) -> list[Example]:
        examples: list[dict[str, Any]] = detail.get("examples", [])
        return [self.parse_example(example) for example in examples]

    def parse_example(self, example: dict[str, Any]) -> Example:
        sentence: str = example["sentence"]
        replacements: list[str] = example["replacements"]
        return Example(sentence=sentence, replacements=replacements)
