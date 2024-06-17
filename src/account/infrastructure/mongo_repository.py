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
    """
    DBAccount represents the account document stored in the MongoDB database.
    It maps the domain model to the database schema and provides methods for
    converting between the two representations.

    It's implemented as a Pydantic model to leverage its data validation and serialization
    capabilities, making it easier to work with MongoDB documents in a type-safe manner.
    """

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
        """
        Converts an Account entity to a DBAccount document. This method is used to
        store account data in the MongoDB database.

        :param entity: The Account entity to convert.
        :return: A DBAccount document representing the provided entity.
        """
        return DBAccount(
            id=entity.id.value,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            password=entity.password,
            account_type=entity.account_type,
        )

    def to_entity(self) -> Account:
        """
        Converts a DBAccount document to an Account entity. This method is used to
        load account data from the MongoDB database.

        :return: An Account entity representing the current document.
        """
        return Account(
            id=Id(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=PasswordStr(self.password, hashed=True),
            account_type=self.account_type,
        )


class MongoDBAccountRepository(IAccountRepository):
    def find_by_id(self, id: Id) -> Account:
        # Find the account document by ID and convert it to an entity
        _account = DBAccount.find_one({"_id": id.value}).run()
        if not _account:
            return None
        return _account.to_entity()

    def save(self, entity: Account) -> None:
        # Convert the entity to a document and save it to the database
        _account = DBAccount.from_entity(entity)
        _account.save()

    def delete_by_id(self, id: Id) -> bool:
        # Delete the account document by ID and return True if successful
        # or False if the account was not found
        # It uses the delete_one method from the driver to remove the document
        # instead of loading it first and then deleting it to reduce unnecessary
        # database queries.
        results = DBAccount.get_motor_collection().delete_one({"_id": id.value})
        return results.deleted_count > 0

    def find_by_email(self, email: str) -> Account:
        # Find the account document by email and convert it to an entity
        _account = DBAccount.find_one({"email": email}).run()
        if not _account:
            return None
        return _account.to_entity()

    def ref(self, id: Id) -> Ref[Account]:
        return AccountRef(id, self)
