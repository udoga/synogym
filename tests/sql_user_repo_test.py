from pathlib import Path
from unittest import TestCase
from synogym.data_classes import User
from synogym.repo.sql_user_repo import SqlUserRepo
from synogym.sqlite_connector import SqliteConnector

class SqlUserRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")
        self.connection = SqliteConnector().connect(":memory:", self.sql_path)
        self.repo = SqlUserRepo(self.connection)

    def test_creates_user(self):
        user = User(email="ada@example.com", first_name="Ada", last_name="Lovelace")
        self.assertEqual(user, self.repo.create(user))
        self.assertEqual(1, user.id)
