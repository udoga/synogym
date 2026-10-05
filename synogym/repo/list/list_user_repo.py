from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class ListUserRepo(UserRepo):
    def __init__(self):
        self.users: list[User] = []
        self.hashed_passwords: dict[str, str] = {}

    def create(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)
        return user

    def create_with_hashed_password(self, user: User, hashed_password: str) -> User:
        self.hashed_passwords[user.email] = hashed_password
        return self.create(user)

    def find(self, user_id: int) -> User | None:
        return next((user for user in self.users if user.id == user_id), None)

    def find_by_email(self, email: str) -> User | None:
        return next((user for user in self.users if user.email == email), None)

    def find_hashed_password_by_email(self, email: str) -> str | None:
        return self.hashed_passwords.get(email)
