# Account service
from uuid import UUID

from account.domain.account import Account, AccountType
from account.domain.account_repository import IAccountRepository
from shared.exceptions import InvalidCredentials, NotFound
from shared.app_context import AppContext
from shared.permissions import AdminOrSameUserPermission, validate
from . import dto


class AccountService:
    
    def __init__(self, account_repository: IAccountRepository, app_context: AppContext):
        self.account_repository = account_repository
        self.app_context = app_context

    def create_account(self, data: dto.CreateAccountDto) -> dto.AccountDto:
        account = Account(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password
        )

        self.account_repository.save(account)

        return dto.AccountDto.from_entity(account)


    def get_account(self, id: UUID) -> dto.AccountDto:
        
        account = self.account_repository.find_by_id(id)
        if account is None:
            raise NotFound("Account not found")

        return dto.AccountDto.from_entity(account)

    def authenticate(self, data: dto.AuthenticateDto) -> dto.AccountDto:
        account = self.account_repository.find_by_email(data.email)
        
        if account and account.password == data.password:
            return dto.AccountDto.from_entity(account)

        raise InvalidCredentials
