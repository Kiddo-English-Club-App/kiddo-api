from abc import ABC, abstractmethod
from . import dto


class TokenService(ABC):

    @abstractmethod
    def create_access_token(self, account: dto.AccountDto) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, account: dto.AccountDto) -> str:
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> bool:
        pass

    @abstractmethod
    def read_token(self, token: str) -> dict:
        pass



