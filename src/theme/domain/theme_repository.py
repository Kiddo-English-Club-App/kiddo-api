from abc import ABC, abstractmethod

from shared.id import Id
from shared.reference import Ref

from .theme import Theme


class IThemeRepository(ABC):
    """
    IThemeRepository is an interface that defines the methods that a theme repository
    should implement. A theme repository is responsible for storing and retrieving
    themes from a data source. It provides methods to find themes by their identifier,
    save a new theme, delete a theme by its identifier, and find all themes.
    """

    @abstractmethod
    def find_by_id(self, id: Id) -> Theme | None:
        """
        Retrieves a theme by its identifier. If the theme is not found, it returns None.

        :param id: The identifier of the theme to retrieve.
        :return: A Theme object representing the theme, if found, otherwise None.
        """
        pass

    @abstractmethod
    def find_all(self) -> list[Theme]:
        """
        Retrieves all themes in the repository as a list.

        :return: A list of Theme objects representing the themes.
        """
        pass

    @abstractmethod
    def save(self, entity: Theme) -> None:
        """
        Saves a new theme in the repository. If the theme already exists, it updates the existing one.

        :param entity: The Theme object to save.
        """
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        """
        Deletes a theme by its identifier. Returns True if the theme was deleted, False otherwise.

        :param id: The identifier of the theme to delete.
        :return: True if the theme was deleted, False otherwise.
        """
        pass

    @abstractmethod
    def ref(self, id: Id) -> Ref[Theme]:
        """
        Creates a reference to a theme by its identifier. The reference can be used to fetch the theme lazily.
        """
        pass


class ThemeRef(Ref[Theme]):
    def __init__(self, id: Id, repository: IThemeRepository):
        super().__init__(id)
        self._repository = repository

    def fetch(self) -> Theme:
        return self._repository.find_by_id(self.id)
