from synogym.data_classes import Bookmark, BookmarkedMeaning, BookmarkedMeaningExample
from synogym.repo.interface import BookmarkRepo

class MemoryBookmarkRepo(BookmarkRepo):
    def __init__(self):
        self.bookmarks: list[Bookmark] = []
        self.bookmarked_meanings: list[BookmarkedMeaning] = []
        self.bookmarked_meaning_examples: list[BookmarkedMeaningExample] = []

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        return [b for b in self.bookmarks if b.user_id == user_id and (not meaning_id or b.meaning_id == meaning_id)]

    def list_bookmarked_meanings(self, user_id: int) -> list[BookmarkedMeaning]:
        return [m for m in self.bookmarked_meanings if m.bookmark.user_id == user_id]

    def list_bookmarked_meaning_examples(self, user_id: int) -> list[BookmarkedMeaningExample]:
        return [e for e in self.bookmarked_meaning_examples if e.bookmark.user_id == user_id]

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
