from synogym.data_classes import Bookmark
from synogym.repo.bookmark_repo import BookmarkRepo

class ListBookmarkRepo(BookmarkRepo):
    def __init__(self):
        self.bookmarks: list[Bookmark] = []

    def create(self, bookmark: Bookmark) -> Bookmark:
        bookmark.id = len(self.bookmarks) + 1
        self.bookmarks.append(bookmark)
        return bookmark

    def find(self, bookmark_id: int) -> Bookmark | None:
        return next((bookmark for bookmark in self.bookmarks if bookmark.id == bookmark_id), None)

    def find_by_user_and_meaning(self, user_id: int, meaning_id: int) -> Bookmark | None:
        return next((bookmark for bookmark in self.bookmarks if self._matches(bookmark, user_id, meaning_id)), None)

    def update(self, bookmark: Bookmark) -> Bookmark:
        existing = self.find(bookmark.id)
        if not existing: raise ValueError("Bookmark not found")
        existing.note = bookmark.note
        existing.tags = bookmark.tags
        return existing

    def delete(self, bookmark_id: int):
        self.bookmarks = [bookmark for bookmark in self.bookmarks if bookmark.id != bookmark_id]

    def _matches(self, bookmark: Bookmark, user_id: int, meaning_id: int) -> bool:
        return bookmark.user_id == user_id and bookmark.meaning_id == meaning_id
