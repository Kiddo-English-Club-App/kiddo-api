# Account service
# This module provides the service layer for account management, encapsulating business logic 
# for account operations such as creation, and ensuring separation of concerns.
from account.domain.account import Account, AccountType
from account.domain.account_repository import IAccountRepository
from shared.id import Id
from shared.exceptions import InvalidCredentials, NotFound, AlreadyExists
from shared.app_context import AppContext
from shared.permissions import AdminOrSameUserPermission, validate
from . import dto


class AccountService:
    """
    AccountService provides a high-level interface for account-related operations.
    It interacts with the account repository to persist account data and utilizes
    application context for cross-cutting concerns like logging and security.
    """
    
    def __init__(self, account_repository: IAccountRepository, app_context: AppContext):
        """
        Initializes the AccountService with necessary dependencies.
        
        :param account_repository: The repository interface for account data operations.
        :param app_context: Shared application context for accessing current user information.
        """
        self.account_repository = account_repository
        self.app_context = app_context

    def create_account(self, data: dto.CreateAccountDto) -> dto.AccountDto:
        """
        Creates a new account with the provided data if it doesn't already exist.

        :param data: Data transfer object containing account creation details.
        :return: An AccountDto object representing the newly created account.
        :raises AlreadyExists: If an account with the provided email already exists.
        """
        
        # Check if an account with the given email already exists to prevent duplicates
        if self.account_repository.find_by_email(data.email):
            raise AlreadyExists("Account already exists")

        account = Account(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password
        )

        self.account_repository.save(account)

        # Return the created account as a DTO to hide sensitive information
        return dto.AccountDto.from_entity(account)

    def get_account(self, id: Id) -> dto.AccountDto:
        """
        Retrieves an account by its unique identifier. Only admins or the account owner can 
        access the account.

        :param id: The unique identifier of the account to retrieve.
        :return: An AccountDto object representing the retrieved account.
        :raises NotFound: If the account with the provided ID does not exist.
        """

        # Validate that the current user has permission to access the account
        validate(self.app_context, AdminOrSameUserPermission(AccountType.ADMIN, id))
        
        account = self.account_repository.find_by_id(id)

        if account is None:
            raise NotFound("Account not found")
        
        # Return the account as a DTO to hide sensitive information
        return dto.AccountDto.from_entity(account)

    def authenticate(self, data: dto.AuthenticateDto) -> dto.AccountDto:
        """
        Authenticates an account with the provided email and password present in a dto.

        :param data: Data transfer object containing account authentication details.
        :return: An AccountDto object representing the authenticated account.
        :raises InvalidCredentials: If the provided credentials are incorrect.
        """

        # Find the account by email and check if the password matches
        account = self.account_repository.find_by_email(data.email)
        
        if account and account.password == data.password:
            return dto.AccountDto.from_entity(account)
        
        raise InvalidCredentials
