from uuid import UUID
from pydantic import BaseModel, EmailStr, computed_field

from account.application import dto


class LoginDto(BaseModel):
    email: EmailStr
    password: str


class RegisterDto(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    account_type: str = "USER"


class AccountDto(BaseModel):
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