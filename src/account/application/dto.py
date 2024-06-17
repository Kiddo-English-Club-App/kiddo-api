from typing import Protocol
from dataclasses import dataclass

from account.domain.account import Account, AccountType, Id


class CreateAccountDto(Protocol):
    """
    Data transfer object for creating a new account.

    It's represented as a protocol to enforce the required fields for account creation
    but doesn't provide any implementation details so that it can be used as a type hint
    or implemented with external libraries like Pydantic or dataclasses.
    """

    first_name: str
    last_name: str
    password: str
    email: str


class AuthenticateDto(Protocol):
    """
    Data transfer object for authenticating an account.

    It's represented as a protocol to enforce the required fields for account creation
    but doesn't provide any implementation details so that it can be used as a type hint
    or implemented with external libraries like Pydantic or dataclasses.
    """

    email: str
    password: str


@dataclass(kw_only=True)
class AccountDto:
    """
    Data transfer object for representing an account.

    It's used to hide sensitive information from the domain layer and provide a
    simplified representation of the account to be used in other layers of the application.

    It's implemented as a dataclass to provide a simple way to create immutable objects and
    decouple the DTO from any external libraries or frameworks.
    """

    id: Id
    first_name: str
    last_name: str
    email: str
    account_type: AccountType

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def from_entity(entity: Account) -> "AccountDto":
        """
        Creates a new AccountDto object from an Account entity.

        :param entity: An Account entity to convert to a DTO.
        :return: An AccountDto object representing the provided entity.
        """
        return AccountDto(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            account_type=entity.account_type,
        )

    def __eq__(self, value: object) -> bool:
        if isinstance(value, (AccountDto, Account)):
            return (
                self.id == value.id
                and self.first_name == value.first_name
                and self.last_name == value.last_name
                and self.email == value.email
                and self.account_type == value.account_type
            )

        return False
