from abc import ABC, abstractmethod

from shared.id import Id
from .account_type import AccountType


class AppContext(ABC):
    """
    AppContext is an interface that defines the contract for providing access to the current user identity
    and account type based on the application context.
    """

    @abstractmethod
    def identity(self) -> Id:
        """
        Get the current user identity.

        :return: The unique identifier of the current user.
        """
        pass

    @abstractmethod
    def account_type(self) -> AccountType:
        """
        Get the account type of the current user.

        :return: The account type of the current user.
        """
        pass

    @abstractmethod
    def authenticated(self) -> bool:
        """
        Check if the current user is authenticated. This method can be used to determine if the user
        has access to protected resources.
        """
        pass
