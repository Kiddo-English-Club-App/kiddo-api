from abc import ABC, abstractmethod
from shared.id import Id


class Ref[T](ABC):
    """
    Ref is an abstract class that represents a reference to a value that can be fetched
    from an external source. It provides a lazy loading mechanism to fetch the value
    only when it is needed.
    """
    id: Id
    __value: T

    def __init__(self, id: Id):
        self.id = id
        self.__value = None

    @abstractmethod
    def fetch(self) -> T:
        pass
    
    @property
    def value(self) -> T:
        if self.__value is None:
            self.__value = self.fetch()
        return self.__value