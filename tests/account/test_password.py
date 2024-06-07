import unittest
import bcrypt

from account.domain.password import PasswordStr
from shared import exceptions


class TestPasswordStr(unittest.TestCase):

    def test_password_with_plain_text(self):
        password = PasswordStr("Password123@")
        self.assertEqual(password, "Password123@")

    def test_password_with_hashed_text(self):
        hashed = bcrypt.hashpw("Password123@".encode(), bcrypt.gensalt())
        hashed = hashed.decode()
        password = PasswordStr(hashed, True)
        self.assertEqual(password, "Password123@")

    def test_password_length_validation(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*8 characters(.)*"):
            PasswordStr("passw")

    def test_password_with_digits(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*digit(.)*"):
            PasswordStr("password")

    def test_password_with_uppercase_text(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*uppercase(.)*"):
            PasswordStr("password1")

    def test_password_with_lowercase_text(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*lowercase(.)*"):
            PasswordStr("PASSWORD1")

    def test_password_with_special_character(self):
        with self.assertRaisesRegex(exceptions.InvalidPassword, "(.)*special character(.)*"):
            PasswordStr("Password1")