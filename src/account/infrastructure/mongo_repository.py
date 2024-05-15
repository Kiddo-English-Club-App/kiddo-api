from bunnet import Document
from pydantic import Field, EmailStr
from uuid import UUID

from shared.reference import Ref
from ..domain.account_type import AccountType
from ..domain.password import Password
from ..domain.account import Account
from ..domain.account_repository import IAccountRepository, AccountRef


class DBAccount(Document):
    id: UUID = Field(alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    account_type: AccountType

    
    class Settings:
        name = "accounts"
        indexes = ["email_1"]

    def from_entity(entity: Account):
        return DBAccount(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            password=entity.password.hashed,
            account_type=entity.account_type
        )

    def to_entity(self) -> Account:
        return Account(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=Password(self.password, hashed=True),
            account_type=self.account_type
        )


class MongoDBAccountRepository(IAccountRepository):

    def find_by_id(self, id: UUID) -> Account:
        _account = DBAccount.find_one({"_id": id}).run()
        if not _account:
            return None
        return _account.to_entity()
    
    def find_all(self, skip: int, limit: int) -> list[Account]:
        _accounts = DBAccount.find_all(skip=skip, limit=limit).run()
        return [_account.to_entity() for _account in _accounts]
    
    def save(self, entity: Account) -> None:
        _account = DBAccount.from_entity(entity)
        _account.save()

    def delete_by_id(self, id: UUID) -> bool:
        results = DBAccount.get_motor_collection().delete_one({"_id": id})
        return results.deleted_count > 0
    
    def find_by_email(self, email: str) -> Account:
        _account = DBAccount.find_one({"email": email}).run()
        if not _account:
            return None
        return _account.to_entity()
    
    def ref(self, id: UUID) -> Ref[Account]:
        return AccountRef(id, self)