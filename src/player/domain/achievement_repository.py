from abc import ABC, abstractmethod

from shared.id import Id

from .achievement import Achievement


class IAchievementRepository(ABC):
    """
    IAchievementRepository is an interface that defines the contract for the achievement repository.
    """

    @abstractmethod
    def find_all(self) -> list[Achievement]:
        """
        Find all achievements in the repository.

        :return: A list of achievements.
        """
        pass

    @abstractmethod
    def find_by_id(self, id: Id) -> Achievement | None:
        """
        Find an achievement by its unique identifier. If the achievement does not exist, return None.

        :param id: The unique identifier of the achievement.
        :return: The achievement if found, None otherwise
        """
        pass

    @abstractmethod
    def find_many(self, ids: list[Id]) -> list[Achievement]:
        """
        Find multiple achievements by their unique identifiers.

        :param ids: A list of unique identifiers.
        :return: A list of achievements
        """
        pass

    @abstractmethod
    def find_not_in(self, ids: list[Id]) -> list[Achievement]:
        """
        Find achievements that are not in the list of unique identifiers.

        :param ids: A list of unique identifiers.
        :return: A list of achievements that are not in the list of unique identifiers.
        """
        pass

    @abstractmethod
    def save(self, entity: Achievement) -> None:
        """
        Save an achievement in the repository.

        :param entity: The achievement to save.
        """
        pass
