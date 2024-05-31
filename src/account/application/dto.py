from typing import Protocol
from dataclasses import dataclass

from account.domain.account import Account, AccountType, Id


class CreateAccountDto(Protocol):
    first_name: str
    last_name: str
    password: str
    email: str


class AuthenticateDto(Protocol):
    email: str
    password: str


@dataclass(kw_only=True)
class AccountDto:
    id: Id
    first_name: str
    last_name: str
    email: str
    account_type: AccountType

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def from_entity(entity: Account) -> 'AccountDto':
        return AccountDto(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            account_type=entity.account_type
        )
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, (AccountDto, Account)):
            return \
                self.id == value.id and \
                self.first_name == value.first_name and \
                self.last_name == value.last_name and \
                self.email == value.email and \
                self.account_type == value.account_type
        
        return False
