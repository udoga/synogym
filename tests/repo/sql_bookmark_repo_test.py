from unittest import TestCase
from synogym.data_classes import Bookmark, Meaning, User
from synogym.repo.sqlalchemy import SqlBookmarkRepo, SqlMeaningRepo, SqlUserRepo
from synogym.db_connector import DbConnector

class SqlBookmarkRepoTest(TestCase):
    def setUp(self):
        self.connection = DbConnector().connect_test()
        self.meaning_repo = SqlMeaningRepo(self.connection)
        self.user_repo = SqlUserRepo(self.connection)
        self.bookmark_repo = SqlBookmarkRepo(self.connection)
        self.meaning = self.meaning_repo.create_all([Meaning(query="happy", definition="joyful", pos="adj")])[0]
        self.user = self.user_repo.create(User("ada@example.com", "Ada", "Lovelace"))
        self.bookmark = self.bookmark_repo.create(Bookmark(self.user.id, self.meaning.id, note="", tags=""))

    def test_lists_by_user_id_and_meaning_id(self):
        self.assertEqual([self.bookmark], self.bookmark_repo.list_by(self.user.id, self.meaning.id))
        self.assertEqual([], self.bookmark_repo.list_by(self.user.id, 2))
        self.assertEqual([], self.bookmark_repo.list_by(2, self.meaning.id))

    def test_lists_by_user_id(self):
        meaning_2 = self.meaning_repo.create_all([Meaning(query="sad", definition="unhappy", pos="adj")])[0]
        user_2 = SqlUserRepo(self.connection).create(User("grace@example.com", "Grace", "Hopper"))
        bookmark_2 = self.bookmark_repo.create(Bookmark(user_id=user_2.id, meaning_id=meaning_2.id, note="", tags=""))
        self.assertEqual([self.bookmark], self.bookmark_repo.list_by(self.user.id, None))
        self.assertEqual([bookmark_2], self.bookmark_repo.list_by(user_2.id, None))

    def test_updates_and_finds_bookmark(self):
        self.bookmark.note = "Remember this one"
        self.bookmark.tags = "feeling,positive"
        self.assertEqual(self.bookmark, self.bookmark_repo.update(self.bookmark))
        self.assertEqual(self.bookmark, self.bookmark_repo.find(self.bookmark.id))
        self.assertIsNone(self.bookmark_repo.find(2))

    def test_deletes_bookmark(self):
        self.bookmark_repo.delete(self.bookmark.id)
        self.assertIsNone(self.bookmark_repo.find(self.bookmark.id))
