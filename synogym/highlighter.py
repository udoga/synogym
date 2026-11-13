import re
from nltk.corpus import wordnet

class Highlighter:
    pattern = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    def highlight(self, text: str, query: str) -> str:
        words: list[re.Match] = list(self.pattern.finditer(text))
        queries: list[str] = [m.group() for m in self.pattern.finditer(query)]
        for index in range(len(words)):
            indexes: list[int] | None = self._match(words, queries, index)
            if indexes:
                return self._wrap(text, words, indexes)
        return text

    def _match(self, words: list[re.Match], queries: list[str], index: int) -> list[int] | None:
        if not queries or not self._equal(words[index].group(), queries[0]):
            return None
        indexes = [index]
        for query in queries[1:]:
            index = self._scan(words, query, index + 1, index + 4)
            if index is None:
                return None
            indexes.append(index)
        return indexes

    def _scan(self, words: list[re.Match], query: str, start: int, end: int) -> int | None:
        for index in range(start, min(end, len(words))):
            if self._equal(words[index].group(), query):
                return index
        return None

    def _equal(self, word: str, query: str) -> bool:
        return bool(self._lemmas(word) & self._lemmas(query))

    def _lemmas(self, word: str) -> set[str]:
        value: str = word.lower()
        try:
            return {value} | set().union(*[wordnet._morphy(value, pos) for pos in ["n", "v", "a", "r"]])
        except LookupError:
            return {value}

    def _wrap(self, text: str, words: list[re.Match], indexes: list[int]) -> str:
        for start, end in reversed(self._groups(indexes)):
            first: int = words[start].start()
            last: int = words[end].end()
            text = f"{text[:first]}<em>{text[first:last]}</em>{text[last:]}"
        return text

    def _groups(self, indexes: list[int]) -> list[tuple[int, int]]:
        groups = [(indexes[0], indexes[0])]
        for index in indexes[1:]:
            start, end = groups[-1]
            groups[-1] = (start, index) if index == end + 1 else (start, end)
            if index != end + 1:
                groups.append((index, index))
        return groups
