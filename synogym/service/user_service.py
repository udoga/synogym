from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo
from werkzeug.exceptions import Unauthorized
from werkzeug.security import check_password_hash

class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def find_user(self, user_id: int) -> User | None:
        return self.repo.find(user_id)

    def find_or_create_user(self, new_user: User) -> User:
        user = self.repo.find_by_email(new_user.email)
        return user if user else self.repo.create(new_user)

    def sign_in(self, email: str, password: str) -> User:
        user = self.repo.find_by_email(email)
        hashed_password = self.repo.find_hashed_password_by_email(email)
        if user and hashed_password and check_password_hash(hashed_password, password):
            return user
        raise Unauthorized("Invalid email or password")
