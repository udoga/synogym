from sqlalchemy import text
from sqlalchemy.engine import Connection, RowMapping
from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class SqlUserRepo(UserRepo):
    INSERT_USER_SQL = """
        INSERT INTO users (email, first_name, last_name)
        VALUES (:email, :first_name, :last_name)
        RETURNING id
    """
    INSERT_USER_WITH_PASSWORD_SQL = """
        INSERT INTO users (email, hashed_password, first_name, last_name)
        VALUES (:email, :hashed_password, :first_name, :last_name)
        RETURNING id
    """
    SELECT_USER_SQL = "SELECT id, email, first_name, last_name FROM users WHERE id = :id"
    SELECT_USER_BY_EMAIL_SQL = "SELECT id, email, first_name, last_name FROM users WHERE email = :email"
    SELECT_HASHED_PASSWORD_SQL = "SELECT hashed_password FROM users WHERE email = :email"

    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, user: User) -> User:
        user.id = self._insert_user(user)
        self.connection.commit()
        return user

    def create_with_hashed_password(self, user: User, hashed_password: str) -> User:
        values = self._get_values(user) | {"hashed_password": hashed_password}
        user.id = self.connection.execute(text(self.INSERT_USER_WITH_PASSWORD_SQL), values).scalar_one()
        self.connection.commit()
        return user

    def find(self, user_id: int) -> User | None:
        row = self._fetch_one(self.SELECT_USER_SQL, {"id": user_id})
        return self._create_user(row) if row else None

    def find_by_email(self, email: str) -> User | None:
        row = self._fetch_one(self.SELECT_USER_BY_EMAIL_SQL, {"email": email})
        return self._create_user(row) if row else None

    def find_hashed_password_by_email(self, email: str) -> str | None:
        row = self._fetch_one(self.SELECT_HASHED_PASSWORD_SQL, {"email": email})
        return row["hashed_password"] if row else None

    def _insert_user(self, user: User) -> int:
        return self.connection.execute(text(self.INSERT_USER_SQL), self._get_values(user)).scalar_one()

    def _fetch_one(self, sql: str, values: dict) -> RowMapping | None:
        return self.connection.execute(text(sql), values).mappings().fetchone()

    def _get_values(self, user: User) -> dict[str, str]:
        return {"email": user.email, "first_name": user.first_name, "last_name": user.last_name}

    def _create_user(self, row: RowMapping) -> User:
        return User(id=row["id"], email=row["email"], first_name=row["first_name"], last_name=row["last_name"])
