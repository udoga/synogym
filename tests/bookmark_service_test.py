from unittest import TestCase
from synogym.data_classes import Bookmark
from synogym.repo.list_bookmark_repo import ListBookmarkRepo
from synogym.service.bookmark_service import BookmarkService

class BookmarkServiceTest(TestCase):
    def setUp(self):
        self.repo = ListBookmarkRepo()
        self.service = BookmarkService(self.repo)

    def test_creates_bookmark_with_empty_note_and_tags(self):
        bookmark = self.service.create(1, 2)
        self.assertEqual(Bookmark(id=1, user_id=1, meaning_id=2, note="", tags=""), bookmark)

    def test_reuses_existing_bookmark(self):
        bookmark = self.service.create(1, 2)
        self.assertEqual(bookmark, self.service.create(1, 2))
        self.assertEqual(1, len(self.repo.bookmarks))

    def test_updates_note_and_tags_for_owner(self):
        bookmark = self.service.create(1, 2)
        updated = self.service.update(1, bookmark.id, "note", "tag")
        self.assertEqual(Bookmark(id=1, user_id=1, meaning_id=2, note="note", tags="tag"), updated)

    def test_rejects_update_for_other_user(self):
        bookmark = self.service.create(1, 2)
        with self.assertRaises(ValueError):
            self.service.update(2, bookmark.id, "note", "tag")

    def test_deletes_bookmark_for_owner(self):
        bookmark = self.service.create(1, 2)
        self.service.delete(1, bookmark.id)
        self.assertIsNone(self.repo.find(bookmark.id))

    def test_rejects_delete_for_other_user(self):
        bookmark = self.service.create(1, 2)
        with self.assertRaises(ValueError):
            self.service.delete(2, bookmark.id)
