from abc import ABC, abstractmethod
from shared.id import Id

from .guest import Guest


class IGuestRepository(ABC):
    
    @abstractmethod
    def find_by_id(self, id: Id) -> Guest:
        pass

    @abstractmethod
    def find_all(self, host_id: Id) -> list[Guest]:
        pass

    @abstractmethod
    def save(self, entity: Guest) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        pass