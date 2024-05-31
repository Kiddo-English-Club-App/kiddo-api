import unittest
import bcrypt

from account.domain.password import Password
from shared import exceptions


class TestPassword(unittest.TestCase):

    def test_password_with_plain_text(self):
        password = Password("Password123@")
        self.assertIsNotNone(password.hashed)
        self.assertEqual(password, "Password123@")

    def test_password_with_hashed_text(self):
        hashed = bcrypt.hashpw("Password123@".encode(), bcrypt.gensalt())
        hashed = hashed.decode()
        password = Password(hashed, True)
        self.assertEqual(password, "Password123@")

    def test_password_length_validation(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*8 characters(.)*"):
            Password("passw")

    def test_password_with_digits(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*digit(.)*"):
            Password("password")

    def test_password_with_uppercase_text(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*uppercase(.)*"):
            Password("password1")

    def test_password_with_lowercase_text(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*lowercase(.)*"):
            Password("PASSWORD1")

    def test_password_with_special_character(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*special character(.)*"):
            Password("Password1")
