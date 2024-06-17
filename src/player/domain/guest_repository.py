from abc import ABC, abstractmethod
from shared.id import Id

from .guest import Guest


class IGuestRepository(ABC):
    """
    IGuestRepository is an interface that defines the contract for the guest repository.
    """

    @abstractmethod
    def find_by_id(self, id: Id) -> Guest | None:
        """
        Find a guest by its unique identifier. If the guest does not exist, return None.

        :param id: The unique identifier of the guest.
        :return: The guest if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self, host_id: Id) -> list[Guest]:
        """
        Find all guests in the repository for a given host.

        :param host_id: The unique identifier of the host.
        :return: A list of guests.
        """
        pass

    @abstractmethod
    def save(self, entity: Guest) -> None:
        """
        Save a guest in the repository or update it if it already exists.

        :param entity: The guest to save.
        """
        pass

    @abstractmethod
    def delete_by_id(self, id: Id) -> bool:
        """
        Delete a guest by its unique identifier.

        :param id: The unique identifier of the guest.
        :return: True if the guest was deleted, False otherwise
        """
        pass
