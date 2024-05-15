from uuid import UUID
from pydantic import BaseModel, EmailStr, computed_field

from account.domain.account import Account, AccountType


class CreateAccountDto(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr


class AccountDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    account_type: AccountType

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @staticmethod
    def from_entity(entity: Account):
        return AccountDto(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            account_type=entity.account_type
        )

class AuthenticateDto(BaseModel):
    email: EmailStr
    password: str