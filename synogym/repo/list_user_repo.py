from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class ListUserRepo(UserRepo):
    def __init__(self):
        self.users: list[User] = []

    def create(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)
        return user
