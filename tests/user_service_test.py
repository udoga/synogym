from unittest import TestCase
from synogym.data_classes import User
from synogym.repo.list_user_repo import ListUserRepo
from synogym.service.user_service import UserService
from werkzeug.exceptions import Conflict, Unauthorized
from werkzeug.security import generate_password_hash

class UserServiceTest(TestCase):
    def setUp(self):
        self.repo = ListUserRepo()
        self.service = UserService(self.repo)

    def test_finds_or_creates_user(self):
        first_user = self.service.find_or_create_user(User("ada@example.com", "Ada", "Lovelace"))
        second_user = self.service.find_or_create_user(User("ada@example.com", "Augusta", "Byron"))
        self.assertEqual(first_user, second_user)
        self.assertEqual([first_user], self.repo.users)

    def test_signs_in_user_with_password(self):
        user = User("ada@example.com", "Ada", "Lovelace")
        self.repo.create(user)
        self.repo.hashed_passwords[user.email] = generate_password_hash("secret")
        self.assertEqual(user, self.service.sign_in("ada@example.com", "secret"))

    def test_rejects_user_with_wrong_password(self):
        user = User("ada@example.com", "Ada", "Lovelace")
        self.repo.create(user)
        self.repo.hashed_passwords[user.email] = generate_password_hash("secret")
        with self.assertRaises(Unauthorized):
            self.service.sign_in("ada@example.com", "wrong")

    def test_signs_up_user_with_email_and_password(self):
        user = self.service.sign_up("ada@example.com", "secret")
        self.assertEqual(User(id=1, email="ada@example.com", first_name="", last_name=""), user)
        self.assertTrue(self.service.sign_in("ada@example.com", "secret"))

    def test_rejects_sign_up_for_existing_email(self):
        self.service.sign_up("ada@example.com", "secret")
        with self.assertRaises(Conflict):
            self.service.sign_up("ada@example.com", "secret")
