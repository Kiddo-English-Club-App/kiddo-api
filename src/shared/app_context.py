from abc import ABC, abstractmethod

from shared.id import Id


class AppContext(ABC):

    @abstractmethod
    def identity(self) -> Id:
        pass

    @abstractmethod
    def account_type(self) -> str:
        pass

    @abstractmethod
    def authenticated(self) -> bool:
        pass
