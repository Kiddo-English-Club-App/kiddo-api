from abc import ABC, abstractmethod
from uuid import UUID

from shared.reference import Ref
from .theme import Theme


class IThemeRepository(ABC):
    
    @abstractmethod
    def find_by_id(self, id: UUID) -> Theme:
        pass

    @abstractmethod
    def find_all(self) -> list[Theme]:
        pass

    @abstractmethod
    def save(self, entity: Theme) -> None:
        pass

    @abstractmethod
    def delete_by_id(self, id: UUID) -> bool:
        pass
    
    @abstractmethod
    def ref(self, id: UUID) -> Ref[Theme]:
        pass


class ThemeRef(Ref[Theme]):
    
    def __init__(self, id: UUID, repository: IThemeRepository):
        super().__init__(id)
        self._repository = repository

    def fetch(self) -> Theme:
        return self._repository.find_by_id(self.id)