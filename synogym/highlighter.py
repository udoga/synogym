import re
from nltk.corpus import wordnet

class Highlighter:
    pattern = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    def highlight(self, text: str, query: str) -> str:
        words: list[re.Match] = list(self.pattern.finditer(text))
        queries: list[str] = self._tokenize(query)
        indexes: list[int] = self._find(words, queries)
        spans: list[tuple[int, int]] = self._merge(words, indexes)
        return self._wrap(text, spans) if spans else text

    def _tokenize(self, text: str) -> list[str]:
        return [m.group() for m in self.pattern.finditer(text)]

    def _find(self, words: list[re.Match], queries: list[str]) -> list[int]:
        for index in range(len(words)):
            indexes: list[int] = self._match(words, queries, index)
            if indexes:
                return indexes
        return []

    def _match(self, words: list[re.Match], queries: list[str], index: int) -> list[int]:
        if not queries or not self._match_word(words[index].group(), queries[0]):
            return []
        indexes = [index]
        for query in queries[1:]:
            index = self._next(words, query, index)
            if index is None:
                return []
            indexes.append(index)
        return indexes

    def _next(self, words: list[re.Match], query: str, index: int) -> int | None:
        for i in range(index + 1, min(index + 4, len(words))):
            if self._match_word(words[i].group(), query):
                return i
        return None

    def _match_word(self, word: str, query: str) -> bool:
        return bool(self._lemmatize(word) & self._lemmatize(query))

    def _lemmatize(self, word: str) -> set[str]:
        value: str = word.lower()
        lemmas: set[str] = {value} | set().union(*[wordnet._morphy(value, pos) for pos in ["n", "v", "a", "r"]])
        if value.endswith("ed"):
            stem: str = value[:-2]
            if len(stem) > 1 and stem[-1] == stem[-2]:
                lemmas.add(stem[:-1])
        return lemmas

    def _merge(self, words: list[re.Match], indexes: list[int]) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        previous = -2
        for index in indexes:
            start, end = words[index].span()
            if index == previous + 1:
                spans[-1] = (spans[-1][0], end)
            else:
                spans.append((start, end))
            previous = index
        return spans

    def _wrap(self, text: str, spans: list[tuple[int, int]]) -> str:
        for start, end in reversed(spans):
            text = f"{text[:start]}<em>{text[start:end]}</em>{text[end:]}"
        return text
