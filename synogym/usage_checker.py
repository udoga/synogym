from lemminflect import getAllInflections
from nltk import pos_tag
from nltk.tokenize import TreebankWordTokenizer

class UsageChecker:
    def __init__(self):
        self.tokenizer = TreebankWordTokenizer()

    def create_inflections(self, query: str, pos: str) -> list[str]:
        if self._is_phrasal_verb(pos, query):
            return self._inflect_phrasal_verb(query)
        return self._inflect_word(pos, query)

    def is_usage_example(self, text: str, inflections: list[str], pos: str) -> bool:
        if any(" " in i and i in text.lower() for i in inflections): return True
        words: list[str] = self.tokenizer.tokenize(text)
        word_tags: list[tuple[str, str]] = pos_tag(words)
        return any(word.lower() in inflections and self._matches(tag, pos) for word, tag in word_tags)

    def _inflect_word(self, pos, word) -> list[str]:
        tag_inflections: dict[str, tuple[str, ...]] = getAllInflections(word)
        inflections = {i for t, inflections in tag_inflections.items() for i in inflections if self._matches(t, pos)}
        inflections.add(word)
        return sorted(list(inflections))

    def _is_phrasal_verb(self, pos, query):
        return " " in query and pos == "verb"

    def _inflect_phrasal_verb(self, query: str) -> list[str]:
        verb, rest = query.split(maxsplit=1)
        return [f"{i} {rest}" for i in self._inflect_word("verb", verb)]

    def _matches(self, tag: str, pos: str) -> bool:
        return ((pos == "noun" and tag.startswith("NN"))
                or (pos == "verb" and tag.startswith("VB"))
                or (pos == "adjective" and tag.startswith("JJ"))
                or (pos == "adverb" and tag.startswith("RB"))
                or (pos == "preposition" and tag == "IN")
                or (pos == "conjunction" and tag == "CC")
                or (pos == "interjection" and tag == "UH")
                or (pos in ["determiner", "article", "det"] and tag == "DT"))
