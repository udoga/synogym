from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo

class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def create_user(self, email: str, first_name: str, last_name: str) -> User:
        user = User(email=email, first_name=first_name, last_name=last_name)
        return self.repo.create(user)
