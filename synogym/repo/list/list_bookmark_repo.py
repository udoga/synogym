from synogym.data_classes import Bookmark, BookmarkWithMeaning, Meaning, ExampleWithBookmark
from synogym.repo.bookmark_repo import BookmarkRepo

class ListBookmarkRepo(BookmarkRepo):
    def __init__(self):
        self.bookmarks: list[Bookmark] = []
        self.examples_with_bookmark: list[ExampleWithBookmark] = []

    def list_by(self, user_id: int, meaning_id: int | None) -> list[Bookmark]:
        return [b for b in self.bookmarks if b.user_id == user_id and (not meaning_id or b.meaning_id == meaning_id)]

    def list_with_meanings(self, user_id: int) -> list[BookmarkWithMeaning]:
        bookmarks = [bookmark for bookmark in self.bookmarks if bookmark.user_id == user_id]
        return [self._create_bookmark_with_meaning(bookmark) for bookmark in bookmarks]

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

    def _create_bookmark_with_meaning(self, bookmark: Bookmark) -> BookmarkWithMeaning:
        meaning = Meaning(id=bookmark.meaning_id, query="", definition="", pos="")
        return BookmarkWithMeaning(id=bookmark.id, user_id=bookmark.user_id, meaning_id=bookmark.meaning_id,
                                   note=bookmark.note, tags=bookmark.tags, meaning=meaning)
