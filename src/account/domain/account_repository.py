"""
Account Repository Interface Definition.
"""
from abc import ABC, abstractmethod

from shared.id import Id
from shared.reference import Ref
from .account import Account


class IAccountRepository(ABC):
    """
    Interface for account repositories. Account repositories are responsible for
    persisting and retrieving account entities from a data store.

    The account repository provides an abstraction over the data access layer,
    allowing for different implementations to be used interchangeably in the application.
    """

    @abstractmethod
    def find_by_id(self, id: Id) -> Account | None:
        """
        Finds an account by its id. If the account does not exist, returns None.

        :param id: The id of the account.
        :return: The account entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def save(self, entity: Account) -> None:
        """
        Saves or updates an account entity.

        :param entity: The account entity to save or update.
        """
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        """
        Deletes an account by its id.

        :param id: The id of the account to delete.
        :return: True if the account was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Account | None:
        """
        Finds an account by its email.

        :param email: The email of the account.
        :return: The account entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def ref(self, id: Id) -> Ref[Account]:
        """
        Creates a reference to an account entity.

        :param id: The id of the account.
        :return: A reference to the account entity.
        """
        pass


class AccountRef(Ref[Account]):
    """
    Reference to an account entity. This class provides a way to reference an account entity
    without loading it from the repository until necessary.

    It allows for lazy loading of the account entity when needed, reducing the number of 
    unnecessary database queries in the application.
    """
    def __init__(self, id: Id, repository: IAccountRepository):
        super().__init__(id)
        self.__repository = repository
    
    def fetch(self) -> Account:
        return self.__repository.find_by_id(self.id)