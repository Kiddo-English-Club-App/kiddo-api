from abc import ABC, abstractmethod
from uuid import UUID

from .achievement import Achievement


class IAchievementRepository(ABC):

    @abstractmethod
    def find_all(self) -> list[Achievement]:
        pass

    @abstractmethod
    def find_by_id(self) -> list[Achievement]:
        pass

    @abstractmethod
    def find_many(self, ids: list[UUID]) -> list[Achievement]:
        pass

    @abstractmethod
    def find_not_in(self, ids: list[UUID]) -> list[Achievement]:
        pass

    @abstractmethod
    def save(self, entity: Achievement) -> None:
        pass
