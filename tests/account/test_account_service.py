import unittest
from unittest.mock import Mock

from account.application.account_service import AccountService, Account
from shared import exceptions
from ..mocks import mock_app_context


def mock_account():
    return Account(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="12345679Ab!")


def mock_account_repository(mock, account = None):
    mock.save.return_value = None
    mock.find_by_id.return_value = account
    mock.find_by_email.return_value = account
    return mock


class TestCreateAccount(unittest.TestCase):

    def test_create_account(self):
        mock = Mock()
        mock = mock_account_repository(mock)
        mock = mock_app_context(mock, None, None)

        class CreateAccountDto:
            first_name = "John"
            last_name = "Doe"
            email = "john.doe@test.com"
            password = "12345679Ab!"

        account_service = AccountService(mock, mock)

        account = account_service.create_account(CreateAccountDto())
        self.assertIsNotNone(account)
        self.assertEqual(account.first_name, "John")
        self.assertEqual(account.last_name, "Doe")
        self.assertEqual(account.email, "john.doe@test.com")
        self.assertEqual(account.account_type, "user")
    
    def test_create_account_with_invalid_password(self):
        mock = Mock()
        mock = mock_account_repository(mock)
        mock = mock_app_context(mock, None, None)

        class CreateAccountDto:
            first_name = "John"
            last_name = "Doe"
            email = "john.doe@test.com"
            password = "12345679"
        
        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.InvalidPassword):
            account_service.create_account(CreateAccountDto())

    def test_create_account_with_existing_email(self):
        mock = Mock()
        mock = mock_account_repository(mock, {"email": "john.doe@test.com"})
        mock = mock_app_context(mock, None, None)

        class CreateAccountDto:
            first_name = "John"
            last_name = "Doe"
            email = "john.doe@test.com"
            password = "12345679Ab!"

        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.AlreadyExists):
            account_service.create_account(CreateAccountDto())


class TestGetAccount(unittest.TestCase):

    def test_user_gets_same_account(self):
        base_account = mock_account()
        mock = Mock()
        mock = mock_account_repository(mock, base_account)
        mock = mock_app_context(mock, base_account.id, "user")

        account_service = AccountService(mock, mock)

        account = account_service.get_account(base_account.id)
        self.assertIsNotNone(account)
        self.assertEqual(account.id, base_account.id)

    def test_admin_gets_any_account(self):
        base_account = mock_account()
        search_account = mock_account()
        mock = Mock()
        mock = mock_account_repository(mock, search_account)
        mock = mock_app_context(mock, base_account.id, "admin")

        account_service = AccountService(mock, mock)

        account = account_service.get_account(search_account.id)
        self.assertIsNotNone(account)
        self.assertEqual(search_account.id, account.id)
    
    def test_user_gets_other_account(self):
        user_account = mock_account()
        search_account = mock_account()
        mock = Mock()
        mock = mock_account_repository(mock, search_account)
        mock = mock_app_context(mock, user_account.id, "user")

        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.Unauthorized):
            account_service.get_account(search_account.id)
    
    def test_get_account_not_found(self):
        mock = Mock()
        mock = mock_account_repository(mock, None)
        mock = mock_app_context(mock, None, "admin")

        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.NotFound):
            account_service.get_account("1234")


class TestLogin(unittest.TestCase):

    def test_login(self):
        base_account = mock_account()
        mock = Mock()
        mock = mock_account_repository(mock, base_account)
        mock = mock_app_context(mock, None, None)

        class LoginDto:
            email: str = base_account.email
            password: str = base_account.password

        account_service = AccountService(mock, mock)

        account = account_service.authenticate(LoginDto())
        self.assertIsNotNone(account)
        self.assertEqual(account, base_account)

    def test_login_with_invalid_password(self):
        base_account = mock_account()
        mock = Mock()
        mock = mock_account_repository(mock, base_account)
        mock = mock_app_context(mock, None, None)

        class LoginDto:
            email: str = base_account.email
            password: str = "12345679"

        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.InvalidCredentials):
            account_service.authenticate(LoginDto())

    def test_login_with_invalid_email(self):
        mock = Mock()
        mock = mock_account_repository(mock, None)
        mock = mock_app_context(mock, None, None)

        class LoginDto:
            email: str = "otheremail@test.com"
            password: str = "12345679Ab!"

        account_service = AccountService(mock, mock)

        with self.assertRaises(exceptions.InvalidCredentials):
            account_service.authenticate(LoginDto())
    