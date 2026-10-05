from pathlib import Path
from unittest import TestCase
from synogym.data_classes import Bookmark, BookmarkWithMeaning, Meaning, User
from synogym.repo.db.sql_bookmark_repo import SqlBookmarkRepo
from synogym.repo.db.sql_meaning_repo import SqlMeaningRepo
from synogym.repo.db.sql_user_repo import SqlUserRepo
from synogym.db_connector import DbConnector

class SqlBookmarkRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "resources" / "sqlite-schema.sql")
        self.connection = DbConnector().connect({"type": "sqlite", "uri": ":memory:", "sql_paths": [self.sql_path]})
        meanings = [Meaning(query="happy", definition="joyful", pos="adj")]
        self.meaning = SqlMeaningRepo(self.connection).create_all(meanings)[0]
        self.user = SqlUserRepo(self.connection).create(User("ada@example.com", "Ada", "Lovelace"))
        self.repo = SqlBookmarkRepo(self.connection)

    def test_creates_finds_and_updates_bookmark(self):
        bookmark = self.repo.create(Bookmark(user_id=self.user.id, meaning_id=self.meaning.id, note="", tags=""))
        self.assertEqual([bookmark], self.repo.find_by_user_and_meaning(self.user.id, self.meaning.id))
        bookmark.note = "Remember this one"
        bookmark.tags = "feeling,positive"
        self.assertEqual(bookmark, self.repo.update(bookmark))
        self.assertEqual(bookmark, self.repo.find(bookmark.id))

    def test_returns_none_for_missing_bookmark(self):
        self.assertEqual([], self.repo.find_by_user_and_meaning(self.user.id, self.meaning.id))
        self.assertIsNone(self.repo.find(123))

    def test_lists_bookmarks_with_meanings_for_user(self):
        bookmark = self.repo.create(Bookmark(user_id=self.user.id, meaning_id=self.meaning.id, note="n", tags="t"))
        expected = [BookmarkWithMeaning(id=bookmark.id, user_id=self.user.id, meaning_id=self.meaning.id,
                                        note="n", tags="t", meaning=self.meaning)]
        self.assertEqual(expected, self.repo.list_with_meanings(self.user.id))

    def test_deletes_bookmark(self):
        bookmark = self.repo.create(Bookmark(user_id=self.user.id, meaning_id=self.meaning.id, note="", tags=""))
        self.repo.delete(bookmark.id)
        self.assertIsNone(self.repo.find(bookmark.id))
