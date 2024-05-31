from abc import ABC, abstractmethod

from shared.id import Id
from shared.reference import Ref
from .theme import Theme


class IThemeRepository(ABC):
    
    @abstractmethod
    def find_by_id(self, id: Id) -> Theme:
        pass

    @abstractmethod
    def find_all(self) -> list[Theme]:
        pass

    @abstractmethod
    def save(self, entity: Theme) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        pass
    
    @abstractmethod
    def ref(self, id: Id) -> Ref[Theme]:
        pass


class ThemeRef(Ref[Theme]):
    
    def __init__(self, id: Id, repository: IThemeRepository):
        super().__init__(id)
        self._repository = repository

    def fetch(self) -> Theme:
        return self._repository.find_by_id(self.id)