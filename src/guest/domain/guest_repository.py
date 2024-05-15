from abc import ABC, abstractmethod
from uuid import UUID

from .guest import Guest


class IGuestRepository(ABC):
    
    @abstractmethod
    def find_by_id(self, id: UUID) -> Guest:
        pass

    @abstractmethod
    def find_all(self, host_id: UUID) -> list[Guest]:
        pass

    @abstractmethod
    def save(self, entity: Guest) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, id: UUID) -> bool:
        pass