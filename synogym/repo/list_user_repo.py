from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class ListUserRepo(UserRepo):
    def __init__(self):
        self.users: list[User] = []

    def create(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)
        return user

    def find(self, user_id: int) -> User | None:
        return next((user for user in self.users if user.id == user_id), None)

    def find_by_email(self, email: str) -> User | None:
        return next((user for user in self.users if user.email == email), None)
