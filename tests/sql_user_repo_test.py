from pathlib import Path
from unittest import TestCase
from sqlalchemy import text
from synogym.data_classes import User
from synogym.repo.db.sql_user_repo import SqlUserRepo
from synogym.db_connector import DbConnector

class SqlUserRepoTest(TestCase):
    def setUp(self):
        self.sql_path = str(Path(__file__).resolve().parent.parent / "sqlite-schema.sql")
        self.connection = DbConnector().connect({"type": "sqlite", "uri": ":memory:", "sql_paths": [self.sql_path]})
        self.repo = SqlUserRepo(self.connection)

    def test_creates_user(self):
        user = User(email="ada@example.com", first_name="Ada", last_name="Lovelace")
        self.assertEqual(user, self.repo.create(user))
        self.assertEqual(1, user.id)

    def test_finds_user(self):
        user = self.repo.create(User(email="ada@example.com", first_name="Ada", last_name="Lovelace"))
        self.assertEqual(user, self.repo.find(user.id))
        self.assertEqual(user, self.repo.find_by_email(user.email))

    def test_finds_hashed_password(self):
        user = self.repo.create(User(email="ada@example.com", first_name="Ada", last_name="Lovelace"))
        self.connection.execute(text("UPDATE users SET hashed_password = :hash WHERE email = :email"),
                                {"hash": "hash", "email": user.email})
        self.assertEqual("hash", self.repo.find_hashed_password_by_email(user.email))

    def test_creates_user_with_hashed_password(self):
        user = self.repo.create_with_hashed_password(User("ada@example.com", "", ""), "hash")
        self.assertEqual(user, self.repo.find_by_email("ada@example.com"))
        self.assertEqual("hash", self.repo.find_hashed_password_by_email("ada@example.com"))
