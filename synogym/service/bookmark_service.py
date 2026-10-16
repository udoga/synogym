from dataclasses import replace
from synogym.data_classes import Bookmark, BookmarkWithMeaning, ExampleWithBookmark
from synogym.repo.bookmark_repo import BookmarkRepo

class BookmarkService:
    def __init__(self, repo: BookmarkRepo):
        self.repo = repo

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        return self.repo.list_by(user_id, meaning_id)

    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        return self.repo.list_with_meanings(user_id)

    def list_examples_with_bookmark(self, user_id: int) -> list[ExampleWithBookmark]:
        return self.repo.list_examples_with_bookmark(user_id)

    def read_or_create(self, user_id: int, meaning_id: int) -> Bookmark:
        bookmarks: list[Bookmark] = self.repo.list_by(user_id, meaning_id)
        if len(bookmarks): return bookmarks[0]
        return self.repo.create(Bookmark(user_id=user_id, meaning_id=meaning_id, note="", tags=""))

    def update(self, user_id: int, bookmark_id: int, note: str, tags: str) -> Bookmark:
        return self.repo.update(replace(self._read_by(user_id, bookmark_id), note=note, tags=tags))

    def delete(self, user_id: int, bookmark_id: int):
        self._read_by(user_id, bookmark_id)
        self.repo.delete(bookmark_id)

    def _read_by(self, user_id: int, bookmark_id: int) -> Bookmark:
        bookmark = self.repo.find(bookmark_id)
        if not bookmark or bookmark.user_id != user_id: raise ValueError("Bookmark not found")
        return bookmark
