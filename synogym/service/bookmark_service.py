import random
from dataclasses import replace
from synogym.data_classes import Bookmark, BookmarkedMeaning, BookmarkedMeaningExample
from synogym.highlighter import Highlighter
from synogym.repo.interface import BookmarkRepo

class BookmarkService:
    def __init__(self, repo: BookmarkRepo):
        self.repo = repo
        self.highlighter = Highlighter()

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        return self.repo.list_by(user_id, meaning_id)

    def list_bookmarked_meanings(self, user_id: int) -> list[BookmarkedMeaning]:
        meanings: list[BookmarkedMeaning] = self.repo.list_bookmarked_meanings(user_id)
        return [self._highlight_note(m) for m in meanings]

    def list_bookmarked_meaning_examples(self, user_id: int, seed: int | None = None) -> list[BookmarkedMeaningExample]:
        examples: list[BookmarkedMeaningExample] = self.repo.list_bookmarked_meaning_examples(user_id)
        examples = random.Random(seed).sample(examples, min(50, len(examples)))
        return [self._highlight_example(e) for e in examples]

    def create(self, user_id: int, meaning_id: int) -> Bookmark:
        bookmarks: list[Bookmark] = self.repo.list_by(user_id, meaning_id)
        if len(bookmarks): raise ValueError("Bookmark already exists")
        return self.repo.create(Bookmark(user_id=user_id, meaning_id=meaning_id, note="", tags=""))

    def update(self, user_id: int, bookmark_id: int, note: str, tags: str) -> Bookmark:
        return self.repo.update(replace(self._read_by(user_id, bookmark_id), note=note, tags=tags))

    def delete(self, user_id: int, bookmark_id: int):
        self._read_by(user_id, bookmark_id)
        self.repo.delete(bookmark_id)

    def _highlight_example(self, example: BookmarkedMeaningExample) -> BookmarkedMeaningExample:
        return replace(example, sentence=self.highlighter.highlight(example.sentence, example.meaning.query))

    def _highlight_note(self, meaning: BookmarkedMeaning) -> BookmarkedMeaning:
        note: str = self.highlighter.highlight(meaning.bookmark.note, meaning.query)
        return replace(meaning, bookmark=replace(meaning.bookmark, note=note))

    def _read_by(self, user_id: int, bookmark_id: int) -> Bookmark:
        bookmark = self.repo.find(bookmark_id)
        if not bookmark or bookmark.user_id != user_id: raise ValueError("Bookmark not found")
        return bookmark
