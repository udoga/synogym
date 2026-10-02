from abc import ABC, abstractmethod
from synogym.data_classes import User

class UserRepo(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def find(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def find_hashed_password_by_email(self, email: str) -> str | None:
        pass
