import sqlite3
from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class SqlUserRepo(UserRepo):
    INSERT_USER_SQL = "INSERT INTO users (email, first_name, last_name) VALUES (?, ?, ?)"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(self, user: User) -> User:
        cursor = self.connection.execute(self.INSERT_USER_SQL, self._get_values(user))
        self.connection.commit()
        user.id = cursor.lastrowid
        return user

    def _get_values(self, user: User) -> tuple[str, str, str]:
        return user.email, user.first_name, user.last_name
