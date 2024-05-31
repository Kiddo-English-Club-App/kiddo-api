from abc import ABC, abstractmethod

from shared.id import Id

from .achievement import Achievement


class IAchievementRepository(ABC):

    @abstractmethod
    def find_all(self) -> list[Achievement]:
        pass

    @abstractmethod
    def find_by_id(self, id: Id) -> list[Achievement]:
        pass

    @abstractmethod
    def find_many(self, ids: list[Id]) -> list[Achievement]:
        pass

    @abstractmethod
    def find_not_in(self, ids: list[Id]) -> list[Achievement]:
        pass

    @abstractmethod
    def save(self, entity: Achievement) -> None:
        pass
