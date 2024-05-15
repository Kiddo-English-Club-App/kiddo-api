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
    
    @abstractmethod
    def authorized(self, all_: list[str] = None, any_: list[str] = None) -> bool:
        pass


def authorize(attribute: str, all: list[str], any: list[str]):
    def wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            if not hasattr(self, attribute):
                raise ValueError(f"Attribute {attribute} not found")
            
            attr = getattr(self, attribute)

            if not attr:
                raise Unauthorized("Unauthorized")
            
            if not isinstance(attr, AppContext):
                raise ValueError(f"Attribute {attribute} must be a AppContext instance")

            if not attr.authorized(all_=all, any_=any):
                raise Unauthorized("Unauthorized")
            
            return func(self, *args, **kwargs)
        
        return wrapped
    return wrapper




    



