from bunnet import Document
from pydantic import Field, EmailStr
from uuid import UUID

from shared.id import Id
from shared.reference import Ref
from shared.account_type import AccountType
from ..domain.password import PasswordStr
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
            id=entity.id.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            password=entity.password,
            account_type=entity.account_type
        )

    def to_entity(self) -> Account:
        return Account(
            id=Id(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=PasswordStr(self.password, hashed=True),
            account_type=self.account_type
        )


class MongoDBAccountRepository(IAccountRepository):

    def find_by_id(self, id: Id) -> Account:
        _account = DBAccount.find_one({"_id": id.value}).run()
        if not _account:
            return None
        return _account.to_entity()
    
    def find_all(self, skip: int, limit: int) -> list[Account]:
        _accounts = DBAccount.find_all(skip=skip, limit=limit).run()
        return [_account.to_entity() for _account in _accounts]
    
    def save(self, entity: Account) -> None:
        _account = DBAccount.from_entity(entity)
        _account.save()

    def delete_by_id(self, id: Id) -> bool:
        results = DBAccount.get_motor_collection().delete_one({"_id": id.value})
        return results.deleted_count > 0
    
    def find_by_email(self, email: str) -> Account:
        _account = DBAccount.find_one({"email": email}).run()
        if not _account:
            return None
        return _account.to_entity()
    
    def ref(self, id: Id) -> Ref[Account]:
        return AccountRef(id, self)