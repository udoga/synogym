import sqlite3
from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class SqlUserRepo(UserRepo):
    INSERT_USER_SQL = "INSERT INTO users (email, first_name, last_name) VALUES (?, ?, ?)"
    SELECT_USER_SQL = "SELECT id, email, first_name, last_name FROM users WHERE id = ?"
    SELECT_USER_BY_EMAIL_SQL = "SELECT id, email, first_name, last_name FROM users WHERE email = ?"

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create(self, user: User) -> User:
        cursor = self.connection.execute(self.INSERT_USER_SQL, self._get_values(user))
        self.connection.commit()
        user.id = cursor.lastrowid
        return user

    def find(self, user_id: int) -> User | None:
        row = self.connection.execute(self.SELECT_USER_SQL, (user_id,)).fetchone()
        return self._create_user(row) if row else None

    def find_by_email(self, email: str) -> User | None:
        row = self.connection.execute(self.SELECT_USER_BY_EMAIL_SQL, (email,)).fetchone()
        return self._create_user(row) if row else None

    def _get_values(self, user: User) -> tuple[str, str, str]:
        return user.email, user.first_name, user.last_name

    def _create_user(self, row: sqlite3.Row) -> User:
        return User(id=row["id"], email=row["email"], first_name=row["first_name"], last_name=row["last_name"])
