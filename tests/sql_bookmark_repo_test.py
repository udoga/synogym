from pathlib import Path
from unittest import TestCase
from synogym.data_classes import Bookmark, Meaning, User
from synogym.repo.sql_bookmark_repo import SqlBookmarkRepo
from synogym.repo.sql_meaning_repo import SqlMeaningRepo
from synogym.repo.sql_user_repo import SqlUserRepo
from synogym.sqlite_connector import SqliteConnector

class SqlBookmarkRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")
        self.connection = SqliteConnector().connect(":memory:", [self.sql_path])
        meanings = [Meaning(query="happy", definition="joyful", pos="adj")]
        self.meaning = SqlMeaningRepo(self.connection).create_all(meanings)[0]
        self.user = SqlUserRepo(self.connection).create(User("ada@example.com", "Ada", "Lovelace"))
        self.repo = SqlBookmarkRepo(self.connection)

    def test_creates_finds_and_updates_bookmark(self):
        bookmark = self.repo.create(Bookmark(user_id=self.user.id, meaning_id=self.meaning.id, note="", tags=""))
        self.assertEqual(bookmark, self.repo.find_by_user_and_meaning(self.user.id, self.meaning.id))
        bookmark.note = "Remember this one"
        bookmark.tags = "feeling,positive"
        self.assertEqual(bookmark, self.repo.update(bookmark))
        self.assertEqual(bookmark, self.repo.find(bookmark.id))

    def test_returns_none_for_missing_bookmark(self):
        self.assertIsNone(self.repo.find_by_user_and_meaning(self.user.id, self.meaning.id))
        self.assertIsNone(self.repo.find(123))

    def test_deletes_bookmark(self):
        bookmark = self.repo.create(Bookmark(user_id=self.user.id, meaning_id=self.meaning.id, note="", tags=""))
        self.repo.delete(bookmark.id)
        self.assertIsNone(self.repo.find(bookmark.id))
