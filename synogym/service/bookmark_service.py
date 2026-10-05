from synogym.data_classes import Bookmark, BookmarkWithMeaning
from synogym.repo.bookmark_repo import BookmarkRepo

class BookmarkService:
    def __init__(self, repo: BookmarkRepo):
        self.repo = repo

    def list_by_user_and_meaning(self, user_id: int, meaning_id: int) -> list[Bookmark]:
        return self.repo.find_by_user_and_meaning(user_id, meaning_id)

    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        return self.repo.list_with_meanings(user_id)

    def create(self, user_id: int, meaning_id: int) -> Bookmark:
        bookmarks: list[Bookmark] = self.repo.find_by_user_and_meaning(user_id, meaning_id)
        if len(bookmarks): return bookmarks[0]
        return self.repo.create(Bookmark(user_id=user_id, meaning_id=meaning_id, note="", tags=""))

    def update(self, user_id: int, bookmark_id: int, note: str, tags: str) -> Bookmark:
        bookmark = self._find_user_bookmark(user_id, bookmark_id)
        bookmark.note = note
        bookmark.tags = tags
        return self.repo.update(bookmark)

    def delete(self, user_id: int, bookmark_id: int):
        self._find_user_bookmark(user_id, bookmark_id)
        self.repo.delete(bookmark_id)

    def _find_user_bookmark(self, user_id: int, bookmark_id: int) -> Bookmark:
        bookmark = self.repo.find(bookmark_id)
        if not bookmark or bookmark.user_id != user_id: raise ValueError("Bookmark not found")
        return bookmark
