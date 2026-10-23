from synogym.data_classes import Bookmark, ExampleWithBookmark, MeaningWithBookmark
from synogym.repo.interface import BookmarkRepo

class MemoryBookmarkRepo(BookmarkRepo):
    def __init__(self):
        self.bookmarks: list[Bookmark] = []
        self.meanings_with_bookmark: list[MeaningWithBookmark] = []
        self.examples_with_bookmark: list[ExampleWithBookmark] = []

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        return [b for b in self.bookmarks if b.user_id == user_id and (not meaning_id or b.meaning_id == meaning_id)]

    def list_meanings_with_bookmark(self, user_id: int) -> list[MeaningWithBookmark]:
        return [m for m in self.meanings_with_bookmark if m.bookmark.user_id == user_id]

    def list_examples_with_bookmark(self, user_id: int) -> list[ExampleWithBookmark]:
        return [e for e in self.examples_with_bookmark if e.bookmark.user_id == user_id]

    def create(self, bookmark: Bookmark) -> Bookmark:
        bookmark.id = len(self.bookmarks) + 1
        self.bookmarks.append(bookmark)
        return bookmark

    def find(self, bookmark_id: int) -> Bookmark | None:
        return next((bookmark for bookmark in self.bookmarks if bookmark.id == bookmark_id), None)

    def update(self, bookmark: Bookmark) -> Bookmark:
        existing = self.find(bookmark.id)
        if not existing: raise ValueError("Bookmark not found")
        existing.note = bookmark.note
        existing.tags = bookmark.tags
        return existing

    def delete(self, bookmark_id: int):
        self.bookmarks = [bookmark for bookmark in self.bookmarks if bookmark.id != bookmark_id]
