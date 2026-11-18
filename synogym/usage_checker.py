from lemminflect import getAllInflections, getAllInflectionsOOV, getInflection
from nltk import pos_tag
from nltk.tokenize import TreebankWordTokenizer

class UsageChecker:
    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()

    def get_inflections(self, query: str, pos: str) -> list[str]:
        inflections: set[str] = {query}
        if not " " in query:
            inflections.update(self._get_word_inflections(query, pos))
        elif pos == "verb":
            inflections.update(self._get_phrasal_verb_inflections(query))
        return sorted(list(inflections))

    def is_usage_example(self, text: str, inflections: list[str], pos: str) -> bool:
        if any(" " in i and i in text.lower() for i in inflections): return True
        words: list[str] = self.tokenizer.tokenize(text)
        word_tags: list[tuple[str, str]] = pos_tag(words)
        return any(word.lower() in inflections and self._matches(tag, pos) for word, tag in word_tags)

    def _get_word_inflections(self, word: str, pos: str) -> set[str]:
        result = self._get_inflection_set(getAllInflections(word, pos.upper()))
        if len(result) == 0:
            result = self._get_inflection_set(getAllInflectionsOOV(word, pos.upper()))
        return result

    def _get_inflection_set(self, tag_tuple_dict: dict[str, tuple[str]]) -> set[str]:
        return {i for tag, inflections in tag_tuple_dict.items() for i in inflections}

    def _get_phrasal_verb_inflections(self, phrasal_verb: str) -> set[str]:
        verb, rest = phrasal_verb.split(maxsplit=1)
        return {f"{i} {rest}" for i in self._get_word_inflections(verb, "verb")}

    def _matches(self, tag: str, pos: str) -> bool:
        if pos == "noun": return tag.startswith("NN")
        if pos == "verb": return tag.startswith("VB")
        return True
