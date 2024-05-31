"""
Account Repository Interface Definition.
"""
from abc import ABC, abstractmethod

from shared.id import Id
from shared.reference import Ref
from .account import Account


class IAccountRepository(ABC):
    """
    Interface for Account Repository.
    """

    @abstractmethod
    def find_by_id(self, id: Id) -> Account | None:
        """
        Finds an account by its id.

        Args:
            id (Id): The id of the account.
        
        Returns:
            The account entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def find_all(self) -> list[Account]:
        """
        Finds all accounts.

        Returns:
            A list of all account entities.
        """
        pass

    @abstractmethod
    def save(self, entity: Account) -> None:
        """
        Saves or updates an account entity.

        Args:
            entity (Account): The account entity to save.
        """
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        """
        Deletes an account by its id.

        Args:
            id (UUID): The id of the account.
        
        Returns:
            True if the account was deleted, False otherwise.
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Account:
        """
        Finds an account by its email.

        Args:
            email (str): The email of the account.
        
        Returns:
            The account entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def ref(self, id: Id) -> Ref[Account]:
        """
        Creates a reference to an account entity.

        Args:
            id (UUID): The id of the account.
        
        Returns:
            A reference to the account entity.
        """
        pass


class AccountRef(Ref[Account]):
    """
    Account Reference.
    """
    def __init__(self, id: Id, repository: IAccountRepository):
        super().__init__(id)
        self.__repository = repository
    
    def fetch(self) -> Account:
        return self.__repository.find_by_id(self.id)