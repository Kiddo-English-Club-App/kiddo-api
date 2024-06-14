"""
Data Transfer Objects (DTOs) for the account module containing Pydantic models.
"""
from uuid import UUID
from pydantic import BaseModel, EmailStr, computed_field

from account.application import dto


class LoginDto(BaseModel):
    """
    Data transfer object for account login requests.

    It's represented as a Pydantic model to leverage its data validation and serialization.
    It sticks to the LoginDto protocol defined in the account service to ensure compatibility.
    """
    email: EmailStr
    password: str


class RegisterDto(BaseModel):
    """
    Data transfer object for account registration requests.

    It's represented as a Pydantic model to leverage its data validation and serialization.
    It sticks to the CreateAccountDto protocol defined in the account service to ensure compatibility.
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    account_type: str = "USER"


class AccountDto(BaseModel):
    """
    Data transfer object for representing an account.

    It's used to hide sensitive information from the domain layer and provide a simplified
    representation of the account to be used in other layers of the application.

    It's implemented as a Pydantic model to leverage its data validation and serialization capabilities.

    The @computed_field decorator is used to define a read-only property that's computed based on other fields.
    """
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    account_type: str

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def new(account: dto.AccountDto) -> 'AccountDto':
        return AccountDto(
            id=account.id.value,
            first_name=account.first_name,
            last_name=account.last_name,
            email=account.email,
            account_type=account.account_type)