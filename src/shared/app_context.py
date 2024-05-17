from abc import ABC, abstractmethod
from uuid import UUID
from functools import wraps
from .exceptions import Unauthorized


class AppContext(ABC):

    @abstractmethod
    def identity(self) -> UUID:
        pass

    @abstractmethod
    def account_type(self) -> str:
        pass

    @abstractmethod
    def authenticated(self) -> bool:
        pass




    



