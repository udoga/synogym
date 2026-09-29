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

    def test_finds_or_creates_user(self):
        first_user = self.service.find_or_create_user("ada@example.com", "Ada", "Lovelace")
        second_user = self.service.find_or_create_user("ada@example.com", "Augusta", "Byron")
        self.assertEqual(first_user, second_user)
        self.assertEqual([first_user], self.repo.users)
