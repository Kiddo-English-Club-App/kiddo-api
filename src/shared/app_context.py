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
        pass

    @abstractmethod
    def account_type(self) -> AccountType:
        pass

    @abstractmethod
    def authenticated(self) -> bool:
        pass
