from unittest import TestCase
from synogym.repo.list_user_repo import ListUserRepo
from synogym.service.user_service import UserService

class UserServiceTest(TestCase):
    def setUp(self):
        self.repo = ListUserRepo()
        self.service = UserService(self.repo)

    def test_creates_user(self):
        user = self.service.create_user("ada@example.com", "Ada", "Lovelace")
        self.assertEqual("ada@example.com", user.email)
        self.assertEqual("Ada", user.first_name)
        self.assertEqual("Lovelace", user.last_name)
        self.assertEqual([user], self.repo.users)
