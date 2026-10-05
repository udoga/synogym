from synogym.data_classes import User
from synogym.repo.user_repo import UserRepo
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized
from werkzeug.security import check_password_hash, generate_password_hash

class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def find_user(self, user_id: int) -> User | None:
        return self.repo.find(user_id)

    def find_or_create_user(self, new_user: User) -> User:
        user = self.repo.find_by_email(new_user.email)
        return user if user else self.repo.create(new_user)

    def sign_up(self, email: str, password: str) -> User:
        email = self._validate_credentials(email, password)
        if self.repo.find_by_email(email):
            raise Conflict("An account with this email already exists")
        return self._create_password_user(email, password)

    def sign_in(self, email: str, password: str) -> User:
        user = self.repo.find_by_email(email)
        hashed_password = self.repo.find_hashed_password_by_email(email)
        if user and hashed_password and check_password_hash(hashed_password, password):
            return user
        raise Unauthorized("Invalid email or password")

    def _validate_credentials(self, email: str, password: str) -> str:
        email = email.strip().lower()
        if not email or not password:
            raise BadRequest("Email and password are required")
        return email

    def _create_password_user(self, email: str, password: str) -> User:
        user = User(email, "", "")
        return self.repo.create_with_hashed_password(user, generate_password_hash(password))
