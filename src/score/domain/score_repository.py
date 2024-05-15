from abc import ABC, abstractmethod
from uuid import UUID

from ..domain.score import Score


class IScoreRepository(ABC):
    @abstractmethod
    def find_all(self, guest_id: UUID) -> list[Score]:
        pass

    @abstractmethod
    def find_by_theme(self, guest_id: UUID, theme_id: UUID) -> Score:
        pass

    @abstractmethod
    def save(self, entity: Score) -> None:
        pass